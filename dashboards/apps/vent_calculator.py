

import copy
import json
import cantera as ct
import math

import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output

#from scripts.NFPA68 import Param,

from app import app
from .callbacks import * #noqa
from .controls import plot_layout
from .layouts import main_dropdowns
from .util import get_main_data, _get_fuel_species, AIR_SPECIES
from scripts.vent_model import Fuel, Geometry, Vent
from scripts.explosion_model import Explosion, Inputs, Patm


# Create app layout
#--------------------CONTAINER FOR WHOLE LAYOUT--------------------------------
layout = html.Div(
    [
        #---------------------TOP MAIN HEADER----------------------------------
        html.Div(
            [   #------------------------UT LOGO--------------------------------
                html.Div(
                    [
                        html.Img(
                            src=("/assets/shield.png"),
                            style={
                                "height": "60px",
                                "width": "auto",
                            }
                        )
                    ],
                    id="logo",
                    className="one-third column",
                    style={"textAlign": "left"}
                ),
                #---------------------TITLE AND SUBTITLE------------------------
                html.Div(
                    [
                        html.H3(
                            "Deflagration Vents",
                            style={"margin-bottom": "0px"}
                        ),
                        html.H5(
                            "NFPA 68 Sizing Calculator",
                        )
                    ],
                    id="title",
                    className="one-half column",
                    style={"margin-bottom":"30px"}
                    ),
                #--------------------PAGE LINK BUTTONS--------------------------
                html.Div(
                    [
                        html.A(                 #Hazard Analysis Buttton
                            html.Button("Hazard Analysis",
                                        id="hazard-analysis",
                                        style={'width': '100%'}
                            ),
                            href="/apps/hazard_analysis",
                            style={"float": "right", 'width': '250px'}
                        ),
                        html.A(                 #Building Deflagration Button
                            html.Button("Building Deflagration",
                                        id="building-deflagration",
                                        style={'width': '100%'}
                            ),
                            href="/apps/explosion_calculator",
                            style={"float":"right", 'width': '250px'}
                        )
                    ]
                )
            ],
                #---------------------HEADER STYLE------------------------------
                id="header",
                className="row flex-display",
                style={"margin-bottom": "25px"}
        ),
        #-----------------------EXPERIMENT SELECTION MENU-----------------------

        #----------------------WARNING SECTION---------------------------------
        html.Div(
            [
                html.H6('This calculator is only avaliable for 100% SOC data.'),
                html.H6('Please update your selection.')
            ],
            style={'text-align': 'center', 'display': 'none'},
            id='SOC-Warning'
        ),
        #-----------------------DATA INPUT SECTION------------------------------
        html.Div(
            [
                html.Div(
                    [
                        html.H6(
                            'Instructions:',
                            style={'margin-top': '0px'}
                        ),
                        #html.P('Disclaimer -- This calculator should only for first order approximations. It is not a substitute for a rigorous design analysis.'),
                        html.P('This calculator uses methodology described in NFPA 68 to estimate the vent area needed to effectively control over-pressure resulting from a deflagration of battery vent gas in an enclosed space. Results are approximate and should not be used as a substitute for a rigorous design analysis. The calculator takes eleven parameters as input and returns an estimate of the required vent area. Definitions for selected parameters are included below.',
                        style={}
                        ),
                        html.Hr(style={'margin-top': '0px', 'margin-bottom': '20px'}),
                        html.P([html.Strong('Reduced Pressure: '), html.Em('The maximum room pressure allowable during a vented deflagration.'),]),
                        html.P([html.Strong('Blockage Ratio: '), html.Em('In an average cross-section of the room (height x width), what fraction of the area is blocked by equipment or other obstructions?')]),
                        html.P([html.Strong('Static Activation Pressure: '), html.Em('Pressure at which the vent fails when the load is applied slowly in a quasi-static manner. (Provided by vent manufacturer.)')]),
                        html.P([html.Strong('Vent Discharge Coefficient: '), html.Em("Adjustment factor for flow losses through the vent on activation. (If you don't have a specific value, assume 0.7)")]),
                        html.P([html.Strong('Equivalence Ratio: '), html.Em("Ratio of the actual fuel-air ratio to the stoichiometric fuel-air ratio. (\u03A6 \u2248 1.1 will provide the highest deflagration pressures)")]),
                        html.Hr(style={'margin-top': '0px', 'margin-bottom': '20px'}),
                        html.P([html.Strong('1: '), html.Em("Select an experiment from the dropdown menu to populate the vent gas composition. (Pre-computed flammability parameters and vent sizing are currently only available for experiments at 100% State-Of-Charge)")]),
                        html.P([html.Strong('2: '), html.Em("Wait for the fuel species chart and flammability parameters table to populate. (If the composition chart fails to populate, please refresh the page)")]),
                        html.P([html.Strong('3: '), html.Em("Enter the remaining parameters and wait for the results field to populate.")]),
                    ],
                    className='pretty_container twelve columns',
                    style={'text-aling': 'center'}
                ),

            ],
            className='row flex-display'
        ),
        html.Hr(),
        main_dropdowns,
        html.Div(
            [
                html.Div(
                    [
                        html.H6([html.Strong('Note: '),html.Em('Pre-computed flammability parameters are only available for 100% SOC data.')])
                    ],
                    className='pretty_container twelve columns',
                    style={'clear': 'both'},
                    id='disclaimer'
                )
            ],
            className='row flex-display',
        ),
        html.Div(
            [
                html.Div(id='selected_experiment', style={'display': 'none'}),
                html.Div(id='gas_composition', style={'display': 'none'}),
                html.Div(id='flammability_data', style={'display': 'none'}),
                html.Div(id='fuel_param', style={'display': 'none'}),
                html.Div(id='master-input-parameters', style={'display': 'none'}),
                html.Div(
                    [
                        dcc.Graph(id='composition_plot')
                    ],
                    className='pretty_container eight columns',
                ),
                html.Div(
                    [
                        dash_table.DataTable(
                            id='summary_table',
                            columns=[{'name': 'Parameter', 'id': 'param'},
                                     {'name': 'Value', 'id': 'value'}],
                            data=[],
                            style_as_list_view=True,
                            style_cell={
                                'font-family': ["Open Sans", "HelveticaNeue",
                                                "Helvetica Neue", "Helvetica",
                                                "Arial", "sans-serif"],
                                'font-size': '18px',
                                'textAlign': 'center',
                                'height': '85px',
                                'minWidth': '0px', 'maxWidth': '180px',
                                'whiteSpace': 'normal'
                            },
                            style_cell_conditional=[{
                                'if': {'column_id': 'param'},
                                'textAlign': 'left'
                            }],
                            style_header_conditional=[{
                                'if': {'column_id': 'param'},
                                'textAlign': 'left'
                            }],
                            style_header={
                                'fontWeight': 'bold',
                                'textAlign': 'center'
                            },
                        )
                    ],
                    id="ftable_div",
                    className="pretty_container five columns"
                )
            ],
            className='row flex-display'
        ),
        html.Hr(),
        html.Div(
            [
                html.Div(
                    [
                        html.H6(
                            'Room Parameters:',
                            style={'margin-top': '0px'}
                        ),
                        dcc.Input(
                            id='room_height',
                            type='number',
                            min=0,
                            placeholder='Height (m)',
                            className='control_label',
                            style={'margin-bottom': '5px'}
                        ),
                        dcc.Input(
                            id='room_width',
                            type='number',
                            min=0,
                            placeholder='Width (m)',
                            className='control_label',
                            style={'margin-bottom': '5px'}
                        ),
                        dcc.Input(
                            id='room_length',
                            type='number',
                            min=0,
                            placeholder='Length (m)',
                            className='control_label',
                            style={'margin-bottom': '5px'}
                        ),
                        html.P(
                            [html.Strong('Note: '), html.Em('The length should be the longest horizontal dimension.')],
                            style={
                                'text-align': 'left',
                                'margin': '2px'}
                        ),
                    ],
                    className='pretty_container four columns',
                    id='room_input_panel'
                ),
                html.Div(
                    [
                        html.H6(
                            'Fuel Parameters:',
                            style={'margin-top': '0px'}
                        ),
                        dcc.Input(
                            id='equivalence_ratio',
                            type='number',
                            min=0,
                            placeholder='Equivalence Ratio',
                            className='control_label',
                            style={'margin-bottom': '5px'}
                        ),
                        dcc.Input(
                            id='blockage_ratio',
                            type='number',
                            min=0,
                            max=1,
                            placeholder='Blockage Ratio',
                            className='control_label',
                            style={'margin-bottom': '5px'}
                        ),
                        dcc.Input(
                            id='amb_pressure',
                            type='number',
                            min=0,
                            placeholder='Ambient Pressure (bar-g)',
                            className='control_label',
                            style={'margin-bottom': '5px'}
                        ),
                        dcc.Input(
                            id='amb_temp',
                            type='number',
                            min=0,
                            placeholder='Ambient Temperature (K)',
                            className='control_label',
                            style={'margin-bottom': '5px'}
                        ),
                    ],
                    className='pretty_container four columns',
                    id='flow_input_panel'
                ),
                # html.Div(
                #     [
                #         html.H6(
                #             'Combustion Parameters:',
                #             style={'margin-top': '0px'}
                #             ),
                #             dcc.Input(
                #                 id='laminar',
                #                 type='number',
                #                 min=0,
                #                 placeholder='Laminar Flame Speed (m/s)',
                #                 className='control_label',
                #                 style={'margin-bottom': '5px'}
                #             ),
                #             dcc.Input(
                #                 id='max_pressure',
                #                 type='number',
                #                 min=0,
                #                 placeholder='Adiabatic Pressure (bar-g)',
                #                 className='control_label',
                #                 style={'margin-bottom': '5px'}
                #             ),
                #             html.P(
                #                 [html.Em('Enter your own values or select an experiment above to see values for different cell types and chemistries')],
                #                 style={
                #                     'text-align': 'left',
                #                     'margin': '2px'}
                #             ),
                #     ],
                #     className='pretty_container four columns',
                #     id='vent_input_panel'
                # ),
                html.Div(
                    [
                        html.H6(
                            'Vent Parameters:',
                            style={'margin-top': '0px'}
                            ),
                            dcc.Input(
                                id='reduced_pressure',
                                type='number',
                                min=0,
                                placeholder='Reduced Pressure bar-g',
                                className='control_label',
                                style={'margin-bottom': '5px'}
                            ),
                            dcc.Input(
                                id='static_pressure',
                                type='number',
                                min=0,
                                placeholder='Static Activation Pressure (bar-g)',
                                className='control_label',
                                style={'margin-bottom': '5px'}
                            ),
                            dcc.Input(
                                id='vent_discharge',
                                type='number',
                                min=0,
                                placeholder='Vent Discharge Coefficient',
                                className='control_label',
                                style={'margin-bottom': '5px'}
                            ),
                            dcc.Input(
                                id='vent_number',
                                type='number',
                                min=1,
                                placeholder='Number of Vents',
                                className='control_label',
                                style={'margin-bottom': '5px'}
                            ),
                    ],
                    className='pretty_container four columns',
                    id='vent_input_panel'
                ),
            ],
            className='row flex-display',
        ),
        html.Div(
            [
                html.Div( #--------Results Pane---------
                    [
                        html.H6(
                            'Results:',
                            style={'margin-top': '0px'}
                        ),
                        html.Div(
                            [
                                html.H6(
                                    'Total Surface Area',
                                    style={
                                        'display': 'inline',
                                        'float': 'left',
                                        'width': '40%',
                                        'margin-left': '10px'
                                    }
                                ),
                                html.H6(
                                    id='total_surface_area',
                                    style={
                                        'display': 'inline',
                                        'float': 'right',
                                        'width': '60%',
                                        'text-align': 'right',
                                        'margin-right': '15px'
                                    }
                                )
                            ],
                            style={'clear': 'both', 'margin-top': '20px'},
                            className='row'
                        ),
                        html.Hr(style={'margin': '0px'}),
                        html.Div(
                            [
                                html.H6(
                                    'Required Vent Area',
                                    style={
                                        'display': 'inline',
                                        'float': 'left',
                                        'width': '40%',
                                        'margin-left': '10px'
                                    }
                                ),
                                html.H6(
                                    'N/A',
                                    id='required_surface_area',
                                    style={
                                        'display': 'inline',
                                        'float': 'right',
                                        'width': '60%',
                                        'text-align': 'right',
                                        'margin-right': '15px'
                                    }
                                )
                            ],
                            style={'clear': 'both'},
                            className='row'
                        )
                    ],
                    className='pretty_container twelve columns',
                    id='results_panel'
                )
            ],
            className='row flex-display'
        ),
        # html.Hr(),
        # html.H6(
        #     'Debugging Section',
        #     id = 'debug_label',
        # ),
        # html.Div(
        # [
        #     html.Div(
        #         [
        #             html.Div(id='master-output-parameters'),
        #             html.Hr(),
        #             html.Div(id='test-return'),
        #             html.Hr(),
        #             html.Div(id='comp_test'),
        #             html.Hr(),
        #             html.Div(id='dummy_dump'),
        #
        #         ],
        #         className='pretty_container twelve columns'
        #     )
        # ],
        # className='row flex-display'
        # )

        #-----------------------END INPUT SECTION----------------------------
    ]
)
#----------------------END OVERALL LAYOUT CONTAINER

