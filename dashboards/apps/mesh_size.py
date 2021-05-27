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
                                    #value=1,        #---------DELETE ME
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
                                    #value=20,       #-----------DELETE ME
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
                                    #value=1,        #---------DELETE ME
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
                                    #value=15,       #-------------DELETE ME
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
                                    #value=1,        #---------------DELETE ME
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
                                    #value=13,       #------------DELETE ME
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
                                'display':'none',
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
                                    "display": 'none'
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
                                    #value=200    #-----------------------DELETE ME
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
                                    value=1.204,        #------LEAVE ME, MAYBE
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
                                    value=1.005     #--------LEAVE ME, MAYBE
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
                                    value=293,      #-------LEAVE ME, MAYBE
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
                                    value=9.81,     #------LEAVE ME, MAYBE
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
                                    "margin-top": "15px",
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
                        html.H5(
                            html.B('Results:'),
                            style={
                            "margin-bottom": "15px",
                            "color": "maroon"
                            }
                        ),
                        html.Div(
                            [
                                html.H6(
                                    id='mesh_diameter_string',
                                    style={'margin-left':'20px','color':'black'},
                                ),
                            ],
                            className='row flex-display',
                            id='mesh_diameter_row'
                        ),
                        #----------COARSE MESH INFORMATION ROW -----------------
                        html.Hr(
                            style={
                                'margin-left':'20px',
                                'margin-top':'5px',
                                'margin-bottom':'10px',
                            }),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Img(
                                            src=('/assets/mesh_coarse1.PNG'),
                                            style={'height': '200px', 'margin-left': '20px'}
                                        ),
                                    ],
                                    style = {'margin-right':'20px','margin-left':'20px'},
                                ),
                                html.Div(
                                    [
                                        html.H6(
                                            'Your MESH line for FDS is:',
                                            style={'color':'black'},
                                        ),
                                        html.H6(
                                            id='coarse_mesh_line',
                                            #style={'color':'black'},
                                        ),
                                        html.P(
                                            id='coarse_size_string',
                                            style={
                                                'color':'black',
                                                'margin-top': '5px',
                                                'margin-bottom': '5px',
                                            },
                                        ),
                                        html.P(
                                            id='coarse_dx_string',
                                            style={
                                                'color':'black',
                                                'margin-top': '0px',
                                                'margin-bottom': '0px',
                                            },
                                        ),
                                        html.P(
                                            id='coarse_distance_string',
                                            style={
                                                'color':'black',
                                                'margin-top': '0px',
                                                'margin-bottom': '0px',
                                            },
                                        ),
                                        html.P(
                                            id='coarse_number_string',
                                            style={
                                                'color':'black',
                                                'margin-top': '0px',
                                                'margin-bottom': '0px',
                                            },
                                        ),
                                    ],
                                ),
                            ],
                            className='row flex-display',
                            id='mesh_coarse_row',
                        ),
                        #-----------MODERATE MESH INFORMATION ROW-------------------
                        html.Hr(
                            style={
                                'margin-left':'20px',
                                'margin-top':'10px',
                                'margin-bottom':'10px',
                            }),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Img(
                                            src=('/assets/mesh_moderate1.PNG'),
                                            style={'height': '200px', 'margin-left': '20px'}
                                        ),
                                    ],
                                    style = {'margin-right':'20px','margin-left':'20px'},
                                ),
                                html.Div(
                                    [
                                        html.H6(
                                            'Your MESH line for FDS is:',
                                            style={'color':'black'},
                                        ),
                                        html.H6(
                                            id='moderate_mesh_line',
                                            #style={'color':'black'},
                                        ),
                                        html.P(
                                            id='moderate_size_string',
                                            style={
                                                'color':'black',
                                                'margin-top': '15px',
                                                'margin-bottom': '15px',
                                            },
                                        ),
                                        html.P(
                                            id='moderate_dx_string',
                                            style={
                                                'color':'black',
                                                'margin-top': '0px',
                                                'margin-bottom': '0px',
                                            },
                                        ),
                                        html.P(
                                            id='moderate_distance_string',
                                            style={
                                                'color':'black',
                                                'margin-top': '0px',
                                                'margin-bottom': '0px',
                                            },
                                        ),
                                        html.P(
                                            id='moderate_number_string',
                                            style={
                                                'color':'black',
                                                'margin-top': '0px',
                                                'margin-bottom': '0px',
                                            },
                                        ),
                                    ],
                                ),
                            ],
                            className='row flex-display',
                            id='mesh_moderate_row',
                        ),
                        #-----FINE MESH INFORMATION ROW-------------------------
                        html.Hr(
                            style={
                                'margin-left':'20px',
                                'margin-top':'10px',
                                'margin-bottom':'10px',
                        }),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Img(
                                            src=('/assets/mesh_fine1.PNG'),
                                            style={'height': '200px', 'margin-left': '20px'}
                                        ),
                                    ],
                                    style = {'margin-right':'20px','margin-left':'20px'},
                                ),
                                html.Div(
                                    [
                                        html.H6(
                                            'Your MESH line for FDS is:',
                                            style={'color':'black'},
                                        ),
                                        html.H6(
                                            id='fine_mesh_line',
                                            #style={'color':'black'},
                                        ),
                                        html.P(
                                            id='fine_size_string',
                                            style={
                                                'color':'black',
                                                'margin-top': '15px',
                                                'margin-bottom': '15px',
                                            },
                                        ),
                                        html.P(
                                            id='fine_dx_string',
                                            style={
                                                'color':'black',
                                                'margin-top': '0px',
                                                'margin-bottom': '0px',
                                            },
                                        ),
                                        html.P(
                                            id='fine_distance_string',
                                            style={
                                                'color':'black',
                                                'margin-top': '0px',
                                                'margin-bottom': '0px',
                                            },
                                        ),
                                        html.P(
                                            id='fine_number_string',
                                            style={
                                                'color':'black',
                                                'margin-top': '0px',
                                                'margin-bottom': '0px',
                                            },
                                        ),
                                    ],
                                ),
                            ],
                            className='row flex-display',
                            id='mesh_fine_row',
                        ),
                    ],
                    id='mesh_results_box',
                    className='pretty_container twelve columns'
                ),
            ],
            className='row flex-display',
            id='mesh_results_row',
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H6(
                            id='mesh_error_message',
                            style={'margin-top':'10px'}
                        ),
                    ],
                    id='mesh_error_box',
                    className='pretty_container twelve columns',
                ),
            ],
            className='row flex-display',
            id='mesh_error_row',
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
        html.Div(id='mesh_comp_state3',children='FALSE',style={"display": "none"}),

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
    mesh_grav = sqrt(float(mesh_grav))

    mesh_dstar_pwr = float("0.4")

    mesh_d_star = pow( (mesh_hrr / (mesh_p_inf * mesh_cp * mesh_t_inf * mesh_grav) ), mesh_dstar_pwr )

    #HTML PRINTING CODE IN ORIGINAL SOURCE
    mDoStr = 'The characteristic fire diamager D\u2082 is ' + round(mesh_d_star,3)

    mesh_uguide_min_suggested_dx = mesh_d_star / 16
    mesh_uguide_mod_suggested_dx = mesh_d_star / 10
    mesh_uguide_max_suggested_dx = mesh_d_star / 4

    coarse = "<img src='./fds_mesh/coarse.png'><br/>" + "When D<sup>*</sup>/dx = 4: " + "the suggested coarse cell size is " + str(round(float(uguide_max_suggested_dx * 100), 2)) + " cm <br/><br/>"

    moderate = "<img src='./fds_mesh/moderate.png'><br/>" + "When D<sup>*</sup>/dx = 10: " + "the suggested moderate cell size is " + str(round(float(uguide_mod_suggested_dx * 100), 2)) + " cm <br/><br/>"

    fine = "<img src='./fds_mesh/fine.png'><br/>" + "When D<sup>*</sup>/dx = 16, " + "the suggested fine cell size is " + str(round(float(uguide_min_suggested_dx * 100), 2)) + " cm <br/><br/>"

    mesh_uguide_min_suggested_dx = str(mesh_uguide_min_suggested_dx)
    mesh_uguide_mod_suggested_dx = str(mesh_uguide_mod_suggested_dx)
    mesh_uguide_max_suggested_dx = str(mesh_uguide_max_suggested_dx)

    mesh_compute(x0_dim, x1_dim, y0_dim, y1_dim, z0_dim, z1_dim, uguide_max_suggested_dx, coarse)
    mesh_compute(x0_dim, x1_dim, y0_dim, y1_dim, z0_dim, z1_dim, uguide_mod_suggested_dx, moderate)
    mesh_compute(x0_dim, x1_dim, y0_dim, y1_dim, z0_dim, z1_dim, uguide_min_suggested_dx, fine)

    # return oo1, oo2, oo3
    return coarse, moderate, fine

