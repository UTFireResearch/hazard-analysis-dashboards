import dash_core_components as dcc
import dash_html_components as html
#import dash_bootstrap_components as dbc
import numpy as np
import dash_table as dt
import pandas as pd

import copy
from dash.dependencies import Input, Output, State

from .controls import plot_layout
from app import app

#==============LAYOUT FOR BURN INTEGRAL PAGE====================================
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
                            'Burn Integral Calculator',
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
        ), #-----------------------END HEADER DIV-------------------------------
    ],
)
