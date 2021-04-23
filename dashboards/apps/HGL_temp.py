import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output

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
                    className='pretty_container twelve columns'
                ),
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
                                    id='submit_cell',
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
                    className='pretty_container twelve columns'
                ),
            ],
            className= "row flex-display",
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
    ],
), #---------------------END LAYOUT--------------------------------------------