def mesh_compute(x0_dim, x1_dim, y0_dim, y1_dim, z0_dim, z1_dim, dx, resolution):

    #global ijk_bars ---- DO NOT UNCOMMENT
    ijk_bars = []
    # print '<hr>'
    # print resolution
    #global x_dim, y_dim, z_dim, current_dx  ---- DO NOT UNCOMMENT

    current_dx = dx

    x0_dim = Decimal(x0_dim)
    x1_dim = Decimal(x1_dim)
    y0_dim = Decimal(y0_dim)
    y1_dim = Decimal(y1_dim)
    z0_dim = Decimal(z0_dim)
    z1_dim = Decimal(z1_dim)
    dx = Decimal(dx)

    x_dim = x1_dim - x0_dim
    y_dim = y1_dim - y0_dim
    z_dim = z1_dim - z0_dim

    if x_dim == 0:
        # print """<h2><font color="red">X dimension cannot be zero</font></h2>"""
        # fill_previous_values()
        # print_html_footer()
        # sys.exit()
        return None
    if y_dim == 0:
        # print """<h2><font color="red">Y dimension cannot be zero</font></h2>"""
        # fill_previous_values()
        # print_html_footer()
        # sys.exit()
        return None
    if z_dim == 0:
        # print """<h2><font color="red">Z dimension cannot be zero</font></h2>"""
        # fill_previous_values()
        # print_html_footer()
        # sys.exit()
        return None

