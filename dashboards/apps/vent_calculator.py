

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
                                        id="hazard-analysi",
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
                        html.P('This calculator uses methodology described in NFPA 68 to estimate the vent area needed to effectively control over-pressure resulting from a deflagration of battery vent gas in an enclosed space. Results are approximate and should not be used as a substitute for a rigorous design analysis. The calculator takes eleven parameters as input and returns the required vent area. Definitions for each parameter is included below.',
                        style={}
                        ),
                        html.Hr(style={'margin-top': '0px', 'margin-bottom': '20px'}),
                        html.P([html.Strong('Reduced Pressure: '), html.Em('The maximum room pressure allowable during a vented deflagration.'),]),
                        html.P([html.Strong('Blockage Ratio: '), html.Em('In an average cross-section of the room (height x width), what fraction of the area is blocked by equipment or other obstructions?')]),
                        html.P([html.Strong('Static Activation Pressure: '), html.Em('Pressure at which the vent fails when the load is applied slowly in a quasi-static manner. (Provided by vent manufacturer.)')]),
                        html.P([html.Strong('Vent Discharge Coefficient: '), html.Em("Adjustment factor for flow losses through the vent on activation. (If you don't have a specific value, assume 0.7)")]),
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
        html.Hr(),
        html.H6(
            'Debugging Section',
            id = 'debug_label',
        ),
        html.Div(
        [
            html.Div(
                [
                    html.Div(id='room_geometry'),
                    html.Hr(),
                    html.Div(id='vent_pp'),
                    html.Hr(),
                    html.Div(id='comp_test'),
                    html.Hr(),
                    html.Div(id='fuel_test'),
                    html.Hr(),
                    html.Div(id='test_return'),
                    html.Hr(),
                    html.Div(id='dummy_dump'),

                ],
                className='pretty_container twelve columns'
            )
        ],
        className='row flex-display'
        )

        #-----------------------END INPUT SECTION----------------------------
    ]
)
#----------------------END OVERALL LAYOUT CONTAINER----------------------------

#-------INTAKE GEOMETRY PARAMETERS AND PACKAGE AS OBJECT-----------------------
@app.callback(
    [
    Output('total_surface_area', 'children'),
    Output('room_geometry', 'children')
    ],
    [
        Input('room_height','value'),
        Input('room_width', 'value'),
        Input('room_length','value'),
    ]
)
def surface_calc(height, width, length):

    if height and width and length:

        As = (1)*(width*length) + (2)*(height*width) + (2)*(height*length)

        room_geo = {
            'rHeight': height,
            'rWidth': width,
            'rLength': length,
        }

        room_geo = json.dumps(room_geo)

        return '{} m\u00b2'.format(As), room_geo
    else:
        return 'N/A', 'empty'

#-------INTAKE FUEL AND COMBUSTION PARAMETERS AND PACKAGE AS OBJECT------------
@app.callback(
    [
        Output('fuel_param', 'children'),
        Output('fuel_test', 'children'),
    ],
    [
        Input('equivalence_ratio','value'),
        Input('blockage_ratio', 'value'),
        Input('amb_pressure', 'value'),
        Input('amb_temp','value'),
    ]
)
def fuel_pack(equiv, block, apres, atemp):

    if equiv and block and apres and atemp:

        vent_gas = {
            'phi': equiv,
            'block': block,
            'ambient_P': apres,
            'ambient_T': atemp,
        }

        vent_gas = json.dumps(vent_gas)

        return vent_gas, vent_gas

#-------INTAKE VENT PARAMETERS AND PACKAGE AS OBJECT---------------------------
@app.callback(
    [
    Output('vent_param', 'children'),
    Output('vent_pp', 'children')
    ],
    [
        Input('static_pressure', 'value'),
        Input('vent_discharge', 'value')
    ]
)
def vent_pack(static_ap, discharge):

    if static_ap and discharge:

        vent = {
            'static': static_ap,
            'discharge': discharge
        }

        vent = json.dumps(vent)

        return vent, vent
    else:
        return 'empty', 'empty'

#-----------PERFORM THE ACTUAL COMPUTATION-------------------------------------

@app.callback(
    [
        Output('required_surface_area', 'children'),
        Output('test_return', 'children')
    ],
    [
        Input('room_geometry', 'children'),
        Input('gas_composition', 'children'),
        Input('fuel_param', 'children'),
        Input('flammability_data', 'children'),
        Input('vent_number', 'value')
    ]

)
def sizing_calc(geom, gases, flame_p, flame_d, num):

    #unpack all of the JSON data objects
    flame_pp = json.loads(flame_p) if flame_p else {}
    geom = json.loads(geom) if geom else {}
    gases = json.loads(gases) if gases else {}
    flammability_data = json.loads(flame_d) if flame_d else {}

    if flame_pp:
        test1 = True
    else:
        test1 = False
    if geom:
        test2 = True
    else:
        test2 = False
    if gases:
        test3 = True
    else:
        test3 = False
    if flammability_data:
        test4 = True
    else:
        test4 = False
    if num:
        test5 = True
    else:
        test5 = False

    test_array = {'flame_p': flame_pp, 'geom': test2, 'gases': test3, 'flammability_data': test4, 'num': num}
    test_array = json.dumps(test_array)

    if geom and gases and flame_p and flame_d:

        #find flame parameters
        if flammability_data is not None:
            flammability_data.pop('_id')
            df = pd.DataFrame.from_dict(flammability_data,
                                        orient='index').transpose()

            ufl = max(df[(df.Xi == 0) & (df.Flammable == 1)].Xf) * 100
            lfl = min(df[(df.Xi == 0) & (df.Flammable == 1)].Xf) * 100
            su = max(df.Su)
            p_max = max(df.Pmax)

        fuel_species = _get_fuel_species(gases) #makes non-cantera species propane

        #create gas properties object
        gas = Input(
            air = AIR_SPECIES,
            fuel = fuel_species,
            phi = flame_p['phi'],
            f = 1.0,
            P = flame_P['ambient_P'],
            T = flame_P['ambient_T'],
            S = su,
        )

        room = Inputs(
            L = geom['rLength'],
            W = geom['rWidth'],
            H = geom['rHeight'],
        )

        cntrl = Inputs(
            tmax = 0.35
        )

        Aw1 = geom['rLength']*geom['rHeight']
        Aw2 = geom['rWidth']*geom['rHeight']
        Aw3 = geom['rWidth']*geom['rLength']

        explode = Explosion(gas=gas, room=room, cntrl = cntrl)

        ventPercent = 0.5
        ventNum = num
        Av1 = ventPercent*Aw1

        while 100*abs(Avo-Avg)/(0.5*(Avo+Avg)) > 1:

            Avo = ventarea(Av1)
            Avg = Av1
            Av1 = Avo

        dedud = {'VentArea': Avo}
        dedud = json.dumps(dedud)

        return '{} m\u00b2'.format(Avo), dedud

    else:
        test_value = 99
        return '{} m\u00b2'.format(test_value), test_array#'{} m\u00b2'.format(test_value)

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
