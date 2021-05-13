import numpy as np
import dash_core_components as dcc
import dash_html_components as html
#import dash_bootstrap_components as dbc
#import dash_table
import re

from dash.dependencies import Input, Output, State
from app import app

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
                                    id='react_fuel_formula',
                                    placeholder='e.g. C3H8',
                                    size='15',
                                    value='C3H8',   #---------REMOVE ME!!!!! (MAYBE)
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
                                    value=0,    #-------------REMOVE ME!!!!!!! (MAYBE)
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
                                    value=0,    #-------------REMOVE ME!!!!!!! (MAYBE)
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
                                    value=0,    #--------------REMOVE ME!!!!!!!! (MAYBE)
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
                                    value=0,    #-------------REMOVE ME!!!!!!!!! (MAYBE)
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
                                    value=0.208,    #-------------REMOVE ME!!!!!!!!!! (MAYBE)
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
                                    value=0.783,    #-------------REMOVE ME!!!!!!!! (MAYBE)
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
                                    value=0.00834,    #-----------REMOVE ME!!!!!!! (MAYBE)
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
                                    value=0.00038,    #---------REMOVE ME!!!!!! (MAYBE)
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
                                    value=0.00,    #---------REMOVE ME!!!!!! (MAYBE)
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
                                    value=0.00,    #----------REMOVE ME!!!!!! (MAYBE)
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
                            id='react_precise',
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
                            id='react_calc_btn',
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
        html.Div(
            [
                #-------------RESULTS PRETTY CONTAINER--------------------------
                html.Div(
                    [
                        # html.P(id='react_eMessage'),
                        # html.P(id='react_placeholder'),
                        html.H5(
                            'Reactants:',
                            style={'margin-left':'15px'},
                        ),
                        html.Div(
                            [
                                html.H6(
                                    id='r_fuelC',
                                    style={'display':'inline-block','color':'red'},
                                ),
                                html.H6(
                                    id='r_fuel',
                                    style={'display':'inline-block', 'color':'black', 'padding-right':'5px'},
                                ),
                                html.H6(
                                    '+',
                                    style={'display':'inline-block','color':'black', 'padding-right':'5px'},
                                ),
                                html.H6(
                                    id='r_groupBC',
                                    style={'display':'inline-block', 'color':'red', 'padding-right':'5px'},
                                ),
                                html.H6(
                                    '(',
                                    style={'display':'inline-block', 'color':'black'},
                                ),
                                html.H6(
                                    id='r_O2',
                                    style={'display': 'inline-block', 'color': 'blue'},
                                ),
                                html.H6(
                                    'O\u2082',
                                    style={'display': 'inline-block', 'color': 'black', 'padding-right':'5px'},
                                ),
                                html.H6(
                                    '+',
                                    style={'display': 'inline-block', 'color': 'black', 'padding-right':'5px'},
                                ),
                                html.H6(
                                    id='r_N2',
                                    style={'display': 'inline-block', 'color': 'blue'},
                                ),
                                html.H6(
                                    'N\u2082',
                                    style={'display': 'inline-block', 'color': 'black', 'padding-right':'5px'},
                                ),
                                html.H6(
                                    '+',
                                    style={'display': 'inline-block', 'color': 'black', 'padding-right':'5px'},
                                ),
                                html.H6(
                                    id='r_H2O',
                                    style={'display': 'inline-block', 'color': 'blue'},
                                ),
                                html.H6(
                                    'H\u2082O',
                                    style={'display': 'inline-block', 'color': 'black', 'padding-right':'5px'},
                                ),
                                html.H6(
                                    '+',
                                    style={'display': 'inline-block', 'color': 'black', 'padding-right':'5px'},
                                ),
                                html.H6(
                                    id='r_CO2',
                                    style={'display': 'inline-block', 'color': 'blue'},
                                ),
                                html.H6(
                                    'CO\u2082',
                                    style={'display': 'inline-block', 'color': 'black'},
                                ),
                                html.H6(
                                    ')',
                                    style={'display': 'inline-block', 'color': 'black'},
                                )
                            ],
                            style={'margin-left':'15px'},
                        ),
                        html.H5(
                            'Products:',
                            style={'margin-left':'15px'},
                        ),
                        html.Div(
                            [
                                html.H6(
                                    id='p_groupBC',
                                    style={'display': 'inline-block', 'color': 'red', 'padding-right':'5px'},
                                ),
                                html.H6(
                                    '(',
                                    style={'display': 'inline-block', 'color': 'black'},
                                ),
                                html.H6(
                                    id='p_N2',
                                    style={'display': 'inline-block', 'color': 'blue'},
                                ),
                                html.H6(
                                    'N\u2082',
                                    style={'display': 'inline-block', 'color': 'black', 'padding-right':'5px'},
                                ),
                                html.H6(
                                    '+',
                                    style={'display': 'inline-block', 'color': 'black', 'padding-right':'5px'},
                                ),
                                html.H6(
                                    id='p_H2O',
                                    style={'display': 'inline-block', 'color': 'blue'},
                                ),
                                html.H6(
                                    'H\u2082O',
                                    style={'display': 'inline-block', 'color': 'black'},
                                ),
                                html.H6(
                                    '+',
                                    style={'display': 'inline-block', 'color': 'black', 'padding-right':'5px'},
                                ),
                                html.H6(
                                    id='p_CO2',
                                    style={'display': 'inline-block', 'color': 'blue'},
                                ),
                                html.H6(
                                    'CO\u2082',
                                    style={'display': 'inline-block', 'color': 'black'},
                                ),
                                html.H6(
                                    ')',
                                    style={'display': 'inline-block', 'color': 'black'},
                                ),
                            ],
                            style={'margin-left':'15px'}
                        ),
                    ],
                    className='pretty_container twelve columns',
                )
            ],
            className='row flex-display',
        ),
        #----------------BOTTOM ACKNOWLEDGEMENTS ROW----------------------------
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
), #---------------------END LAYOUT---------------------------------------------