# Checks to see if dx is bigger than any single dimension
    if (dx > x_dim) | (dx > y_dim) | (dx > z_dim):
        # print """<h2><font color="red">dx cannot be greater than any x, y, or z dimension</font></h2><br/>"""
        # fill_previous_values()
        # print_html_footer()
        # sys.exit()
        return None

    desired_i = x_dim / dx
    desired_j = y_dim / dx
    desired_k = z_dim / dx

    Poisson(int(desired_i))
    Poisson(int(desired_j))
    Poisson(int(desired_k))

    return None

def Poisson(mesh_desired_num):

    #Uses mod 2, 3, 5 to see if numbers are Poisson optimized.
    #----------------
    #If they are not, it goes from x to x*1.4 in increments of 1 and rechecks
    #until factorable
    #----------------
    #Then it returns the factorable and Poisson-friendly I,J,K values

    for i in range(int(mesh_desired_num*Decimal('1.4'))):

        #global mesh_ijk_bars -- DO NOT UNCOMMENT
        pIJKbars = []
        mesh_check_digit = mesh_desired_num

        while mesh_check_digit % 2 == 0:
            mesh_check_digit = mesh_check_digit / 2

        while mesh_check_digit % 3 == 0:
            mesh_check_digit = mesh_check_digit / 3

        while mesh_check_digit % 5 == 0:
            mesh_check_digit = mesh_check_digit / 5

        if mesh_check_digit in (1, 2, 3, 5):
            #mesh_ijk_bars.append(int(mesh_desired_num))
            #break
            return int(mesh_desired_num)
        else:
            mesh_desired_num = mesh_desired_num + 1
            continue

    # if len(mesh_ijk_bars) == 3:
    #     #print_output_results()
    #     #mesh_resolution = ''
    #     return pIJKbars

