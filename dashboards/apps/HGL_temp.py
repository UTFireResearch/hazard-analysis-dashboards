import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table as dtab
from dash.dependencies import Input, Output, State
from .controls import plot_layout

from app import app

import numpy as np
import copy

#----------------------APPlICATION LAYOUT---------------------------------------
layout = html.Div(
    [   #-----------------------HEADER BAR DIV---------------------------------
        html.Div(
            [   #---------------------LEFT HEADER COLUMN-----------------------
                html.Div(
                    [   #-----------------UT LOGO------------------------------
                        html.Img(
                            src=("/assets/shield.png"),
                            style={
                                "height": "60px",
                                "width": "auto",
                                "textAlign": 'center',
                            }
                        )
                    ],
                    id="logo",
                    style={'textAlign': 'left'},
                    className='one-third column',
                ),
                #---------------------CENTER HEADER COLUMN---------------------
                html.Div(
                    [   #-------------------HEADER TITLE-----------------------
                        html.H3(
                            'Fire Tools:',
                            style={'margin-bottom': '5px'}
                        ),
                        html.H6(
                            'Hot Gas Layer Temperature Calculator',
                            style={'margin': '0px'}
                        )
                    ],
                    id="title",
                    className='one-half column',
                    style={"margin-bottom": "5px", "margin-top": "5px",'textAlign': 'center'}
                ),
                #--------------------LEGACY NAVIGATION BUTTONS-----------------
                #---------------------RIGHT HEADER COLUMN----------------------
                html.Div(
                    [
                        html.A(
                            html.Button("Fire Research Group",
                                        id="building-deflagration",
                                        style={'width':'100%'}
                            ),
                            href='https://utfireresearch.com',
                            target="_blank",
                            style={"float": "right", "width": "240px"}
                        ),
                    ],
                    className="one-third column",
                    id="button",
                    style={'margin-right': '10px'}
                ),
            ],
            id="header",
            className='row flex-display',
            style={
                "margin-bottom": "30px"
            }
        ), #-----------------------END HEADER DIV------------------------------
        #---------------START INSTRUCTION FLEX-ROW------------------------------
        html.Div(
            [

            ],
            className= "row flex-display",
        ),
        #----------------START MIDDLE INPUT FLEX ROW---------------------------
        html.Div(
            [
                html.Div(
                    [   html.H5(
                            html.B('Enter Input Parameters'),
                            style={"margin-bottom": "15px", "color": "maroon"},
                        ),
                        html.H6(
                            'Fire Parameters',
                            style={'margin-left':'20px'}
                        ),
                        #-------MAXIMUM FIRE SIZE FIELD AND LABEL--------------
                        html.Div(
                            [
                                html.P(
                                    'Maximum Fire Size: ',
                                    style={'margin-right':'35px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='HGL_size_in',
                                type='number',
                                placeholder='kW',
                                size='15',
                                value=300,
                                ),
                                html.P(
                                    'kW',
                                    style={'margin-left':'10px','margin-top':'5px'}
                                ),
                            ],
                            className="row flex-display",
                            style={
                                'margin-left':'20px',
                                'margin-top':'10px',
                                'margin-bottom': '10px',
                                'vertical-align': 'middle',
                            }
                        ),
                        html.H6(
                            'Time Parameters',
                            style={'margin-left':'20px'}
                        ),
                        #-------------TIME FIELD AND LABEL---------------------
                        html.Div(
                            [
                                html.P(
                                    'Time: ',
                                    style={'margin-right':'128px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='HGL_time_in',
                                type='number',
                                placeholder='s',
                                size='15',
                                value=300,
                                ),
                                html.P(
                                    's',
                                    style={'margin-left':'10px','margin-top':'5px'}
                                ),
                            ],
                            className="row flex-display",
                            style={
                                'margin-left':'20px',
                                'margin-top':'10px',
                                'margin-bottom': '10px',
                                'vertical-align': 'middle',
                            }
                        ),
                        html.H6(
                            'Ventilation Parameters',
                            style={'margin-left':'20px'}
                        ),
                        #-----------VENTILATION WIDTH FIELD AND LABEL-----------
                        html.Div(
                            [
                                html.P(
                                    'Vent Width: ',
                                    style={'margin-right':'85px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='HGL_vent_width',
                                type='number',
                                placeholder='m',
                                size='15',
                                value=0.8,
                                ),
                                html.P(
                                    'meters',
                                    style={'margin-left':'10px','margin-top':'5px'}
                                ),
                            ],
                            className="row flex-display",
                            style={
                                'margin-left':'20px',
                                'margin-top':'10px',
                                'margin-bottom': '10px',
                                'vertical-align': 'middle',
                            }
                        ),
                        #-----------VENTILATION HEIGHT FIELD AND LABEL-----------
                        html.Div(
                            [
                                html.P(
                                    'Vent Height: ',
                                    style={'margin-right':'83px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='HGL_vent_height',
                                type='number',
                                placeholder='m',
                                size='15',
                                value=2.0,
                                ),
                                html.P(
                                    'meters',
                                    style={'margin-left':'10px','margin-top':'5px'}
                                ),
                            ],
                            className="row flex-display",
                            style={
                                'margin-left':'20px',
                                'margin-top':'10px',
                                'margin-bottom': '10px',
                                'vertical-align': 'middle',
                            }
                        ),
                        html.H6(
                            'Compartment Parameters',
                            style={'margin-left':'20px'}
                        ),
                        #-----------COMPARTMENT LENGTH FIELD AND LABEL-----------
                        html.Div(
                            [
                                html.P(
                                    'Room Length: ',
                                    style={'margin-right':'75px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='HGL_room_length',
                                type='number',
                                placeholder='m',
                                size='15',
                                value=3.6,
                                ),
                                html.P(
                                    'meters',
                                    style={'margin-left':'10px','margin-top':'5px'}
                                ),
                            ],
                            className="row flex-display",
                            style={
                                'margin-left':'20px',
                                'margin-top':'10px',
                                'margin-bottom': '10px',
                                'vertical-align': 'middle',
                            }
                        ),
                        #-----------COMPARTMENT WIDTH FIELD AND LABEL-----------
                        html.Div(
                            [
                                html.P(
                                    'Room Width: ',
                                    style={'margin-right':'75px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='HGL_room_width',
                                type='number',
                                placeholder='m',
                                size='15',
                                value=2.4,
                                ),
                                html.P(
                                    'meters',
                                    style={'margin-left':'10px','margin-top':'5px'}
                                ),
                            ],
                            className="row flex-display",
                            style={
                                'margin-left':'20px',
                                'margin-top':'10px',
                                'margin-bottom': '10px',
                                'vertical-align': 'middle',
                            }
                        ),
                        #-----------COMPARTMENT HEIGHT FIELD AND LABEL---------
                        html.Div(
                            [
                                html.P(
                                    'Room Height: ',
                                    style={'margin-right':'75px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='HGL_room_height',
                                type='number',
                                placeholder='m',
                                size='15',
                                value=2.4,
                                ),
                                html.P(
                                    'meters',
                                    style={'margin-left':'10px','margin-top':'5px'}
                                ),
                            ],
                            className="row flex-display",
                            style={
                                'margin-left':'20px',
                                'margin-top':'10px',
                                'margin-bottom': '10px',
                                'vertical-align': 'middle',
                            }
                        ),
                        #---COMPARTMENT AMBIENT TEMPERATURE FIELD AND LABEL-----
                        html.Div(
                            [
                                html.P(
                                    'Ambient Temperature: ',
                                    style={'margin-right':'25px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='HGL_amb_temp',
                                type='number',
                                placeholder='C',
                                size='15',
                                value=20,
                                ),
                                html.P(
                                    '\u00B0C',
                                    style={'margin-left':'10px','margin-top':'5px'}
                                ),
                            ],
                            className="row flex-display",
                            style={
                                'margin-left':'20px',
                                'margin-top':'10px',
                                'margin-bottom': '10px',
                                'vertical-align': 'middle',
                            }
                        ),
                        html.H6(
                            'Wall Parameters',
                            style={'margin-left':'20px'}
                        ),
                        #--------------WALL THICKNESS FIELD AND LABEL-----------
                        html.Div(
                            [
                                html.P(
                                    'Wall Thickness: ',
                                    style={'margin-right':'75px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='HGL_wall_thickness',
                                type='number',
                                placeholder='m',
                                size='15',
                                value=0.016,
                                ),
                                html.P(
                                    'meters',
                                    style={'margin-left':'10px','margin-top':'5px'}
                                ),
                            ],
                            className="row flex-display",
                            style={
                                'margin-left':'20px',
                                'margin-top':'10px',
                                'margin-bottom': '10px',
                                'vertical-align': 'middle',
                            }
                        ),
                        #------WALL THERMAL CONDUCTIVITY FIELD AND LABEL--------
                        html.Div(
                            [
                                html.P(
                                    'Wall Thermal Conductivity: ',
                                    style={'margin-right':'10px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='HGL_thermal_cond',
                                type='number',
                                placeholder='W/m-k',
                                size='15',
                                value=0.48,
                                ),
                                html.P(
                                    'W/m-k',
                                    style={'margin-left':'10px','margin-top':'5px'}
                                ),
                            ],
                            className="row flex-display",
                            style={
                                'margin-left':'20px',
                                'margin-top':'10px',
                                'margin-bottom': '10px',
                                'vertical-align': 'middle',
                            }
                        ),
                        #-------------WALL SPECIFIC HEAT FIELD AND LABEL--------
                        html.Div(
                            [
                                html.P(
                                    'Wall Specific Heat: ',
                                    style={'margin-right':'60px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='HGL_cp',
                                type='number',
                                placeholder='J/kg-k',
                                size='15',
                                value=840,
                                ),
                                html.P(
                                    'J/kg-k',
                                    style={'margin-left':'10px','margin-top':'5px'}
                                ),
                            ],
                            className="row flex-display",
                            style={
                                'margin-left':'20px',
                                'margin-top':'10px',
                                'margin-bottom': '10px',
                                'vertical-align': 'middle',
                            }
                        ),
                        #-------------WALL DENSITY FIELD AND LABEL--------------
                        html.Div(
                            [
                                html.P(
                                    'Wall Density: ',
                                    style={'margin-right':'90px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='HGL_density',
                                type='number',
                                placeholder='kg/m^3',
                                size='15',
                                value=1440,
                                ),
                                html.P(
                                    'kg/m^3',
                                    style={'margin-left':'10px','margin-top':'5px'}
                                ),
                            ],
                            className="row flex-display",
                            style={
                                'margin-left':'20px',
                                'margin-top':'10px',
                                'margin-bottom': '10px',
                                'vertical-align': 'middle',
                            }
                        ),
                        html.Div(
                            [
                                html.Button(
                                    'Calculate HGL Temperatures >>',
                                    id='HGL_submit',
                                    style={
                                    "margin-left": '2px',
                                    "margin-bottom": '15px',
                                    "margin-top": '15px'
                                    }
                                )
                            ],
                            className="row flex-display",
                            style={
                                'margin-left':'20px',
                                'margin-top':'10px',
                                'margin-bottom': '10px',
                                'vertical-align': 'middle',
                            }
                        ),

                    ],
                    id='HGL_input_container',
                    className='pretty_container four columns',
                ),
                html.Div(
                    [   html.H5(
                            html.B('Instructions'),
                            style={"margin-bottom": "15px", "color": "maroon"},
                        ),
                        html.P(
                            'This tool calculates a steady-state hot gas layer (HGL) temperature as a function of heat release rate (HRR) at a given time based on the correlation by McCaffrey, Quintiere, and Harkleroad (MQH).',
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.P(
                            [
                            'The thermal penetration time (s) through the wall is calculated by \u03B4',
                            html.Sup('2'),
                            '/(4\u03B1).',
                            ],
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.P(
                            [
                            'If the input time is less than the thermal penetration time (',
                            html.I('t'),
                            '<',
                            html.I('t'),
                            html.Sub('p'),
                            '), then the effective heat transfer coefficient is calculated by:',
                            ],
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.Img(
                            src=('/assets/HGL_eq1_mod.PNG'),
                            style={'height': '40px', 'margin-left': '20px'},
                        ),
                        html.P(
                            [
                            'If the input time is greater than or equal to the thermal penetration time (',
                            html.I('t '),
                            '>= ',
                            html.I('t'),
                            html.Sub('p'),
                            '), then the effective heat transfer coefficient is calculated by ',
                            html.I('h'),
                            html.Sub('k'),
                            ' = ',
                            html.I('k / \u03B4.')
                            ],
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.P(
                        [
                            'The total wall area (m',
                            html.Sup('2'),
                            ') is calculated by:',
                        ],
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.Img(
                            src='/assets/HGL_eq3_mod.PNG',
                            style={'height': '35px', 'margin-left': '20px'},
                        ),
                        html.P(
                            'The hot gas layer temperature MQH correlation is given by: ',
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.Img(
                            src='/assets/HGL_eq4_mod.PNG',
                            style={'height': '55px', 'margin-left': '20px'},
                        )

                    ],
                    id='HGL_instructions_container',
                    className='pretty_container nine columns',
                ),
            ],
            className= "row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H5(
                            html.B('Results:'),
                            style={
                            "margin-bottom": "0px",
                            "color": "maroon"
                            }
                        ),
                        #DIV WITH OUTPUT DESCRIPTIVE STRINGS
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.P(
                                                    'Wall thermal penetration time:  ',
                                                    style={'margin-right':'20px'}
                                                ),
                                            ],
                                            className='one-half column'
                                        ),
                                        html.Div(
                                            [
                                                html.P(
                                                    id='HGL_String1'
                                                ),
                                            ],
                                            className='one-half column',
                                        ),
                                    ],
                                    className='row flex-display',
                                ),
                                html.Hr(),
                                html.Div(
                                    [
                                        html.P(
                                            html.B(id='HGL_String2'),
                                            style={'textAlign':'center'},
                                        ),

                                    ],
                                    className='row flex-display',
                                ),
                                html.Hr(),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.P(
                                                    'Effective heat transfer coefficient:  ',
                                                    style={'margin-right':'20px'}
                                                ),
                                            ],
                                            className='one-half column'
                                        ),
                                        html.Div(
                                            [
                                                html.P(
                                                    html.B(id='HGL_String3')
                                                ),
                                            ],
                                            className='one-half column',
                                        ),
                                    ],
                                    className='row flex-display',
                                ),
                                html.Hr(),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.P(
                                                    'Total wall area:  ',
                                                    style={'margin-right':'20px'}
                                                ),
                                            ],
                                            className='one-half column'
                                        ),
                                        html.Div(
                                            [
                                                html.P(
                                                    html.B(id='HGL_String4')
                                                ),
                                            ],
                                            className='one-half column',
                                        ),
                                    ],
                                    className='row flex-display',
                                ),
                            ],
                            id='HGL_dStrings',
                            className='one-third column',
                            style={'color':'black','margin-left':'15px','margin-top':'40px'},
                        ),
                        html.Div(
                            [
                                dcc.Graph(id='HGL_graph'),
                            ],
                            style={
                                "height":'450px',
                                "width":'700px',
                                "padding-left":'10px',
                                "padding-right":'10px'
                            },
                            className='one-half column'
                        ),
                        # html.Div(
                        #     [
                        #         dtab.DataTable(
                        #             id='table',
                        #             columns
                        #         )
                        #     ],
                        #     className='one-third column'
                        # )

                    ],
                    id='HGL_results_container',
                    className='pretty_container twelve columns',
                )
            ],
            id='HGL_results_row',
            className='row flex-display',
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            'This is a placeholder!!!',
                            id='HGL_eMessage',
                        ),
                    ],
                    id='HGL_error_container',
                    className='pretty_container twelve columns',
                )
            ],
            id='HGL_error_row',
            className='row flex-display',
        ),
        #----------------BOTTOM ACKNOWLEDGEMENTS ROW---------------------------
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            'This calculator was develop by Dr. Kris Overholt and it is based on a Matlab script by Randall McDermott. This calculator is powered by the free and open source tools Python, Numpy, Matplotlib, and Plotly|Dash.',
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
                        ),
                    ],
                    className="pretty_container twelve columns",
                ),
            ],
            className= "row flex-display",
        ),
        #------------SECTION TO HOLDEN HIDDEN VALUE PASSING DIVS----------------
        html.Div(id='HGL_comp_state1',children='FALSE',style={"display": "none"}),
    ],
), #---------------------END LAYOUT--------------------------------------------


