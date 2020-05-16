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
from .callbacks import * #noqa
from .controls import plot_layout
from .layouts import main_dropdowns
from .util import (
    get_flammability_data, TERNARY_OPTIONS, X_AXIS_OPTIONS, Y_AXIS_OPTIONS
)

# Create app layout
#--------------------CONTAINER FOR WHOLE LAYOUT--------------------------------
layout = html.Div(
    [   #---------------------TOP MAIN HEADER----------------------------------
        html.Div(       #CONTAINS UT LOGO, PAGE TITLE, OTHER PAGE BUTTONS
            [   #--------------------------------------------------------------
                html.Div(           #---Container for UT Logo
                    [
                        html.Img(
                            src=("/assets/shield.png"),
                            style={
                                "height": "60px",
                                "width": "auto",
                            }
                        )
                    ],
                    id="logo",
                    className="one-third column",
                    style={"textAlign": "left"}
                ),                  #---End UT Logo Container
                #--------------------------------------------------------------
                html.Div(           #---Title and Subtitle Container
                    [
                        html.H3(
                            "Deflagration Vents",
                            style={"margin-bottom": "0px"}
                        ),
                        html.H5(
                            "NFPA 68 Sizing Calculator",
                        )
                    ],
                    id="title",
                    className="one-half column",
                    style={"margin-bottom":"30px"}
                    ),              #---Title and Subtitle Container
                #--------------------------------------------------------------
                    html.Div(       #---Page Buttons Container
                        [
                            html.A(                 #Hazard Analysis Buttton
                                html.Button("Hazard Analysis",
                                            id="hazard-analysi"),
                                href="/apps/hazard_analysis",
                                style={"float": "right"}
                                ),
                            html.A(                 #Building Deflagration Button
                                html.Button("Building Deflagration",
                                            id="building-deflagration"),
                                href="/apps/vent_calculator",
                                style={"float":"right"}
                                )
                        ]
                    )               #---Page Button Container
                #-------------------------------------------------------------
                ],                  #---Formatting for Header Bar
                id="header",
                className="row flex-display",
                style={"margin-bottom": "25px"}
                ),
        #-----------------------END TOP MAIN HEADER ----------------------------
        main_dropdowns,                                 #pretty self explanatory
        #-----------------------DATA INPUT SECTION------------------------------


            ]
        )
        #----------------------END OVERALL LAYOUT CONTAINER--------------------