# def print_output_results():

def mesh_line_string(ijk_bars, dimList):

    mesh_string = "&MESH IJK=" + str(ijk_bars[0]) + "," + str(ijk_bars[1]) + "," + str(ijk_bars[2]) + ", XB=" + str(dimList[0]) + "," + str(dimList[1]) + "," + str(dimList[2]) + "," + str(dimList[3]) + "," + str(dimList[4]) + "," + str(dimList[5]) + ' /'

    return mesh_string

def mesh_size_string(num, dx):

    cell_size = str(round(float(dx * 100), 2))

    cell_string = f"When D*/dx = {num}: the suggested moderate cell size is {cell_size} cm"

    return cell_string

def mesh_dx_string(diffList, ijk_bars):

    d1 = round(diffList[0]/ijk_bars[0], 3)
    d2 = round(diffList[1]/ijk_bars[1], 3)
    d3 = round(diffList[2]/ijk_bars[2], 3)

    dx_string = f" Your actual dx(es) are {d1}, {d2}, {d3} (meters)"

    return dx_string

def mesh_num_string(ijk_bars):

    cNum = ijk_bars[0]*ijk_bars[1]*ijk_bars[2]
    oString = f"Your total number of cells is {cNum:,}"

    return oString

def mesh_input_checking(inList):

    if not all(inList):
        return False, 'You appear to be missing a required field.'

    #VERIFY THAT X1 GREATER THAN X0
    if inList[0] >= inList[1] or inList[2] >= inList[3] or inList[4] >= inList[5]:
        return False, 'Ensure that maximum coordinates are GREATER than minimum coordinates.'

    #VERIFY THAT FIRE PARAMETERS ARE ALL GREATER THAN ZERO
    if inList[6] <= 0 or inList[7] <= 0 or inList[8] <= 0 or inList[9] <= 0 or inList[10] <= 0:
        return False, 'Ensure that all of the fire parameters are POSITIVE and NON-ZERO'

    return [True, '']
#------------------BEGIN CALLBACK DEFINITIONS-----------------------------------

#---THIS CALLBACK TOGGLES VISIBILITY FOR THE RESULT ROW ON AND OFF--------------
@app.callback(
    [
        Output('mesh_results_row','style'),
        Output('mesh_error_box','style'),
    ],
    [
        Input('mesh_comp_state1','children'),
    ],
    [
        State('submit_cell','n_clicks'),
    ]
)
def mesh_visibility_toggle(Mcomp1, clicks):

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

    if Mcomp1 == 'TRUE' and clicks > 0:
        return display_style, hidden_style

    if Mcomp1 == 'FALSE' and clicks == None:
        return hidden_style, hidden_style

    if Mcomp1 == 'FALSE' and clicks > 0:
        return hidden_style, display_style


#THIS CALLBACK EXECUTES ON CLICKING OF 'CALCULATE SUGGESTED CELL SIZE' BUTTON
# @app.callback(
#     [
#         Output('mesh_comp_state2', 'children'),
#         Output('mesh_comp_state3','children')
#     ],
#     [
#         Input('submit_cell','n_clicks'),
#     ],
#     [
#         State('X_min','value'),
#         State('X_max','value'),
#         State('Y_min','value'),
#         State('Y_max','value'),
#         State('Z_min','value'),
#         State('Z_max','value'),
#         State('mesh_HRR_in','value'),
#         State('mesh_density_in','value'),
#         State('mesh_CP_in','value'),
#         State('mesh_T_in','value'),
#         State('mesh_g_in','value'),
# )
# def input_field_checking(btn, xMin, xMax, yMin, yMax, zMin, zMax, hrr, den, cp, temp, grav):
#
#     inList = [xMin,xMax,yMin,yMax,zMin,zMax,hrr,den,cp,temp,grav]
#     oList = []
#     oList = mesh_input_checking(inList)
#
#     if
#
#     return oList[0], oList[1]