#------------------------START FUNCTION DEFITIONS-------------------------------

def HGL_input_check(inList):

    if not all(inList):
        return False, 'You appear to be missing a required field.'

    #VERIFY THAT X1 GREATER THAN X0
    if inList[0] >= inList[1] or inList[2] >= inList[3] or inList[4] >= inList[5]:
        return False, 'Ensure that maximum coordinates are GREATER than minimum coordinates.'

    #VERIFY THAT FIRE PARAMETERS ARE ALL GREATER THAN ZERO
    if inList[6] <= 0 or inList[7] <= 0 or inList[8] <= 0 or inList[9] <= 0 or inList[10] <= 0:
        return False, 'Ensure that all of the fire parameters are POSITIVE and NON-ZERO'

    return [True, '']

#------------------------CALLBACK DEFINITIONS-----------------------------------
@app.callback(
    [
        Output('HGL_results_row','style'),
        Output('HGL_error_box','style'),
    ],
    [
        Input('HGL_comp_state1','children'),
    ],
    [
        State('HGL_submit','n_clicks'),
    ]
)
def HGL_visibility_toggle(Mcomp1, clicks):

    display_style = {
        "margin-bottom": "15px",
        "color": "maroon"
        }

    hidden_style = {
        "margin-bottom": "15px",
        "color": "maroon",
        "display": "none"
        }

    btn_hidden = {'display':'none'}

    btn_shown = {'display':'block'}

    return display_style, display_style

    #
    # if Mcomp1 == 'TRUE' and clicks > 0:
    #     return display_style, hidden_style
    #
    # if Mcomp1 == 'FALSE' and clicks == None:
    #     return hidden_style, hidden_style
    #
    # if Mcomp1 == 'FALSE' and clicks > 0:
    #     return hidden_style, display_style

