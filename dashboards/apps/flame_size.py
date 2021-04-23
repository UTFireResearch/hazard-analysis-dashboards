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
                            'This tool calculates the flame height and plume centerline temperatures based on the correlations by Heskestad and McCaffrey.',
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.H6(
                            'Governing Equations',
                            style={'margin-left':'20px'}
                        ),
                        html.P(
                            'The flame height correlation by Heskestad is given by:',
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.Img(
                            src=('/assets/flame_eq1_mod.PNG'),
                            style={'height': '40px', 'margin-left': '20px'},
                        ),
                        html.P(
                            'The plume centerline temperature correlation by Heskestad is given by:',
                            style={"margin": "0px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.Img(
                            src=('/assets/flame_eq2_mod.PNG'),
                            style={'height': '40px', 'margin-left': '20px'},
                        ),
                        html.P(
                            'which is valid above the flame height.',
                            style={"margin": "0px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.P(
                            'The plume centerline temperature correlation by McCaffrey is given by:',
                            style={"margin": "0px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.Img(
                            src=('/assets/flame_eq3_mod.PNG'),
                            style={'height': '40px', 'margin-left': '20px'},
                        ),
                        html.P(
                            'which is valid above the flame height. The McCaffrey plume temperature correlation can be used in the intermittent and continuous flaming regions with other constants. For the sake of simplicity, only the plume region form of the correlation is used here.',
                            style={"margin": "0px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.P(
                            [
                            'Note: An ambient temperature (T',
                            html.Sub('\u221E'),
                            ') of 20',
                            html.Sup('\u00B0'),
                            'C is used.'
                            ],
                            style={"margin": "0px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.P(
                            [
                            'More information on the above equations can be found in the textbook',
                            html.I('Enclosure Fire Dynamics by Karlsson and Quintiere.')
                            ],
                            style={"margin": "0px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.H6(
                            'Characteristic Fire Size',
                            style={'margin-left':'20px'}
                        ),
                        html.P(
                            'Additionally, the characteristic fire size (or nondimensional heat release rate) is a useful quantity to relate the energy output of a fire to its physical diameter. Q* is calculated by:',
                            style={"margin": "0px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.Img(
                            src=('/assets/flame_eq4_mod.PNG'),
                            style={'height': '40px', 'margin-left': '20px'},
                        ),
                        html.P(
                            [
                            'The properties of air at standard temperature and pressure are used as \u03C1',
                            html.Sub('\u221E'),
                            ' = 1.204 kg/m',
                            html.Sup('3'),
                            ', c',
                            html.Sub('p'),
                            ' = 1.005 kJ/kg-K,',
                            ' T',
                            html.Sub('\u221E'),
                            ' = 293 K, and g = 9.81 m/s',
                            html.Sup('2'),
                            '. More details can be found in NUREG 1824.',
                            ],
                            style={"margin": "0px", "font-size": "20", "margin-left": "20px"}
                        ),

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
                                    'Fire Size: ',
                                    style={'margin-right':'35px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='flame_size_in',
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
                        #------------FIRE DIAMETER FIELD AND LABEL--------------
                        html.Div(
                            [
                                html.P(
                                    'Fire Diameter: ',
                                    style={'margin-right':'35px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='flame_diameter_in',
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
                        #-------MAXIMUM FIRE SIZE FIELD AND LABEL--------------
                        html.Div(
                            [
                                html.P(
                                    'Radiative Fraction: ',
                                    style={'margin-right':'35px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='flame_rad_frac',
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
                        #------------CALCULATE BUTTON--------------------------
                        html.Div(
                            [
                                html.Button(
                                    'Calculate Plume Characteristics >>',
                                    id='flame_calc_button',
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
