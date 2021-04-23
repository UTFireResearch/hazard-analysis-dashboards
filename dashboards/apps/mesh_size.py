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
                            'FDS Mesh Size Calculator',
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
                        html.H6(
                            html.B('About This Tool'),
                            style={"margin-left": "20px"}
                        ),
                        html.P(
                            'This tool allows you to easily generate a MESH line for input into FIRE dynamics Simulator (FDS). It automatically calculates the optimal (Poison-friendly mesh division numbers and returns a complest MESH line to be used in an FDS input file. The cell sizes are determined using the characteristic fire diameter and cell size ratio that should accurately resolve your fire simulation based on the total heat release rate.',
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.H6(
                            html.B('Background'),
                            style={"margin-left": "20px"}
                        ),
                        html.P(
                            'The cell size (dx) for a given simulation can be related to the characteristic fire diameter (D*), i.e., the smaller the characteristic fire diameter, the smaller the cell size should be in order to adequatey resolve the fluid flow and fire dynamics.',
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.P(
                            'The characteristic fire diameter (D*) is given by the following relationship:',
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.Img(
                            src=('/assets/mesh_eq1_mod.PNG'),
                            style={'height': '100px', 'margin-left': '20px'}
                        ),
                        html.P(
                            'A reference within the FDS User Guide (Verification and Validation of Selected Fire Models for Nuclear power Plant Applications. NUREG 1824, United States Nuclear Regulatory Commission, 2007) used a D*/dx ratio between 4 and 16 to accurately resolve fires in various scenarios. From the FDS User Guide: "These values were used to adequately resolve plume dynamics, along with other geometrical characteristics of the models as well. This range does not indicate what values to use for all models, only what values worked well for that particular set of models."',
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
                        ),
                    ],
                    className='pretty_container twelve columns'
                ),
            ],
            className= "row flex-display",
        ),
        #----------------MIDDLE INPUTS FLEX ROW--------------------------------
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            'NOTE: You should always perform a grid sensitivity analysis and verify the grid resolution yourself. This calculator should only be used as a guide / rule of thumb!',
                            style={'color': 'red', 'margin-left':'20px', 'margin-bottom': '10px'},
                        ),
                        html.H6(
                            'Enter the x,y,z dimensions (meters) and your expected HRR',
                            style={'margin-left':'20px'}
                        ),
                        html.Div(
                            [
                                html.P(
                                    [
                                        'X',
                                        html.Sub('min')
                                    ],
                                    style={'margin-right': '5px'}
                                ),
                                dcc.Input(
                                id='X_min',
                                type='number',
                                placeholder='meters',
                                style={'margin-left': '5px'},
                                size='15',
                                ),
                                html.P(
                                    [
                                        'X',
                                        html.Sub('max')
                                    ],
                                    style={'margin-right': '5px', 'margin-left': '10px'}
                                ),
                                dcc.Input(
                                id='X_max',
                                type='number',
                                placeholder='meters',
                                style={'margin-left': '5px'},
                                size='15',
                                ),
                            ],
                            className="row flex-display",
                            style={'margin-left':'20px'}
                        ),
                        html.Div(
                            [
                                html.P(
                                    [
                                        'Y',
                                        html.Sub('min')
                                    ],
                                    style={'margin-right': '5px'}
                                ),
                                dcc.Input(
                                id='Y_min',
                                type='number',
                                placeholder='meters',
                                style={'margin-left': '5px'},
                                size='15',
                                ),
                                html.P(
                                    [
                                        'Y',
                                        html.Sub('max')
                                    ],
                                    style={'margin-right': '5px', 'margin-left': '10px'}
                                ),
                                dcc.Input(
                                id='Y_max',
                                type='number',
                                placeholder='meters',
                                style={'margin-left': '5px'},
                                size='15',
                                ),
                            ],
                            className="row flex-display",
                            style={'margin-left':'20px'}
                        ),
                        html.Div(
                            [
                                html.P(
                                    [
                                        'Z',
                                        html.Sub('min')
                                    ],
                                    style={'margin-right': '5px'}
                                ),
                                dcc.Input(
                                id='Z_min',
                                type='number',
                                placeholder='meters',
                                style={'margin-left': '5px'},
                                size='15',
                                ),
                                html.P(
                                    [
                                        'Z',
                                        html.Sub('max')
                                    ],
                                    style={'margin-right': '5px', 'margin-left': '10px'}
                                ),
                                dcc.Input(
                                id='Z_max',
                                type='number',
                                placeholder='meters',
                                style={'margin-left': '7px'},
                                size='15',
                                ),
                            ],
                            className="row flex-display",
                            style={'margin-left':'20px'}
                        ),
                        html.Div(
                            [
                                html.P(
                                    'Requested cell size (dx, dy, dz):',
                                    style={'margin-right':'40px'},
                                ),
                                dcc.Input(
                                id='cell_size',
                                type='text',
                                placeholder='',
                                size='15'
                                ),
                            ],
                            className="row flex-display",
                            style={
                                'margin-left':'20px',
                                'margin-top':'10px',
                                'margin-bottom': '10px',
                            }
                        ),
                        #-----------MESH LINE CALCULATE BUTTON------------------
                        html.Div(
                            [
                                html.Button(
                                    'Calculate MESH Line',
                                    id='submit_mesh',
                                    style={
                                    "margin-left": '2px',
                                    "margin-bottom": '15px',
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
                        #-----------------HRR INPUT ROW-------------------------
                        html.Div(
                            [
                                html.P(
                                    'Heat Release Rate (Q): ',
                                    style={'margin-right':'35px'}
                                ),
                                dcc.Input(
                                id='mesh_HRR_in',
                                type='number',
                                placeholder='kW',
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
                        #--------------DENSITY INPUT ROW-----------------------
                        html.Div(
                            [
                                html.P(
                                    [
                                        'Density (P',
                                        html.Sub('\u221E'),
                                        '): ',
                                    ],
                                    style={'margin-right':'105px'}
                                ),
                                dcc.Input(
                                id='mesh_desnity_in',
                                type='number',
                                placeholder='kW/m^3',
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
                        #--------------SPECIFIC HEAT INPUT ROW-----------------
                        html.Div(
                            [
                                html.P(
                                    [
                                        'Specific heat (C',
                                        html.Sub('p'),
                                        '): ',
                                    ],
                                    style={'margin-right':'72px'}
                                ),
                                dcc.Input(
                                id='mesh_CP_in',
                                type='number',
                                placeholder='kg / m^3',
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
                        #------------AMBIENT TEMP INPUT ROW--------------------
                        html.Div(
                            [
                                html.P(
                                    [
                                        'Ambient Temperature (T',
                                        html.Sub('\u221E'),
                                        '): ',
                                    ],
                                    style={'margin-right':'17px'}
                                ),
                                dcc.Input(
                                id='mesh_T_in',
                                type='number',
                                placeholder='K',
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
                        #------------GRAVITY INPUT ROW-------------------------
                        html.Div(
                            [
                                html.P(
                                    [
                                        'Gravity (g):',
                                    ],
                                    style={'margin-right':'120px'}
                                ),
                                dcc.Input(
                                id='mesh_g_in',
                                type='number',
                                placeholder='m/s^2',
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
                        html.Div(
                            [
                                html.Button(
                                    'Calculate Suggested Cell Sizes >>',
                                    id='submit_cell',
                                    style={
                                    "margin-left": '2px',
                                    "margin-bottom": '15px',
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
    ]
), #---------------------END LAYOUT--------------------------------------------
