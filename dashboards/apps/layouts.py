# -*- coding: utf-8 -*-

import dash_core_components as dcc
import dash_html_components as html

from .util import get_main_data


main_dropdowns = html.Div(
    [
        html.P(
            'Pick a battery explosion experiment:',
            style={
                "font-size": "1.5em",
                "margin-left": "10px",
                "margin-bottom": "10px"
            }
        ),
        html.Div(
            id='db_data',
            children=get_main_data(),
            style={'display': 'none'}
        ),
        html.Div(
            [
                html.Label(
                    [
                        'Publication:',
                        dcc.Dropdown(
                            id='vent_ref_pub'
                        ),
                    ],
                    className="control_label"
                ),
                html.Label(
                    [
                        'Cell type:',
                        dcc.Dropdown(
                            id='vent_cell_types'
                        ),
                    ],
                    className="control_label"
                ),
                html.Label(
                    [
                        'Chemistry:',
                        dcc.Dropdown(
                            id='vent_cell_chemistry'
                        ),
                    ],
                    className="control_label"
                ),
                html.Label(
                    [
                        'Electrolyte:',
                        dcc.Dropdown(
                            id='vent_cell_electrolytes'
                        ),
                    ],
                    className="control_label"
                ),
                html.Label(
                    [
                        'SOC:',
                        dcc.Dropdown(
                            id='vent_cell_soc'
                        ),
                    ],
                    className="control_label"
                ),
                html.Div(
                    [
                        html.Button(id='clear_button',
                                    n_clicks=0,
                                    children='Clear',
                                    style={
                                        'position': 'relative',
                                        'top': '40%'}
                                    ),
                    ],
                ),
            ],
            className="pretty_container row",
            style={
                'width': '75%',
            }
        ),
    ]
)
