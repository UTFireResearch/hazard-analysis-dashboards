import dash_core_components as dcc
import dash_html_components as html
import warnings
import numpy as np
import pandas as pd
import json

from scipy.interpolate import griddata
from CoolProp import CoolProp as cp
from scipy import constants as constant
from scipy import integrate
from scipy import optimize
from dash.dependencies import Input, Output, State
from plotly.figure_factory import create_ternary_contour
from app import app
from .callbacks import *  # noqa
from dash.exceptions import PreventUpdate
from scripts.H2_model import Fluid, JetModel # OtherJetModel
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame




#====================PLOTLY VERSION SPECIFIC DEPENDENCIES=======================
#===============================================================================
import plotly.express as px
import plotly.graph_objects as go

#=========================MATPLOTLIB VERSION SPECIFIC DEPENDENCIES==============
#===============================================================================
# import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
# import matplotlib.style as style
# import matplotlib.cm as cm


#==============VESTIGIAL DEPENDENCIES I THINK COULD BE REMOVED==================
#===============================================================================
# from .controls import plot_layout



#---------------------MAIN LAYOUT CONTAINER-------------------------------------
layout = html.Div( 
    [
        #-------------------HEADER BAR CONTAINER--------------------------------
        html.Div(
            [   #---------------------LEFT HEADER COLUMN-----------------------
                html.Div(
                    [   #-----------------UT LOGO------------------------------
                        html.Img(
                            src=("/assets/shield.png"),
                            style={
                                "height": "60px",
                                "width": "auto",
                                'textAlign': 'center',
                            }
                        )
                    ],
                    id="logo",
                    className='one-third column',
                    style={'textAlign':'left'}
                ),
                html.Div(
                    [
                        html.H3(
                            'H2 Release Screening Model',
                        ),
                    ],
                    id="title",
                    className='one-half column',
                    style={"margin-bottom": "30px"}
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Tools Home",
                                        id="building-deflagration",
                                        style={'width': '100%'}
                            ),
                            href="/apps/table",
                            style={"float": "right", 'width': '250px'}
                        ),
                        

                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className='row flex-display',
            style={
                "magin-bottom": "25px"
            }
        ),
        #-------------------INTRODUCTION CONTAINER-----------------------------
        html.Div(
            [   #==================INTRODUCTION PRETTY CONTAINER================
                html.Div(
                    [
                        # html.H5(
                        #     'Introduction'
                        # ),
                        html.Div(
                            [
                                html.P("There are currently substanital investments being made to convert many industries from conventional fuels sources to hydrogen as part of efforts to reduce carbon emissions. With this in mind, safety considerations around hydrogen leaks with only become more important."),
                                html.P("The following model estimates concentration, velocity, density, and position of a hydrogen plume based on a number of user provided parameters."),
                                html.Hr(
                                    style={'margin':'5px'}
                                ),
                                html.P("This tool was developed by Juliette Franqueville and is maintained by The University of Texas Fire Research Group."),
                                html.P(
                                    children=[
                                        html.I('PLEASE NOTE: The model may take up to 15 seconds to run. Please wait before clicking the run button again or refreshing the page.'),
                                    ]
                                ),
                            ],
                        ),
                    ],
                    className='pretty_container twelve columns'
                )
            ],
            style={'padding-left':'5px'},
            className='row flex-display',
        ),
        #-------------------------INPUT CONTAINER-------------------------------
        html.Div(
            [
                html.Div(
                    [
                        html.H5(
                                html.B('Input Parameters'),
                                style={"margin-bottom": "15px"},
                        ),
                        html.Div
                        (
                            [
                                html.Div(["Hydrogen Temperature (K)"], style={'float':'left'}),
                                html.Div(
                                    [
                                        dcc.Input(
                                        id='H2_temp',
                                        placeholder='Enter a value...',
                                        type='number',
                                        min=0,
                                        value=300,
                                        style={'maxWidth':'250px','float':'right'}
                                        ),
                                    ],
                                    #style={'maxWidth':'150px'}
                                ),
                            ],
                            style={"display": "grid", "grid-template-columns": "50% 50%"}
                        ),
                        html.Div(
                            [
                                html.Div(["Hydrogen Pressure (Pa)"]),
                                html.Div(
                                    [
                                        dcc.Input(
                                        id='H2_pressure',
                                        placeholder='Enter a value...',
                                        type='number',
                                        min=0,
                                        value=4e6,
                                        style={'maxWidth':'250px','float':'right'}
                                        ),
                                    ],
                                    # style={'maxWidth':'150px'}
                                )
                            ],
                            style={"display": "grid", "grid-template-columns": "50% 50%"}
                        ),
                        html.Div(
                            [
                                html.Div(["Orifice Diameter (m)"]),
                                html.Div(
                                    [
                                        dcc.Input(
                                        id='orifice_diameter',
                                        placeholder='Enter a value...',
                                        type='number',
                                        min=0,
                                        value=0.001,
                                        style={'maxWidth':'250px','float':'right'}
                                        ),
                                    ],
                                    # style={'maxWidth':'150px'}
                                )

                            ],
                            style={"display": "grid", "grid-template-columns": "50% 50%"}
                        ),
                        html.Div(
                            [
                                html.Div(["Release Angle* (rad)"]),
                                html.Div(
                                    [
                                        dcc.Input(
                                        id='H2_release_angle',
                                        placeholder='Enter a value...',
                                        type='number',
                                        min=0,
                                        value=0,
                                        style={'maxWidth':'250px','float':'right'}
                                        ),
                                    ],
                                    # style={'maxWidth':'150px'}
                                )

                            ],
                            style={"display": "grid", "grid-template-columns": "50% 50%"}
                        ),
                        html.Div(
                            [
                                html.Div(["Release Velocity** (m/s)"]),
                                html.Div(
                                    [
                                        dcc.Input(
                                        id='H2_release_velocity',
                                        placeholder='Enter a value...',
                                        type='number',
                                        min=0,
                                        value=200,
                                        style={'maxWidth':'250px','float':'right'}
                                        ),
                                    ],
                                    # style={'maxWidth':'150px','float':'right'}
                                )

                            ],
                            style={"display": "grid", "grid-template-columns": "50% 50%"}
                        ),
                        # html.Hr(),
                        # html.Div(
                        #     [
                        #         html.Div(['Model']),
                        #         html.Div(
                        #             [
                        #                 dcc.Dropdown(
                        #                     id='H2_model',
                        #                     options=[
                        #                         {'label': 'Hyman', 'value': 'Hyman'},
                        #                         {'label': 'Other Model', 'value': 'Other'},
                        #                         ],
                        #                     value='Other',
                        #                     style={'maxWidth':'250px', 'minWidth':'200px','float':'right'}
                        #                 ),
                        #             ],
                        #         ),
                        
                        #     ],
                        #     style={"display": "grid", "grid-template-columns": "50% 50%"}
                        # ),

                    ],
                    className='pretty_container six columns',
                    style={'padding-right':'25px', 'padding-left':'25px'}
                ),
                html.Div(
                    [
                        html.H5(
                                html.B('Ambient Conditions'),
                                style={"margin-bottom": "15px"},
                        ),
                        html.Div
                        (
                            [
                                html.Div(["Ambient Temperature (K)"], style={'float':'left'}),
                                html.Div(
                                    [
                                        dcc.Input(
                                        id='H2_amb_temp',
                                        placeholder='Enter a value...',
                                        type='number',
                                        min=0,
                                        value=300,
                                        style={'maxWidth':'250px','float':'right'},
                                        ),
                                    ],
                                    #style={'maxWidth':'150px'}
                                ),
                            ],
                            style={"display": "grid", "grid-template-columns": "50% 50%"}
                        ),
                        html.Div(
                            [
                                html.Div(["Ambient Pressure (Pa)"]),
                                html.Div(
                                    [
                                        dcc.Input(
                                        id='H2_amb_pressure',
                                        placeholder='Enter a value...',
                                        type='number',
                                        min=0,
                                        value=101000,
                                        style={'maxWidth':'250px','float':'right'}
                                        ),
                                    ],
                                    # style={'maxWidth':'150px'}
                                )
                            ],
                            style={"display": "grid", "grid-template-columns": "50% 50%"}
                        ),
                        html.H5(
                            html.B('Plotting Inputs'),
                            style={"margin-bottom": "15px"},
                        ),
                        # html.Div
                        # (
                        #     [
                        #         html.Div(["Minimum x location for plot 1"], style={'float':'left'}),
                        #         html.Div(
                        #             [
                        #                 dcc.Input(
                        #                 id='H2_plot1_xmin',
                        #                 type='number',
                        #                 value=0,
                        #                 style={'maxWidth':'250px','float':'right'}
                        #                 ),
                        #             ],
                        #             #style={'maxWidth':'150px'}
                        #         ),
                        #     ],
                        #     style={"display": "grid", "grid-template-columns": "50% 50%"}
                        # ),
                        # html.Div(
                        #     [
                        #         html.Div(["Maximum x location for plot 1"]),
                        #         html.Div(
                        #             [
                        #                 dcc.Input(
                        #                 id='H2_plot1_xmax',
                        #                 type='number',
                        #                 value=0,
                        #                 style={'maxWidth':'250px','float':'right'}
                        #                 ),
                        #             ],
                        #             # style={'maxWidth':'150px'}
                        #         )
                        #     ],
                        #     style={"display": "grid", "grid-template-columns": "50% 50%"}
                        # ),
                        # html.Div(
                        #     [
                        #         html.Div(["Minimum y location for plot 1"]),
                        #         html.Div(
                        #             [
                        #                 dcc.Input(
                        #                 id='H2_plot1_ymin',
                        #                 type='number',
                        #                 style={'maxWidth':'250px','float':'right'}
                        #                 ),
                        #             ],
                        #             # style={'maxWidth':'150px'}
                        #         )
                        #     ],
                        #     style={"display": "grid", "grid-template-columns": "50% 50%"}
                        # ),
                        # html.Div(
                        #     [
                        #         html.Div(["Maximum y location for plot 1"]),
                        #         html.Div(
                        #             [
                        #                 dcc.Input(
                        #                 id='H2_plot1_ymax',
                        #                 type='number',
                        #                 style={'maxWidth':'250px','float':'right'}
                        #                 ),
                        #             ],
                        #             # style={'maxWidth':'150px'}
                        #         )
                        #     ],
                        #     style={"display": "grid", "grid-template-columns": "50% 50%"}
                        # ),
                        html.Div(
                            [
                                html.Div(["Volume concentration of interest for contour plot 1 (v/V)"]),
                                html.Div(
                                    [
                                        dcc.Input(
                                        id='H2_vol_con_int',
                                        type='number',
                                        value=0.4,
                                        style={'maxWidth':'250px','float':'right'}
                                        ),
                                    ],
                                    # style={'maxWidth':'150px'}
                                )
                            ],
                            style={"display": "grid", "grid-template-columns": "50% 50%"}
                        ),
                        html.Div(
                            [
                                html.Div(["Point along pathline at which to plot contour plot 3 (meters)"]),
                                html.Div(
                                    [
                                        dcc.Input(
                                        id='H2_plot3_point',
                                        type='number',
                                        value=0,
                                        style={'maxWidth':'250px','float':'right'}
                                        ),
                                    ],
                                    # style={'maxWidth':'150px'}
                                )
                            ],
                            style={"display": "grid", "grid-template-columns": "50% 50%"}
                        ),
                        html.Div(
                            [
                                html.Div(["Minimum mass concentration after which integration stops"]),
                                html.Div(
                                    [
                                        dcc.Input(
                                        id='H2_min_mass_con',
                                        type='number',
                                        value=0.0007,
                                        style={'maxWidth':'250px','float':'right'}
                                        ),
                                    ],
                                    # style={'maxWidth':'150px'}
                                )
                            ],
                            style={"display": "grid", "grid-template-columns": "50% 50%"}
                        ),
                    ],
                    className='pretty_container six columns',
                    style={'padding-right':'25px', 'padding-left':'25px'}
                ),
            ],
            style={'padding-left':'5px'},
            className='row flex-display',
        ),
        #-----------------ROW WITH RUN MODEL BUTTON-----------------------------
        # html.Div(
        #     [
                
        #     ],
        #     style={'padding-left':'5px'},
        #     className='row flex-display',
        # ),
        #-------------------RESULT FIELDS OUPTUT ROW----------------------------
        html.Div(
            [
                html.Div(
                    [
                        html.Button(
                            'Run Model',
                            id='H2_run_button',
                             n_clicks=0,
                             style={'float':'left', 'width': '100%', 'height': '100%'},
                         ),
                    ],
                    className='pretty_container two columns',
                    style={'padding':'25px'}
                ),
                
                #=============OUPUT PARAMETERS PRETTY CONTAINER==================
                html.Div(
                    [
                        html.H5(
                                html.B('Output Parameters'),
                                style={"margin-bottom": "15px"},
                        ),
                        html.Div(
                            [
                                html.Div(["Chocked Flow"]),
                                html.Div(
                                    [
                                        dcc.Input(
                                        id='H2_choked_yn',
                                        type='text',
                                        disabled=True,
                                        value=0,
                                        style={'maxWidth':'250px','float':'right'}
                                        ),
                                    ],
                                    # style={'maxWidth':'150px'}
                                )
                            ],
                            style={"display": "grid", "grid-template-columns": "50% 50%"}
                        ),

                        


                        html.Div(
                            [
                                html.Div(["Throat Pressure"]),
                                html.Div(
                                    [
                                        dcc.Input(
                                        id='H2_throat_pressure',
                                        type='text',
                                        disabled=True,
                                        value=0,
                                        style={'maxWidth':'250px','float':'right'}
                                        ),
                                    ],
                                    # style={'maxWidth':'150px'}
                                )
                            ],
                            style={"display": "grid", "grid-template-columns": "50% 50%"}
                        ),
                        html.Div(
                            [
                                html.Div(["Horizontal Seperation Distance"]),
                                html.Div(
                                    [
                                        dcc.Input(
                                        id='H2_horizon_dist',
                                        type='text',
                                        disabled=True,
                                        value=0,
                                        style={'maxWidth':'250px','float':'right'}
                                        ),
                                    ],
                                    # style={'maxWidth':'150px'}
                                )
                            ],
                            style={"display": "grid", "grid-template-columns": "50% 50%"}
                        ),
                        html.Div(
                            [
                                html.Div(["Vertical Seperation Distance"]),
                                html.Div(
                                    [
                                        dcc.Input(
                                        id='H2_vertical_dist',
                                        type='text',
                                        disabled=True,
                                        value=0,
                                        style={'maxWidth':'250px','float':'right'}
                                        ),
                                    ],
                                    # style={'maxWidth':'150px'}
                                )
                            ],
                            style={"display": "grid", "grid-template-columns": "50% 50%"}
                        ),


                      html.Div( 
                          [
                              html.Button("Download csv", id="btn"), 
                          Download(id="download")
                          ])
    
                    ],
                    className='pretty_container eleven columns',
                    style={'padding-right':'25px', 'padding-left':'25px'}
                )
            ],
            style={'padding-left':'5px'},
            className='row flex-display',
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H5(
                                html.B('Output Plots'),
                                # style={"margin-bottom": "15px"},
                        ),
                    ],
                    className='pretty_container twelve columns',
                )
            ],
            className='row flex-display',
            id='h2_output_header',
            style={'display':'None'}
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(
                                    id = 'h2_plot1',
                                    style={'float':'left'}
                                ),
                                dcc.Graph(
                                 id = 'h2_plot2',
                                 style={'float':'right'}
                                ),
                            ],
                            style={"display": "grid", "grid-template-columns": "50% 50%"}
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    id = 'h2_plot3',
                                    style={'float':'left'}
                                ),
                                dcc.Graph(
                                 id = 'h2_plot4',
                                 style={'float':'right'}
                                ),
                            ],
                            style={"display": "grid", "grid-template-columns": "50% 50%"}
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    id = 'h2_plot5',
                                    style={'float':'left'}
                                ),
                                dcc.Graph(
                                 id = 'h2_plot6',
                                 style={'float':'right'}
                                ),
                            ],
                            style={"display": "grid", "grid-template-columns": "50% 50%"}
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    id = 'h2_plot7',
                                    style={'float':'left'}
                                ),
                                # dcc.Graph(
                                #  id = 'h2_plot6',
                                #  style={'float':'right'}
                                # ),
                            ],
                            style={"display": "grid", "grid-template-columns": "50% 50%"}
                        ),
                    ],
                    className='pretty_container twelve columns'
                )
            ],
            className='row flex-display',
            id = 'h2_output_row',
            style={'display':'none'}
        ),
        dcc.Store(id='raw_data')
    ]
)

