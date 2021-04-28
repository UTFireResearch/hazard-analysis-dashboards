import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table

from app import app
from dash.dependencies import Input, Output, State
from decimal import *
from math import sqrt

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
                                id='mesh_density_in',
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
                    className='pretty_container five columns'
                ),
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
                    className='pretty_container nine columns'
                ),
            ],
            className='row flex-display',
        ),
        #-------------MESH RESULTS ROW FLEX-DISPLAY-----------------------------
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            'This is a test', id='meshROut'
                        ),
                        html.P(
                            'This is a test', id='meshROut2'
                        )
                    ],
                    className='pretty_container twelve columns'
                ),
            ],
            className='row flex-display',
            id='mesh_results_row',
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
        #------HTML DIVS TO HOLD HIDDEN VALUES FOR DASHBOARD FUNCTIONING--------
        html.Div(id='mesh_comp_state1',children='FALSE',style={"display": "none"}),
        html.Div(id='mesh_comp_state2',children='FALSE',style={"display": "none"}),

        #-----VALUE PASSING COMPONENTS TO SUBSTITUTE FOR GLOBAL VARIABLES-----------
        #html.Div(id='mesh_input_fields',children='FALSE',style={"display": "none"}),
        dcc.Store(id='input_fields', storage_type='session'),
        dcc.Store(id='input_values', storage_type='session'),
        dcc.Store(id='ijk_bars', storage_type='session'),
    ],
), #---------------------END LAYOUT---------------------------------------------



#--------------------NON-CALLBACK FUNCTION DEFINITIONS--------------------------
#-------------------------------------------------------------------------------
#----THESE FUNCTIONS ARE MORE OR LESS TRANSCRIBED FROM THE ORIGINAL SOURCE

#Calculates the deisred I,J,K values and sends them to the Poisson optimizer for
#checking/calculation
def dstar_compute(mesh_hrr, mesh_p_inf, mesh_cp, mesh_t_inf, mesh_grav):

    mesh_hrr = float(mesh_hrr)
    mesh_p_inf = float(mesh_p_inf)
    mesh_cp = float(mesh_cp)
    mesh_t_inf = float(mesh_t_inf)
    mesh_grav = float(mesh_grav)

    mesh_dstar_pwr = float("0.4")

    mesh_d_star = pow( (mesh_hrr / (mesh_p_inf * mesh_cp * mesh_t_inf * mesh_grav)), mesh_dstar_pwr )

    #HTML PRINTING CODE IN ORIGINAL SOURCE

    mesh_uguide_min_suggested_dx = mesh_d_star / 16
    mesh_uguide_mod_suggested_dx = mesh_d_star / 10
    mesh_uguide_max_suggested_dx = mesh_d_star / 4

    #HTML PRINTING CODE IN ORIGINAL SOURCE

    mesh_uguide_min_suggested_dx = str(mesh_uguide_min_suggested_dx)
    mesh_uguide_mod_suggested_dx = str(mesh_uguide_mod_suggested_dx)
    mesh_uguide_max_suggested_dx = str(mesh_uguide_max_suggested_dx)

    #TO BE CONTINUED -------------

    return None

def Poisson(mesh_desired_num):

    #Uses mod 2, 3, 5 to see if numbers are Poisson optimized.
    #----------------
    #If they are not, it goes from x to x*1.4 in increments of 1 and rechecks
    #until factorable
    #----------------
    #Then it returns the factorable and Poisson-friendly I,J,K values

    for i in range(mesh_desired_num*Decimal('1.4')):

        global mesh_ijk_bars
        mesh_check_digit = mesh_desired_num

        while mesh_check_digit % 2 == 0:
            mesh_check_digit = mesh_check_digit / 2

        while mesh_check_digit % 3 == 0:
            mesh_check_digit = mesh_check_digit / 3

        while mesh_check_digit % 5 == 0:
            mesh_check_digit = mesh_check_digit / 5

        if mesh_check_digit in (1, 2, 3, 5):
            mesh_ijk_bars.append(int(mesh_desired_num))
            break
        else:
            mesh_desired_num = mesh_desired_num + 1
            continue

    if len(mesh_ijk_bars) == 3:
        print_output_results()
        mesh_resolution = ''

        #------CREATE STRING AND SEND IT TO BODY IN ORIGINAL CGI SCRIPT -
        mesh_output_string1 = "Your MESH line for FDS is: " + str(mesh_ijk_bars[0]) + "," + str(mesh_ijk_bars[1]) + "," + str(ijk_bars[2]) + ", XB=" + str(mesh_x0_dim) + "," + str(mesh_y0_dim) + "," + str(mesh_y1_dim) + "," + str(mesh_z0_dim) + "," + str(mesh_z1_dim)

        mesh_ouput_string2 = "You entered: "

        return None

# def print_output_results():



#------------------BEGIN CALLBACK DEFINITIONS-----------------------------------
#-------------------------------------------------------------------------------

@app.callback(
    Output('meshROut2','children'),
    [
        Input('submit_cell','n_clicks'),
    ],
    [
        State('mesh_HRR_in','value'),
        State('mesh_density_in','value'),
        State('mesh_CP_in','value'),
        State('mesh_T_in','value'),
        State('mesh_g_in','valuel'),
    ]
)
def exec1(mesh_btn2, mHRR, mDen, mCP, mT, mG):

    if mHRR and mDen and mCP and mT and mG:

        d_star_power = 0.4
        mesh_d_star = pow( (mHRR / (mDen * mDen * mT * mG)), d_star_power )

        mOstring1 = 'The characteristic fire diameter D\u2082 ' + str(round(d_star,3))

        mesh_uguide_min_suggested_dx = mesh_d_star / 16
        mesh_uguide_mod_suggested_dx = mesh_d_star / 10
        mesh_uguide_max_suggested_dx = mesh_d_star / 4


        return mOstring1

    else:
        return 'Fail'

#---THIS CALLBACK TOGGLES VISIBILITY FOR THE RESULT ROW ON AND OFF--------------
@app.callback(
    Output('mesh_results_row','style'),
    [
        Input('mesh_comp_state1','children'),
        Input('mesh_comp_state2','children')
    ]
)
def mesh_visibility_toggle(Mcomp1,Mcomp2):

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

    if Mcomp1 == 'TRUE' and Mcomp2 == 'TRUE':

        return display_style

    else:
        return hidden_style

#---THIS CALLBACK EXECUTES ON CLICKING OF 'CALCULATE MESH LINE' BUTTON----------
@app.callback(
    [
        Output('meshROut','children'),
        Output('mesh_comp_state1', 'children'),
        Output('mesh_comp_state2', 'children'),
    ],
    [
        Input('submit_mesh','n_clicks'),
    ],
    [
        State('X_min','value'),
        State('X_max','value'),
        State('Y_min','value'),
        State('Y_max','value'),
        State('Z_min','value'),
        State('Z_max','value'),
        State('cell_size','value'),
    ]
)
def mesh_primary_execution(mesh_btn1,xMin,xMax,yMin,yMax,zMin,zMax,cSize):





    return 'Success-ish', 'TRUE', 'TRUE'