#-------------------NON-CALLBACK FUNCTIONS
def parse_formula(formula):

    C, H, O, N = 0, 0, 0, 0

    # Search for C, H, O, N atoms in formula
    match = re.search('[cC](\d+\.?\d*)', formula)
    if match:
        C = match.group(1)
    match = re.search('[hH](\d+\.?\d*)', formula)
    if match:
        H = match.group(1)
    match = re.search('[oO](\d+\.?\d*)', formula)
    if match:
        O = match.group(1)
    match = re.search('[nN](\d+\.?\d*)', formula)
    if match:
        N = match.group(1)

    # If an atom is included with no number following,
    # then assign it a value of 1
    if (C == 0) and ('C' in formula):
        C = 1
    if (H == 0) and ('H' in formula):
        H = 1
    if (O == 0) and ('O' in formula):
        O = 1
    if (N == 0) and ('N' in formula):
        N = 1

    # Convert all atom numbers to floats
    C = float(C)
    H = float(H)
    O = float(O)
    N = float(N)

    oList = [C,H,O,N]

    if ((C == 0) or (H == 0)):
        return 'C and H must be included in the fuel formula.', oList

    else:
        return '', oList


@app.callback(
    [
        #Output('react_comp_state','children'),
        Output('r_fuelC','children'),
        Output('r_fuel','children'),
        Output('r_groupBC','children'),
        Output('r_O2','children'),
        Output('r_N2','children'),
        Output('r_H2O','children'),
        Output('r_CO2','children'),
        Output('p_groupBC','children'),
        Output('p_N2','children'),
        Output('p_H2O','children'),
        Output('p_CO2','children'),
    ],
    [
        Input('react_calc_btn','n_clicks'),
    ],
    [
        State('react_fuel_formula','value'),
        State('react_CO_yield','value'),
        State('react_soot_yield','value'),
        State('react_hydrogen_fraction','value'),

        State('react_fuel_frac','value'),
        State('react_O2_frac','value'),
        State('react_N2_frac','value'),
        State('react_H2O_frac','value'),
        State('react_CO2_frac','value'),
        State('react_CO_frac','value'),
        State('react_soot_frac','value')
    ]
)
def test_call(btn, formula, y_CO, y_s, X_H, bg_1, bg_2, bg_3, bg_4, bg_5, bg_6, bg_7):

    #================================
    # = Establish constant parameters
    #================================

    # Molecular weights of C, H, O, N
    MW_C = 12.0107
    MW_H = 1.00794
    MW_O = 15.9994
    MW_N = 14.0067

    i_fuel            = 0
    i_oxygen          = 1
    i_nitrogen        = 2
    i_water_vapor     = 3
    i_carbon_dioxide  = 4
    i_carbon_monoxide = 5
    i_soot            = 6

    if btn > 0:

        #Parse the text formula and output a list with coefficients [C, H, O, N]
        message, coList = parse_formula(formula)

        C = coList[0]
        H = coList[1]
        O = coList[2]
        N = coList[3]

        E = np.matrix([[C, 0, 0, 0, 1, 1, (1-X_H)],              # C
                       [H, 0, 0, 2, 0, 0, X_H    ],              # H
                       [O, 2, 0, 1, 2, 1, 0      ],              # O
                       [N, 0, 2, 0, 0, 0, 0]     ], dtype=float) # N

        MW = np.matrix([MW_C, MW_H, MW_O, MW_N]) # primitive species molecular weights

        W = E.T * MW.T

        v_0 = np.matrix([bg_1, bg_2, bg_3, bg_4, bg_5, bg_6, bg_7], dtype=float)
        v_0 = v_0/np.sum(v_0) # normalize

        v_1 = np.matrix([1, 0, 0, 0, 0, 0, 0], dtype=float)
        v_1 = v_1/np.sum(v_1) # normalize

        v_2 = np.matrix([0, 0, 0, 0, 0, 0, 0], dtype=float)

        v_2[0,i_carbon_monoxide] = W.item(i_fuel) / W.item(i_carbon_monoxide) * y_CO
        v_2[0,i_soot]            = W.item(i_fuel) / W.item(i_soot) * y_s

        b = E * (v_1.T - v_2.T)

        L = np.column_stack([E*v_0.T, E[:,i_carbon_dioxide], E[:,i_water_vapor], E[:,i_nitrogen]])

        x = np.linalg.inv(L)*b

        nu_0                    = x.item(0) # background stoichiometric coefficient
        v_2.T[i_carbon_dioxide] = x.item(1)
        v_2.T[i_water_vapor]    = x.item(2)
        v_2.T[i_nitrogen]       = x.item(3)

        nu_1 = -1 # fuel stoich coeff
        nu_2 = np.sum(v_2) # prod stoich coeff

        v_2 = v_2/nu_2 # normalize volume fractions

        Z2Y = np.row_stack([v_0, v_1, v_2])

        Z2Y = Z2Y.T

        coeff_fuel = Z2Y[0,1] # Fuel

        coeff_lhs_1 = Z2Y[0,0] # Fuel
        coeff_lhs_2 = Z2Y[1,0] # O2
        coeff_lhs_3 = Z2Y[2,0] # N2
        coeff_lhs_4 = Z2Y[3,0] # H2O
        coeff_lhs_5 = Z2Y[4,0] # CO2
        coeff_lhs_6 = Z2Y[5,0] # CO
        coeff_lhs_7 = Z2Y[6,0] # C

        coeff_rhs_1 = Z2Y[0,2] # Fuel
        coeff_rhs_2 = Z2Y[1,2] # O2
        coeff_rhs_3 = Z2Y[2,2] # N2
        coeff_rhs_4 = Z2Y[3,2] # H2O
        coeff_rhs_5 = Z2Y[4,2] # CO2
        coeff_rhs_6 = Z2Y[5,2] # CO
        coeff_rhs_7 = Z2Y[6,2] # C

        #Formulate the parenthetical string
        cStrFuel = f'{coeff_fuel:.2f} '
        cStrPBlock = f'{abs(nu_0):.2f} '
        rO2_str = f'{coeff_lhs_2:.2f} '
        rN2_str = f'{coeff_lhs_3:.2f} '
        rH20_str = f'{coeff_lhs_4:.2f} '
        rCO2_str = f'{coeff_lhs_5:.2f} '

        pStrBlock = f'{abs(nu_2):.2f} '
        pN2_str = f'{coeff_rhs_3:.2f} '
        pH2O_str = f'{coeff_rhs_4:.2f} '
        pCO2_str = f'{coeff_rhs_5:.2f} '

        return cStrFuel, formula, cStrPBlock, rO2_str, rN2_str, rH20_str, rCO2_str, pStrBlock, pN2_str, pH2O_str, pCO2_str

    else:
        return '','','','','','','','','','',''