#-------------MASTER INPUT PARAMETER CALLBACK ---------------------------------
@app.callback(
    [
        Output('master-input-parameters', 'children'),
        Output('master-output-parameters', 'children'),
    ],
    [
        Input('reduced_pressure', 'value'),
        Input('room_height', 'value'),
        Input('room_width', 'value'),
        Input('room_length', 'value'),
        Input('equivalence_ratio', 'value'),
        Input('blockage_ratio', 'value'),
        Input('amb_pressure', 'value'),
        Input('amb_temp', 'value'),
        Input('static_pressure', 'value'),
        Input('vent_discharge', 'value'),
        Input('vent_number', 'value'),
    ]
)
def master_parameter_input(rP, rH, rW, rL, eR, bR, aP, aT, sP, vD, vN):

     '''
     Takes all of the input fields and packages them into a single data object
     that can be unpacked in a subsequent callback.
     '''

     if rP and rH and rW and rL and eR and bR and aP and aT and sP and vD and vN:

         input_array = {
            'Height': rH,
            'Width': rW,
            'Length': rL,
            'Phi': eR,
            'Block': bR,
            'AmbientP': aP,
            'AmbientT': aT,
            'Static': sP,
            'Discharge': vD,
            'Number': vN,
            'rPressure': rP
             }

         jArray = json.dumps(input_array)

         return jArray, jArray

