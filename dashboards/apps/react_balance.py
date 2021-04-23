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
                            'Chemical Reaction Balancer',
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
                            'This tool balances a combustion chemical reaction with an option to include a specified soot or CO yield. The chemical reaction is of the following general form:',
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
                        ),
                        html.Img(
                            src=('/assets/Chem_eq1_mod.PNG'),
                            style={'height': '60px', 'margin-left': '15px'},
                        ),
                        html.P(
                            'Input the chemical formula of the fuel, and (optionally) specify a soot or CO yield. Supported fuel atoms are C,H,O,N. For example, enter CH4 for methane or C3H8 for propane.',
                            style={"margin": "10px", "font-size": "20", "margin-left": "20px"}
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

                        #-------MAXIMUM FIRE SIZE FIELD AND LABEL--------------
                        html.Div(
                            [
                                html.P(
                                    'Chemical Formula of Fuel: ',
                                    style={'margin-right':'55px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='chem_fuel_formula',
                                placeholder='e.g. C3H8',
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
                        #---------CARBON MONOXIDE YIELD FIELD AND LABEL---------
                        html.Div(
                            [
                                html.P(
                                    'Carbon Monoxide Yield: ',
                                    style={'margin-right':'80px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='react_CO_yield',
                                type='number',
                                placeholder='kg/kg',
                                size='15',
                                ),
                                html.P(
                                    'kgkg',
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
                        #-------------SOOT YIELD FIELD AND LABEL----------------
                        html.Div(
                            [
                                html.P(
                                    'Soot Yield: ',
                                    style={'margin-right':'160px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='react_soot_yield',
                                type='number',
                                placeholder='kgkg',
                                size='15',
                                ),
                                html.P(
                                    'kgkg',
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
                        #--------HYDROGEN SOOT FRACTION FIELD AND LABEL---------
                        html.Div(
                            [
                                html.P(
                                    'Hydrogen Atomic Fraction in Soot: ',
                                    style={'margin-right':'10px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='react_hydrogen_fraction',
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
                            'Volume Fractions of Background Species:',
                            style={'margin-left':'20px'}
                        ),
                        #-----------FUEL FRACTION FIELD AND LABEL---------------
                        html.Div(
                            [
                                html.P(
                                    'Fuel: ',
                                    style={'margin-right':'90px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='react_fuel_frac',
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
                        #-----------OXYGEN FRACTION FIELD AND LABEL-------------
                        html.Div(
                            [
                                html.P(
                                    [
                                    'O',
                                    html.Sub('2'),
                                    ': ',
                                    ],
                                    style={'margin-right':'95px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='react_O2_frac',
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
                        #-----------NITROGEN FRACTION FIELD AND LABEL-----------
                        html.Div(
                            [
                                html.P(
                                    [
                                    'N',
                                    html.Sub('2'),
                                    ': ',
                                    ],
                                    style={'margin-right':'95px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='react_N2_frac',
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
                        #-----------WATER FRACTION FIELD AND LABEL--------------
                        html.Div(
                            [
                                html.P(
                                    [
                                    'H',
                                    html.Sub('2'),
                                    'O: ',
                                    ],
                                    style={'margin-right':'95px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='react_H2O_frac',
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
                        #--------CARBON DIOXIDE FRACTION FIELD AND LABEL--------
                        html.Div(
                            [
                                html.P(
                                    [
                                    'CO',
                                    html.Sub('2'),
                                    ': ',
                                    ],
                                    style={'margin-right':'95px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='react_CO2_frac',
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
                        #-------CARBON MONOXIDE FRACTION FIELD AND LABEL--------
                        html.Div(
                            [
                                html.P(
                                    'CO:',
                                    style={'margin-right':'95px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='react_CO_frac',
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
                        #-----------SOOT FRACTION FIELD AND LABEL-------------
                        html.Div(
                            [
                                html.P(
                                    'Soot:',
                                    style={'margin-right':'95px', 'margin-top': '5px'}
                                ),
                                dcc.Input(
                                id='react_soot_frac',
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
                        dcc.Checklist(
                            options=[
                                {'label': 'Print extra decimal precision', 'value': 'precise'},
                            ],
                            value=[],
                            labelStyle={
                            'display': 'inline-block',
                            "margin-left": "20px",
                            "margin-bottom": "20px"
                            }
                        ),
                        html.Button(
                            'Balance Chemical Equation',
                            id='react_calculate_button',
                            style={
                                "margin-left": "20px",
                            },
                            n_clicks=0,
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