@app.callback(
    [
        Output('HGL_eMessage','children'),
        Output('HGL_sMessage','children'),
        Output('HGL_graph','figure'),
        Output('HGL_comp_state1','children'),
        Output('HGL_String1','children'),
        Output('HGL_String2','children'),
        Output('HGL_String3','children'),
        Output('HGL_String4','children'),
    ],
    [
        Input('HGL_submit','n_clicks'),
    ],
    [
        State('HGL_size_in','value'),
        State('HGL_time_in','value'),
        State('HGL_vent_width','value'),
        State('HGL_vent_height','value'),
        State('HGL_room_width','value'),
        State('HGL_room_height','value'),
        State('HGL_room_length','value'),
        State('HGL_amb_temp','value'),
        State('HGL_wall_thickness','value'),
        State('HGL_thermal_cond','value'),
        State('HGL_cp','value'),
        State('HGL_density','value'),
    ]
)
def HGL_btn_execut(btn, size, tIn, vWidth, vHeight, rWidth, rHeight, rLength, aTemp, wThick, wCond, cp, dense):

    #------------------ESTABLISHING DEFINITIONS---------------------------------
    #eleven inputs without the button
    inList= [size, tIn, vWidth, vHeight, rWidth, rHeight, aTemp, wThick, wCond, cp, dense]

    #figure parameters
    HGL_data=[]
    HGL_layout = copy.deepcopy(plot_layout)

    #completion checks and error messaging
    HGL_state = 'TRUE'
    eMessage = ''



    #CALL INPUT CHECKING FUNCTION
    HGL_test_list = HGL_input_check(inList)

    #if HGL_test_list[0] and btn > 0:

    hrrs = np.arange(size + 1)

    #Thermal diffusivity
    alpha = wCond / (dense * cp)

    #Thermal penetration time
    t_p = wThick**2/(4*alpha)

    #Ventilation area
    A_o = vWidth * vHeight

    #Effective heat transfer coefficient
    if tIn < t_p:
        h_k = np.sqrt(wCond * dense * cp / tIn) / 1000
    elif tIn >= t_p:
        h_k = (wCond / wThick) / 1000

    A_T = (2 * rLength * rWidth) + (2 * rLength * rHeight) + (2 * rWidth * rHeight) - (A_o)

    Delta_T = 6.85 * (hrrs**2 / (A_o * np.sqrt(vHeight) * h_k * A_T))**(1/3)

    T_g = Delta_T + aTemp

    #--------------------PLOTTING CODE--------------------------------------

    try:
        HGL_data = [
            dict(
                type="scatter",
                mode="lines",
                x=hrrs,
                y=T_g,
                name="HGL Graph",
                opacity=1,
                hoverinfo="skip",
            )
        ]

        HGL_layout["title"] = f"HGL Temperature vs. HRR at {tIn} seconds"
        HGL_layout["showlegend"] = False
        HGL_layout["xaxis"] = {"title": {"text": "HRR (kW)"}}
        HGL_layout["yaxis"] = {"title": {"text": "HGL Temperature (C)"}}

        HGL_figure = dict(data=HGL_data, layout=HGL_layout)

    except:
        HGL_state = 'FALSE'
        HGL_figure = dict(data=HGL_data, layout=HGL_layout)


    HGL_String1 = f'{t_p} seconds'
    HGL_String2 = f'As a result, t >= t\u209A'
    HGL_String3 = f'{h_k} kW/m\u00b2'
    HGL_String4 = f'{A_T} m\u00b2'

    return 'The error', 'The result', HGL_figure, HGL_state, HGL_String1, HGL_String2, HGL_String3, HGL_String4