#========================PLOTLY VERSION OF THE CALLBACK=========================================
#===============================================================================================\
#data = np.column_stack((np.arange(10), np.arange(10) * 2))
#df = pd.DataFrame(columns=["a column", "another column"], data=data)





@app.callback(
    [
        Output('H2_choked_yn', 'value'),
        Output('H2_throat_pressure', 'value'),
        Output('H2_horizon_dist', 'value'),
        Output('H2_vertical_dist', 'value'),
        Output('h2_plot1', 'figure'),
        Output('h2_plot2', 'figure'),
        Output('h2_plot3', 'figure'),
        Output('h2_plot4', 'figure'),
        Output('h2_plot5', 'figure'),
        Output('h2_plot6', 'figure'),
        Output('h2_plot7', 'figure'),
        Output('raw_data','data'),
        Output('h2_output_row', 'style'),
    ],
    [
        Input('H2_run_button', 'n_clicks'),
    ],

   
    [
        State('H2_temp', 'value'),
        State('H2_pressure','value'),
        State('orifice_diameter', 'value'),
        State('H2_release_angle', 'value'),
        State('H2_release_velocity', 'value'),
        State('H2_amb_temp', 'value'),
        State('H2_amb_pressure', 'value'),
        State('H2_vol_con_int', 'value'),
        State('H2_plot3_point', 'value'),
        State('H2_min_mass_con', 'value'),
    ]
)
def H2_code_run(h2_button_clicks, release_temperature, release_pressure, orifice_diameter, release_angle, velocity_if_not_sonic, ambient_temperature, ambient_pressure, contour_of_interest, point_along_pathline, min_concentration):

    if h2_button_clicks < 1:
        raise PreventUpdate
    else:
        args = [ambient_temperature, ambient_pressure, release_temperature, release_pressure, orifice_diameter,
                    release_angle, min_concentration, point_along_pathline,
                    contour_of_interest, velocity_if_not_sonic]

        #run model
        Jet = JetModel(*args)
        Jet.run()
        
        figures = np.array(7)
        figures = Jet.centerline_velocity_plot(), Jet.centerline_mass_concentration_plot(), Jet.theta_plot(), Jet.concentration_profile_plot(), Jet.contour_plot_1(), Jet.centerline_mole_concentration_plot(), Jet.contour_plot_2()

        #Output values
        choked_flow = 'yes' if Jet.H2_fluid.choked else 'no'
        jet_pressure = Jet.pressure_at_1 if Jet.H2_fluid.choked else ambient_pressure
        horizontal_seperation = np.round(Jet.max_x_coords[0], 3)
        vertical_seperation = np.round(Jet.max_y_coords[1], 3)

        h2_hidden_style = {'display':'none'}
        h2_shown_style = {'display': 'block'}

        # Write to csv file
        df = pd.DataFrame(Jet.__solution__)
        #data = send_data_frame(df.tjsono_csv, filename="raw_data.csv")
        data = df.to_json()

        return_style = h2_shown_style if h2_button_clicks else h2_hidden_style

        return choked_flow, jet_pressure, horizontal_seperation, vertical_seperation, figures[0], figures[1], figures[2], figures[3], figures[4], figures[5], figures[6],data, return_style 


@app.callback(Output('download','data'),[Input('btn','n_clicks'),Input('raw_data','data')])
def generate_csv(n_clicks,raw):
    # I had to write this line otherwise it would automatically download the file even if you didn't click the download button...seems hacky
    if n_clicks is None:
        raise PreventUpdate
    json_data = json.loads(raw)
    df = pd.DataFrame.from_dict(json_data, orient='columns')
    return send_data_frame(df.to_csv, filename="raw_data.csv")
 