#-----------PERFORM THE ACTUAL COMPUTATION-------------------------------------

@app.callback(
    [
        Output('required_surface_area', 'children'),
        Output('total_surface_area', 'children')
    ],
    [
        Input('master-input-parameters', 'children'),
        Input('gas_composition', 'children'),
        Input('flammability_data', 'children'),
    ]

)
def sizing_calc(iParameters, gases, fData):

    #unpack all of the JSON data objects
    iParameters = json.loads(iParameters) if iParameters else {} #user parameters
    gases = json.loads(gases) if gases else {} #database gas composition
    fData = json.loads(fData) if fData else {} #database flammability data

    if iParameters and gases and fData:

        #find UFL - LFL - Su - Pmax from flammabilty data
        if fData is not None:
            fData.pop('_id')
            df = pd.DataFrame.from_dict(fData,
                                        orient='index').transpose()

            ufl = max(df[(df.Xi == 0) & (df.Flammable == 1)].Xf) * 100
            lfl = min(df[(df.Xi == 0) & (df.Flammable == 1)].Xf) * 100
            su = max(df.Su)
            p_max = max(df.Pmax)

        fuel_species = _get_fuel_species(gases) #makes non-cantera species propane

        Aw1 = iParameters['Length']*iParameters['Height']
        Aw2 = iParameters['Width']*iParameters['Height']
        Aw3 = iParameters['Width']*iParameters['Length']

        iVentPercent = 0.4

        #create gas properties object
        gas_comp = Fuel(
            air = AIR_SPECIES,
            fuel = fuel_species,
            phi = iParameters['Phi'],
            f = 1.0,
            P = iParameters['AmbientP'],
            T = iParameters['AmbientT'],
            S = su,
            Block = iParameters['Block'],
            Reduced = iParameters['rPressure'],
            Drag = iParameters['Discharge'],
            Static = iParameters['Static'],
            Number = iParameters['Number'],
            Adiabatic = p_max
        )

        userInput = Fuel(
            L = iParameters['Length'],
            W = iParameters['Width'],
            H = iParameters['Height'],
        )

        cntrl = Fuel(
            tmax = 0.35
        )

        explode = Vent(gas=gas_comp, room=userInput, cntrl = cntrl)

        ventPercent = 0.3
        ventNum = iParameters['Number']
        Av1 = ventPercent*Aw1
        Avg = 0.001
        Avo = 0

        Asurface = 2*Aw1 + 2*Aw2 + Aw3

        while 100*abs(Avo-Avg)/(0.5*(Avo+Avg)) > 1:

            Avo = explode.areaV(Av1)
            Avg = Av1
            Av1 = Avo
        #dddd = explode.areaV(Av1)

        #dedud = {'VentArea': Avo}
        #dedud = json.dumps(dedud)
        #dddd = json.dumps(dddd)

        #return dddd, fuel_species
        return '{:.2f} m\u00b2'.format(Avo), '{:.2f} m\u00b2'.format(Asurface)

    else:
        return 'Error', 'Error'

#----------FUEL COMPOSITION DEBUGGING -----------------------------------------
@app.callback(
    [
    Output('dummy_dump', 'children'),
    Output('comp_test', 'children')
    ],
    [
        Input('flammability_data', 'children'),
        Input('gas_composition', 'children')
    ]
)
def gas_comp_debug(flame, gases):

    if gases:                                  #check if data has been stored
        un_flame = json.loads(flame)           #unpack JSON data from 'gas_composition'
        un_gas = json.loads(gases)

        return '"{}"'.format(un_flame), '"{}"'.format(un_gas)
    else:
        return 'Invalid Input', 'Invalid Input'