# @app.callback(
#     [
#         Output('HGL_eMessage','children'),
#         Output('HGL_sMessage','children'),
#         Output('HGL_graph','figure'),
#         Output('HGL_comp_state1','children'),
#     ],
#     [
#         Input('HGL_submit','n_clicks'),
#     ],
#     [
#         State('HGL_size_in','value'),
#         State('HGL_time_in','value'),
#         State('HGL_vent_width','value'),
#         State('HGL_vent_height','value'),
#         State('HGL_room_width','value'),
#         State('HGL_room_height','value'),
#         State('HGL_room_length','value'),
#         State('HGL_amb_temp','value'),
#         State('HGL_wall_thickness','value'),
#         State('HGL_thermal_cond','value'),
#         State('HGL_cp','value'),
#         State('HGL_density','value'),
#     ]
# )
# def HGL_btn_execut(btn, size, tIn, vWidth, vHeight, rWidth, rHeight, rLength, aTemp, wThick, wCond, cp, dense):
#
#     HGL_state = 'TRUE'
#     eMessage = ''
#     #ELEVEN INPUTS WITHOUT THE BUTTON
#     inList= [size, tIn, vWidth, vHeight, rWidth, rHeight, aTemp, wThick, wCond, cp, dense]
#
#     #CALL INPUT CHECKING FUNCTION
#     HGL_test_list = HGL_input_check(inList)
#
#     if HGL_test_list[0] and btn > 0:
#
#         hrrs = np.arange(size + 1)
#
#         #Thermal diffusivity
#         alpha = wThick / (dense * cp)
#
#         #Thermal penetration time
#         t_p = wThick**2/(4*alpha)
#
#         #Ventilation area
#         A_o = vWidth * vHeight
#
#         #Effective heat transfer coefficient
#         if tIn < t_p:
#             h_k = np.sqrt(wCond * dense * cp / t) / 1000
#         elif tIn >= t_p:
#             h_k = (wCond / wThick) / 1000
#
#         A_T = (2 * rLength * rWidth) + (2 * rLength * rHeight) + (2 * rWidth * rHeight) - (A_o)
#
#         Delta_T = 6.85 * (hrrs**2 / (A_o * np.sqrt(vHeight) * h_k * A_T))**(1/3)
#
#         T_g = Delta_T + T_inf
#
#     #--------------------PLOTTING CODE--------------------------------------
#     HGL_data=[]
#     HGL_layout = copy.deepcopy(plot_layout)
#
#     try:
#         data = [
#             dict(
#                 type="scatter",
#                 mode="lines",
#                 x=hrrs,
#                 y=T_g,
#                 name="HGL Graph",
#                 opacity=1,
#                 hoverinfo="skip",
#             )
#         ]
#
#         layout["title"] = f"HGL Temperature vs. HRR at {tIn} seconds"
#         layout["showlegend"] = False
#         layout["xaxis"] = {"title": {"text": "HRR (kW)"}}
#         layout["yaxis"] = {"title": {"text": "HGL Temperature (C)"}}
#
#         HGL_figure = dict(data=HGL_data, layout=HGL_layout)
#
#     except:
#         completion_state = 'FALSE'
#         HGL_figure = dict(data=HGL_data, layout=HGL_layout)
#
#         if completion_state == True:
#             return HGL_test_list[0], 'This is the complete message', HGL_figure, completion_state
#         else:
#             return HGL_test_list[0], 'This is the complete message', HGL_figure, completion_state
#
#     return 'The last', 'The filler', HGL_figure, HGL_state
#