#-------------------CALLBACKS SECTION-------------------------------------------
# @app.callback(
#     [
#         Output('react_eMessage','children'),
#         Output('react_placeholder','children'),
#     ],
#     [
#         Input('react_calc_btn','n_clicks'),
#     ],
#     [
#         State('chem_fuel_formula','value'),
#         State('react_CO_yield','value'),
#         State('react_soot_yield','value'),
#         State('react_hydrogen_fraction','value'),
#         State('react_fuel_frac','value'),
#         State('react_O2_frac','value'),
#         State('react_N2_frac','value'),
#         State('react_H2O_frac','value'),
#         State('react_CO2_frac','value'),
#         State('react_CO_frac','value'),
#         State('react_soot_frac','value'),
#         State('react_precise','value'),
#     ]
# )
# def react_primary_exectue(btn, formula, y_CO, y_s, x_H, fuel, O2, N2, H2O, CO2, CO, soot_frac, precise):
#
#     if btn > 0:
#         message1 = ''
#         message2 = ''
#
#         #============================================
#         # = Prepping input parameters
#         #============================================
#         bg_1 = float(fuel)
#         bg_2 = float(O2)
#         bg_3 = float(N2)
#         bg_4 = float(H2O)
#         bg_5 = float(CO2)
#         bg_6 = float(CO)
#         bg_7 = float(soot_frac)
#
#         #============================================
#         # = Parsing chemical formula =
#         #============================================
#
#         C, H, O, N = 0, 0, 0, 0
#
#         # Search for C, H, O, N atoms in formula
#         match = re.search('[cC](\d+\.?\d*)', formula)
#         if match:
#             C = match.group(1)
#         match = re.search('[hH](\d+\.?\d*)', formula)
#         if match:
#             H = match.group(1)
#         match = re.search('[oO](\d+\.?\d*)', formula)
#         if match:
#             O = match.group(1)
#         match = re.search('[nN](\d+\.?\d*)', formula)
#         if match:
#             N = match.group(1)
#
#         # If an atom is included with no number following,
#         # then assign it a value of 1
#         if (C == 0) and ('C' in formula):
#             C = 1
#         if (H == 0) and ('H' in formula):
#             H = 1
#         if (O == 0) and ('O' in formula):
#             O = 1
#         if (N == 0) and ('N' in formula):
#             N = 1
#
#         # Convert all atom numbers to floats
#         C = float(C)
#         H = float(H)
#         O = float(O)
#         N = float(N)
#
#         # if ((C == 0) or (H == 0)):
#         #     return 'C and H must be included in the fuel formula.', ''
#
#         #----------TEST STOP 1----------------------------
#         message1 = 'Test stop 1 - st1'
#         message2 = 'Test stop 2 - st2'
#
#         return message1, message2
#
#     else:
#         return 'Fail', 'Fail'
#
#     # #=================================================
#     # # = Chemical equation balancing calculations =
#     # #=================================================
#     #
#     # # Molecular weights of C, H, O, N
#     # MW_C = 12.0107
#     # MW_H = 1.00794
#     # MW_O = 15.9994
#     # MW_N = 14.0067
#     #
#     # # define the element matrix (number of atoms [rows] for each primitive species [columns])
#     #
#     # i_fuel            = 0
#     # i_oxygen          = 1
#     # i_nitrogen        = 2
#     # i_water_vapor     = 3
#     # i_carbon_dioxide  = 4
#     # i_carbon_monoxide = 5
#     # i_soot            = 6
#     #
#     # E = np.matrix([[C, 0, 0, 0, 1, 1, (1-X_H)],              # C
#     #                [H, 0, 0, 2, 0, 0, X_H    ],              # H
#     #                [O, 2, 0, 1, 2, 1, 0      ],              # O
#     #                [N, 0, 2, 0, 0, 0, 0]     ], dtype=float) # N
#     #
#     # MW = np.matrix([MW_C, MW_H, MW_O, MW_N]) # primitive species molecular weights
#     #
#     # W = E.T * MW.T
#     #
#     # # define the volume fractions of the background and fuel
#     #
#     # v_0 = np.matrix([bg_1, bg_2, bg_3, bg_4, bg_5, bg_6, bg_7], dtype=float)
#     # v_0 = v_0/np.sum(v_0) # normalize
#     #
#     # # print v_0
#     #
#     # v_1 = np.matrix([1, 0, 0, 0, 0, 0, 0], dtype=float)
#     # v_1 = v_1/np.sum(v_1) # normalize
#     #
#     # # the reaction coefficients for the product primitive species temporarily stored in v_2
#     #
#     # v_2 = np.matrix([0, 0, 0, 0, 0, 0, 0], dtype=float)
#     #
#     # # compute what we know so far
#     #
#     # v_2[0,i_carbon_monoxide] = W.item(i_fuel) / W.item(i_carbon_monoxide) * y_CO
#     # v_2[0,i_soot]            = W.item(i_fuel) / W.item(i_soot) * y_s
#     #
#     # # linear system right hand side
#     #
#     # b = E * (v_1.T - v_2.T)
#     #
#     # # matrix
#     #
#     # L = np.column_stack([E*v_0.T, E[:,i_carbon_dioxide], E[:,i_water_vapor], E[:,i_nitrogen]])
#     #
#     # # solve the system
#     #
#     # x = np.linalg.inv(L)*b
#     #
#     # nu_0                    = x.item(0) # background stoichiometric coefficient
#     # v_2.T[i_carbon_dioxide] = x.item(1)
#     # v_2.T[i_water_vapor]    = x.item(2)
#     # v_2.T[i_nitrogen]       = x.item(3)
#     #
#     # nu_1 = -1 # fuel stoich coeff
#     # nu_2 = np.sum(v_2) # prod stoich coeff
#     #
#     # v_2 = v_2/nu_2 # normalize volume fractions
#     #
#     # # display fuel properties
#     #
#     # Z2Y = np.row_stack([v_0, v_1, v_2])
#     #
#     # Z2Y = Z2Y.T
#     #
#     # coeff_fuel = Z2Y[0,1] # Fuel
#     #
#     # coeff_lhs_1 = Z2Y[0,0] # Fuel
#     # coeff_lhs_2 = Z2Y[1,0] # O2
#     # coeff_lhs_3 = Z2Y[2,0] # N2
#     # coeff_lhs_4 = Z2Y[3,0] # H2O
#     # coeff_lhs_5 = Z2Y[4,0] # CO2
#     # coeff_lhs_6 = Z2Y[5,0] # CO
#     # coeff_lhs_7 = Z2Y[6,0] # C
#     #
#     # coeff_rhs_1 = Z2Y[0,2] # Fuel
#     # coeff_rhs_2 = Z2Y[1,2] # O2
#     # coeff_rhs_3 = Z2Y[2,2] # N2
#     # coeff_rhs_4 = Z2Y[3,2] # H2O
#     # coeff_rhs_5 = Z2Y[4,2] # CO2
#     # coeff_rhs_6 = Z2Y[5,2] # CO
#     # coeff_rhs_7 = Z2Y[6,2] # C
#     #
#     # return str(coeff_lhs_2), coeff_lhs_3
#
#     # #==============================================
#     # # = Output generation
#     # #==============================================
#     # coeff_string = [coeff_lhs2 != 0, coeff_lhs_3 != 0, coeff_lhs_4 != 0, coeff_lhs_5 != 0, coeff_lhs_6 != 0, coeff_lhs_7 != 0]
#     #
#     #
#     # bString = '('
#     #
#     # if coeff_lhs_2 != 0:
#     #     bString += '{coeff_lhs_2}O\u2082'
#     #     if any(coeff_string[1:]):
#     #         bString += '+'
#     #
#     # if coeff_lhs_3 != 0:
#     #     bString += '{coeff_lhs_3}N\u2082'
#     #     if any(coeff_string[2:]):
#     #         bString += '+'
#     #
#     # return bString, str(coeff_string)
