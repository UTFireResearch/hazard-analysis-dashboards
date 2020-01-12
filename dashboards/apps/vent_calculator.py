# -*- coding: utf-8 -*-

import copy
import json

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from .callbacks import *  # noqa
from .controls import plot_layout
from .layouts import main_dropdowns
from scripts.explosion_model import Explosion, Inputs, Patm
from .util import _get_fuel_species, AIR_SPECIES


# Create app layout
layout = html.Div(
    [
        html.Div(
            [
                html.Div(
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
                    className='one-third column',
                    style={"textAlign": "left"}
                ),
                html.Div(
                    [
                        html.H3(
                            'Building Deflagration',
                            style={"margin-bottom": "0px"}
                        ),
                        html.H5(
                            'Pressure-Time History',
                        )
                    ],
                    id="title",
                    className='one-half column',
                    style={"margin-bottom": "30px"}
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Hazard Analysis",
                                        id="hazard-analysis"),
                            href="/apps/hazard_analysis",
                            style={"float": "right"}
                        )
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
        main_dropdowns,
        html.Div(
            [
                html.P(
                    'Room and vent dimensions:',
                    style={
                        "font-size": "1.5em",
                        "margin-left": "10px",
                        "margin-bottom": "10px"
                    }
                ),
                html.Div(
                    [
                        html.Label(
                            [
                                'Spherical Room Radius:',
                                dcc.Input(
                                    id="vent_room_rad",
                                    type="number",
                                    min=0,
                                    placeholder="Radius (m)",
                                    className="control_label"
                                ),
                            ],
                            className="control_label"
                        ),
                        html.Label(
                            [
                                'Vent Area:',
                                dcc.Input(
                                    id="vent_area",
                                    type="number",
                                    min=0,
                                    placeholder="Area (m^2)",
                                    className="control_label"
                                ),
                            ],
                            className="control_label"
                        ),
                        html.Label(
                            [
                                'Vent Drag Coefficient (Cd):',
                                dcc.Input(
                                    id="vent_drag",
                                    type="number",
                                    min=0,
                                    placeholder="Drag Coeff",
                                    className="control_label"
                                ),
                            ],
                            className="control_label"
                        ),
                    ],
                    className="pretty_container row",
                    style={
                        'width': '50%',
                    }
                ),
            ]
        ),
        html.Div(
            [
                html.Div(id='selected_experiment', style={'display': 'none'}),
                html.Div(id='gas_composition', style={'display': 'none'}),
                html.Div(
                    [
                        dcc.Graph(id='composition_plot')
                    ],
                    className='pretty_container four columns',
                ),
                html.Div(
                    [
                        dcc.Graph(id='explosion_plot')
                    ],
                    id="explosionGraphContainer",
                    className="pretty_container eight columns"
                )
            ],
            className="row"
        )
    ],
    id="mainContainer",
    style={
        "display": "flex",
        "flex-direction": "column"
    }
)


@app.callback(
    Output("explosion_plot", "figure"),
    [
        Input("gas_composition", "children"),
        Input("vent_room_rad", "value"),
        Input("vent_area", "value"),
        Input("vent_drag", "value"),
    ],
)
def make_explosion_figure(gases, radius, area, drag):
    """ Create explosion plot. """
    gases = json.loads(gases) if gases else {}
    data = []

    if gases and radius and area and drag:

        fuel_species = _get_fuel_species(gases)

        # Gas properties
        gas = Inputs(
            air=AIR_SPECIES,
            fuel=fuel_species,
            phi=1.0,  # Composition
            f=1.0,
            P=Patm,  # Initial Pressure
            T=298,  # Initial unburned gas temperature (K)
            S=0.45
        )

        # Room and Vent geometry
        geom = Inputs(
            R=radius,
            Cd=area,
            Av=drag
        )

        # Control inputs
        cntrl = Inputs(
            tmax=0.35  # Max Time for analysis
        )

        explosion = Explosion(gas=gas, geom=geom, cntrl=cntrl)
        explosion.run()

        data = [
            dict(
                type="scatter",
                mode="lines",
                x=explosion.t,
                y=explosion.P_,
                name="Explosion Pressure vs. Time",
                opacity=1,
                hoverinfo="skip",
            )
        ]

    layout = copy.deepcopy(plot_layout)
    layout["title"] = "Pressure vs. Time"
    layout["showlegend"] = False
    layout["xaxis"] = {"title": {"text": "time (s)"}}
    layout["yaxis"] = {"title": {"text": "Pressure"}}

    figure = dict(data=data, layout=layout)
    return figure
