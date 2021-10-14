import copy
import json

import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
from plotly.figure_factory import create_ternary_contour

from app import app
from .callbacks import *  # noqa
from .controls import plot_layout

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
                        # html.A(
                        #     html.Button("Vent Sizing",
                        #                 id="vent-sizing",
                        #                 style={'width': '100%'}
                        #     ),
                        #     href="/apps/vent_calculator",
                        #     style={"float": "right","width": '250px'}
                        # )
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
        #-------------------INTTRODUCTION CONTAINER-----------------------------
        html.Div(
            [   #==================INTRODUCTION PRETTY CONTAINER================
                html.Div(
                    [
                        # html.H5(
                        #     'Introduction'
                        # ),
                        html.Div(
                            [
                                html.P("The following model estimates concentration, velocity, density, and position of a hydrogen plume based on a number of user provided parameters."),
                                # html.Hr(
                                #     style={'margin':'5px'}
                                # ),
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
                        #
                        #     ],
                        #     style={"display": "grid", "grid-template-columns": "50% 50%"}
                        # ),

                    ],
                    className='pretty_container four columns'
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
                                html.Div(["Ambient Pressure (Pa)"]),
                                html.Div(
                                    [
                                        dcc.Input(
                                        id='H2_amb_pressure',
                                        placeholder='Enter a value...',
                                        type='number',
                                        min=0,
                                        style={'maxWidth':'250px','float':'right'}
                                        ),
                                    ],
                                    # style={'maxWidth':'150px'}
                                )
                            ],
                            style={"display": "grid", "grid-template-columns": "50% 50%"}
                        ),
                    ],
                    className='pretty_container four columns'
                ),
                html.Div(
                    [
                        html.H5(
                                html.B('Plotting Inputs (Optional)'),
                                style={"margin-bottom": "15px"},
                        ),
                        html.Div
                        (
                            [
                                html.Div(["Minimum x location for plot 1"], style={'float':'left'}),
                                html.Div(
                                    [
                                        dcc.Input(
                                        id='H2_plot1_xmin',
                                        type='number',
                                        value=0,
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
                                html.Div(["Maximum x location for plot 1"]),
                                html.Div(
                                    [
                                        dcc.Input(
                                        id='H2_plot1_xmax',
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
                                html.Div(["Minimum y location for plot 1"]),
                                html.Div(
                                    [
                                        dcc.Input(
                                        id='H2_plot1_ymin',
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
                                html.Div(["Maximum y location for plot 1"]),
                                html.Div(
                                    [
                                        dcc.Input(
                                        id='H2_plot1_ymax',
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
                                        id='H2_vol_con_int',
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
                                        id='H2_vol_con_int',
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
                    className='pretty_container four columns'
                ),


            ],
            style={'padding-left':'5px'},
            className='row flex-display',
        ),
        #-----------------ROW WITH RUN MODEL BUTTON-----------------------------
        html.Div(
            [
                html.Div(
                    [
                        html.Button(
                            'Run Model',
                            id='H2_run_button',
                             n_clicks=0,
                             style={'float':'right', 'minWidth': '200px'},
                         ),
                    ],
                    className='pretty_container twelve columns',
                )
            ],
            style={'padding-left':'5px'},
            className='row flex-display',
        ),
        #-------------------RESULT FIELDS OUPTUT ROW----------------------------
        html.Div(
            [
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
                    ],
                    className='pretty_container twelve columns',
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
                                style={"margin-bottom": "15px"},
                        ),
                        html.Img(
                            src=('/assets/H2_contour1_ex.PNG'),
                            style={'height': '600px', 'margin-left': '20px','float':'left'},
                        ),
                        html.Img(
                            src=('/assets/H2_contour2_ex.PNG'),
                            style={'height': '600px', 'margin-left': '20px','float':'right'},
                        ),
                        html.Img(
                            src=('/assets/H2_contour3_ex.PNG'),
                            style={'height': '600px', 'margin-left': '20px','float':'left'},
                        ),
                        html.Img(
                            src=('/assets/H2_conProf_ex.PNG'),
                            style={'height': '600px', 'margin-left': '20px','float':'right'},
                        ),
                        html.Img(
                            src=('/assets/H2_center_ex.PNG'),
                            style={'height': '600px', 'margin-left': '20px','float':'left'},
                        ),
                        html.Img(
                            src=('/assets/H2_curve_ex.PNG'),
                            style={'height': '600px', 'margin-left': '20px','float':'right'},
                        ),
                        html.Img(
                            src=('/assets/H2_veloc_ex.PNG'),
                            style={'height': '600px', 'margin-left': '20px','float':'left'},
                        ),
                    ],
                    className="pretty_container twelve columns",
                )
            ],
            className="row flex-display"
        )
    ]
)
