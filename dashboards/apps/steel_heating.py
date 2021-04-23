import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output

protList=['Unprotected','Protected']

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
                            'Steel Heating Under Fire Conditions',
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
                            'This tool calculates the lumped transient temperature of steel under fire conditions using standad time-temperature curves. You can select unprotected or protected steel, and various input parameters can be changed.',
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.P(
                            'The ISO 834 time-temperature curve is given by:',
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.Img(
                            src='/assets/steel_eq1_mod.PNG',
                            style={'height': '25px', 'margin-left': '20px'}
                        ),
                        html.P(
                            'The ASTM E119 time-temperature curve is approximated by:',
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.Img(
                            src='/assets/steel_eq2_mod.PNG',
                            style={'height': '25px', 'margin-left': '20px'}
                        ),
                        html.P(
                            'The rate of change temperature of the unprotected steel is given by:',
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.Img(
                            src='/assets/steel_eq3_mod.PNG',
                            style={'height': '25px', 'margin-left': '20px'}
                        ),
                        html.P(
                            'The rate of change temperature of the protected steel is given by:',
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.Img(
                            src='/assets/steel_eq4_mod.PNG',
                            style={'height': '25px', 'margin-left': '20px'}
                        ),

                    ],
                    className='pretty_container twelve columns'
                ),
            ],
            className= "row flex-display",
        ),
        #----------------MIDDLE INPUTS FLEX ROW--------------------------------
        #----------------START MIDDLE INPUT FLEX ROW---------------------------
        html.Div(
            [
                html.Div(
                    [   html.H5(
                            html.B('Enter Input Parameters'),
                            style={"margin-bottom": "15px", "color": "maroon"},
                        ),
                        #----------SIMULATION TIME FIELD AND LABEL--------------
                        html.Div(
                            [
                                html.P(
                                    'Simulation Time: ',
                                    style={'margin-right':'35px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='steel_sim_time',
                                type='number',
                                placeholder='hr',
                                size='15',
                                ),
                                html.P(
                                    'hours',
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
                            'Steel Parameters',
                            style={'margin-left':'20px'}
                        ),
                        #-----------SECTION FACTOR FIELD AND LABEL--------------
                        html.Div(
                            [
                                html.P(
                                    'Section Factor: ',
                                    style={'margin-right':'51px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='steel_section_factor',
                                type='number',
                                placeholder='1/m',
                                size='15',
                                ),
                                html.P(
                                    '1/m',
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
                        #---------------DENSITY FIELD AND LABEL-----------------
                        html.Div(
                            [
                                html.P(
                                    'Density: ',
                                    style={'margin-right':'97px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='steel_density',
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
                        #------------SPECIFIC HEAT FIELD AND LABEL--------------
                        html.Div(
                            [
                                html.P(
                                    'Specific Heat: ',
                                    style={'margin-right':'60px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='steel_cp',
                                type='number',
                                placeholder='J/kg-K',
                                size='15',
                                ),
                                html.P(
                                    'J/kg-K',
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
                        #--------------EMMISSIVITY FIELD AND LABEL--------------
                        html.Div(
                            [
                                html.P(
                                    'Emissivity: ',
                                    style={'margin-right':'80px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='steel_emissive',
                                type='number',
                                placeholder='',
                                size='15',
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
                            'Fire Parameters',
                            style={'margin-left':'20px'}
                        ),
                        #--------------FIRE CURVE FIELD AND LABEL---------------
                        html.Div(
                            [
                                html.P(
                                    'Fire Curve: ',
                                    style={'margin-right':'105px', 'margin-top': '5px'}
                                ),
                                html.Div(
                                    dcc.Dropdown(
                                    id='steel_protected',
                                    options=
                                    [
                                        {'label': 'ISO 834', 'value': '834'},
                                        {'label': 'ASTM E119', 'value': 'E119'}
                                    ],
                                    ),
                                    style={'width':'150px'}
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
                        #------HEAT TRANSFER COEFFICIENT FIELD AND LABEL--------
                        html.Div(
                            [
                                html.P(
                                    'Heat Transfer Coefficient: ',
                                    style={'margin-right':'10px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='steel_transfer_coeff',
                                type='number',
                                placeholder='W/m^2-K',
                                size='15',
                                ),
                                html.P(
                                    'W/m^2-K',
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
                            'Insulation Parameters',
                            style={'margin-left':'20px'}
                        ),
                        #--------------INSULATION FIELD AND LABEL---------------
                        html.Div(
                            [
                                html.P(
                                    'Steel Protection?: ',
                                    style={'margin-right':'38px', 'margin-top': '5px'}
                                ),
                                html.Div(
                                    dcc.Dropdown(
                                    id='steel_protected',
                                    options=
                                    [
                                        {'label': 'Unprotected', 'value': 'False'},
                                        {'label': 'Protected', 'value': 'True'}
                                    ],
                                    ),
                                    style={'width':'150px'}
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
                        html.P(
                            'If protected steel, then input the following: ',
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
                        ),
                        #--------------THICKNESS FIELD AND LABEL----------------
                        html.Div(
                            [
                                html.P(
                                    'Thickness: ',
                                    style={'margin-right':'80px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='steel_thickness',
                                type='number',
                                placeholder='m',
                                size='15',
                                ),
                                html.P(
                                    'm',
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
                                html.P(
                                    'Thermal Conductivity: ',
                                    style={'margin-right':'10px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='steel_conductivity',
                                type='number',
                                placeholder='W/m-K',
                                size='15',
                                ),
                                html.P(
                                    'W/m-K',
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
                        #----------PROTECTED DENSITY FIELD AND LABEL-----------------
                        html.Div(
                            [
                                html.P(
                                    'Density: ',
                                    style={'margin-right':'97px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='steel_protected_density',
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
                        #------PROTECTED SPECIFIC HEAT FIELD AND LABEL----------
                        html.Div(
                            [
                                html.P(
                                    'Specific Heat: ',
                                    style={'margin-right':'60px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='steel_protected_cp',
                                type='number',
                                placeholder='J/kg-K',
                                size='15',
                                ),
                                html.P(
                                    'J/kg-K',
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
                                    'Calculate Transient Steel Temperature >>',
                                    id='submit_steel',
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
    ]
), #---------------------END LAYOUT--------------------------------------------