@app.callback(
    [
        Output('mesh_comp_state1','children'),
        Output('mesh_diameter_string','children'),
        Output('coarse_mesh_line','children'),
        Output('moderate_mesh_line','children'),
        Output('fine_mesh_line', 'children'),
        Output('coarse_size_string','children'),
        Output('moderate_size_string','children'),
        Output('fine_size_string','children'),
        Output('coarse_distance_string','children'),
        Output('moderate_distance_string','children'),
        Output('fine_distance_string','children'),
        Output('coarse_dx_string','children'),
        Output('moderate_dx_string','children'),
        Output('fine_dx_string','children'),
        Output('coarse_number_string','children'),
        Output('moderate_number_string','children'),
        Output('fine_number_string','children'),
        Output('mesh_error_message','children')
    ],
    [
        Input('submit_cell','n_clicks'),
    ],
    [
        State('X_min','value'),
        State('X_max','value'),
        State('Y_min','value'),
        State('Y_max','value'),
        State('Z_min','value'),
        State('Z_max','value'),
        State('mesh_HRR_in','value'),
        State('mesh_density_in','value'),
        State('mesh_CP_in','value'),
        State('mesh_T_in','value'),
        State('mesh_g_in','value'),
    ]
)
def mesh_suggest_btn_execute(btn, xMin, xMax, yMin, yMax, zMin, zMax, hrr, den, cp, temp, grav):

    cDiv = 4
    mDiv = 10
    fDiv = 16

    grav = sqrt(grav)

    inList = [xMin,xMax,yMin,yMax,zMin,zMax,hrr,den,cp,temp,grav]
    dimList = [xMin,xMax,yMin,yMax,zMin,zMax]

    mesh_test_list = mesh_input_checking(inList)

    if mesh_test_list[0] and btn > 0:

        #CALCULATE D*
        dstar_power = float('0.4')
        d_star = pow((hrr / (den * cp * temp * grav) ), dstar_power)

        #WRITE OUPUT STRING DESCRIBING D*
        dString = 'The characteristic fire diameter D\u2082 is ' + str(round(d_star,3))

        uguide_min_suggested_dx = d_star / fDiv
        uguide_mod_suggested_dx = d_star / mDiv
        uguide_max_suggested_dx = d_star / cDiv

        #DECIMALIZE SHARED MESH PARAMETERS
        x0_dim = Decimal(xMin)
        x1_dim = Decimal(xMax)
        y0_dim = Decimal(yMin)
        y1_dim = Decimal(yMax)
        z0_dim = Decimal(zMin)
        z1_dim = Decimal(zMax)

        xDim = x1_dim - x0_dim
        yDim = y1_dim - y0_dim
        zDim = z1_dim - z0_dim
        diffList = [xDim,yDim,zDim]

        Cdx = Decimal(uguide_max_suggested_dx)
        Mdx = Decimal(uguide_mod_suggested_dx)
        Fdx = Decimal(uguide_min_suggested_dx)

        distance_string = f"Your distances are {xDim}, {yDim}, {zDim} (meters)"

        c_ijk_bars = []
        m_ijk_bars = []
        f_ijk_bars = []

        #COARSE COMPUTATIONS
        cDesI = xDim / Cdx
        cDesJ = yDim / Cdx
        cDesK = zDim / Cdx

        c_ijk_bars.append(Poisson(int(cDesI)))
        c_ijk_bars.append(Poisson(int(cDesJ)))
        c_ijk_bars.append(Poisson(int(cDesK)))

        c1String = mesh_line_string(c_ijk_bars, dimList)
        c2String = mesh_size_string(cDiv,uguide_max_suggested_dx)
        c3String = mesh_dx_string(diffList, c_ijk_bars)
        c4String = mesh_num_string(c_ijk_bars)
        c_num_cells = c_ijk_bars[0] * c_ijk_bars[1] * c_ijk_bars[2]

        #MODERATE COMPUTATIONS
        mDesI = xDim / Mdx
        mDesJ = yDim / Mdx
        mDesK = zDim / Mdx

        m_ijk_bars.append(Poisson(int(mDesI)))
        m_ijk_bars.append(Poisson(int(mDesJ)))
        m_ijk_bars.append(Poisson(int(mDesK)))

        m1String = mesh_line_string(m_ijk_bars, dimList)
        m2String = mesh_size_string(mDiv, uguide_mod_suggested_dx)
        m3String = mesh_dx_string(diffList, m_ijk_bars)
        m4String = mesh_num_string(m_ijk_bars)
        _num_cells = m_ijk_bars[0] * m_ijk_bars[1] * m_ijk_bars[2]

        #MODERATE COMPUTATIONS
        fDesI = xDim / Fdx
        fDesJ = yDim / Fdx
        fDesK = zDim / Fdx

        f_ijk_bars.append(Poisson(int(fDesI)))
        f_ijk_bars.append(Poisson(int(fDesJ)))
        f_ijk_bars.append(Poisson(int(fDesK)))

        f1String = mesh_line_string(f_ijk_bars, dimList)
        f2String = mesh_size_string(fDiv, uguide_min_suggested_dx)
        f3String = mesh_dx_string(diffList, f_ijk_bars)
        f4String = mesh_num_string(f_ijk_bars)
        f_num_cells = f_ijk_bars[0] * f_ijk_bars[1] * f_ijk_bars[2]

        return 'TRUE', dString, c1String, m1String, f1String, c2String, m2String, f2String, distance_string, distance_string, distance_string, c3String, m3String, f3String, c4String, m4String, f4String, ''

    if not mesh_test_list[0]:
        return 'FALSE', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', mesh_test_list[1]




# @app.callback(
#     Output('meshROut2','children'),
#     [
#         Input('submit_cell','n_clicks'),
#     ],
#     [
#         State('mesh_HRR_in','value'),
#         State('mesh_density_in','value'),
#         State('mesh_CP_in','value'),
#         State('mesh_T_in','value'),
#         State('mesh_g_in','valuel'),
#     ]
# )
# def mesh_dstar_comp(mesh_btn2, mHRR, mDen, mCP, mT, mG):
#
#     dstar_compute(mHRR, mDen, mCP, mT, mG)
#
#     # if mHRR and mDen and mCP and mT and mG:
#     #
#     #     d_star_power = 0.4
#     #     mesh_d_star = pow( (mHRR / (mDen * mDen * mT * mG)), d_star_power )
#     #
#     #     mOstring1 = 'The characteristic fire diameter D\u2082 ' + str(round(d_star,3))
#     #
#     #     mesh_uguide_min_suggested_dx = mesh_d_star / 16
#     #     mesh_uguide_mod_suggested_dx = mesh_d_star / 10
#     #     mesh_uguide_max_suggested_dx = mesh_d_star / 4
#     #
#     #
#     #     return mOstring1
#     #
#     # else:
#     #     return 'Fail'



#---THIS CALLBACK EXECUTES ON CLICKING OF 'CALCULATE MESH LINE' BUTTON----------
# @app.callback(
#     [
#         Output('meshROut','children'),
#         Output('meshROut2','children'),
#         Output('meshROut3','children'),
#         Output('mesh_comp_state1', 'children'),
#         Output('mesh_comp_state2', 'children'),
#     ],
#     [
#         Input('submit_cell','n_clicks'),
#     ],
#     [
#         State('X_min','value'),
#         State('X_max','value'),
#         State('Y_min','value'),
#         State('Y_max','value'),
#         State('Z_min','value'),
#         State('Z_max','value'),
#         State('cell_size','value'),
#     ]
# )
# def mesh_line_execution(mesh_btn1,xMin,xMax,yMin,yMax,zMin,zMax,cSize):
#
#     dstar_compute()
#
#
#
#     return 'Success-ish', 'TRUE', 'TRUE'
