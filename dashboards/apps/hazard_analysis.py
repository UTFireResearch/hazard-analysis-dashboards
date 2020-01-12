# -*- coding: utf-8 -*-

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
from .layouts import main_dropdowns
from .util import (
    get_flammability_data, TERNARY_OPTIONS, X_AXIS_OPTIONS, Y_AXIS_OPTIONS
)


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
                ),
                html.Div(
                    [
                        html.H3(
                            'Battery Vent Gas Hazard Analysis',
                        ),
                    ],
                    id="title",
                    className='one-half column',
                    style={"margin-bottom": "30px"}
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Building Deflagration",
                                        id="building-deflagration"),
                            href="/apps/vent_calculator",
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
                html.Div(id='selected_experiment', style={'display': 'none'}),
                html.Div(id='gas_composition', style={'display': 'none'}),
                html.Div(id='flammability_data', style={'display': 'none'}),
                html.Div(
                    [
                        dcc.Graph(id='composition_plot')
                    ],
                    className='pretty_container seven columns',
                ),
                html.Div(
                    [
                        dash_table.DataTable(
                            id='summary_table',
                            columns=[{'name': 'Parameter', 'id': 'param'},
                                     {'name': 'Value', 'id': 'value'}],
                            data=[],
                            style_as_list_view=True,
                            style_cell={
                                'font-family': ["Open Sans", "HelveticaNeue",
                                                "Helvetica Neue", "Helvetica",
                                                "Arial", "sans-serif"],
                                'font-size': '18px',
                                'textAlign': 'center',
                                'height': '85px',
                                'minWidth': '0px', 'maxWidth': '180px',
                                'whiteSpace': 'normal'
                            },
                            style_cell_conditional=[{
                                'if': {'column_id': 'param'},
                                'textAlign': 'left'
                            }],
                            style_header_conditional=[{
                                'if': {'column_id': 'param'},
                                'textAlign': 'left'
                            }],
                            style_header={
                                'fontWeight': 'bold',
                                'textAlign': 'center'
                            },
                        )
                    ],
                    id="table_div",
                    className="pretty_container five columns"
                )
            ],
            className="row"
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label(
                                    [
                                        'y-axis:',
                                        dcc.Dropdown(
                                            id='y_axis',
                                            options=Y_AXIS_OPTIONS,
                                            placeholder='Change y-axis:',
                                            style={'width': '80%',
                                                   'padding-left': '10px'},
                                        ),
                                    ],
                                    className="control_label row",
                                ),
                                html.Label(
                                    [
                                        'x-axis:',
                                        dcc.Dropdown(
                                            id='x_axis',
                                            options=X_AXIS_OPTIONS,
                                            placeholder='Change x-axis:',
                                            style={'width': '80%',
                                                   'padding-left': '10px'},
                                        ),
                                    ],
                                    className="control_label row",
                                ),
                            ],
                            className="row",
                            style={'padding-bottom': '10px'}
                        ),
                        dcc.Graph(id='summary_graph')
                    ],
                    className='pretty_container seven columns',
                ),
                html.Div(
                    [
                        html.Label(
                            [
                                dcc.Dropdown(
                                    id='ternary_dropdown',
                                    options=TERNARY_OPTIONS,
                                    placeholder='Select plot',
                                    style={'width': '60%'},
                                ),
                            ],
                            className="control_label"
                        ),
                        dcc.Graph(id='ternary_graph')
                    ],
                    className='pretty_container five columns',
                ),
            ],
            className='row'
        ),
    ],
    id="mainContainer",
    style={
        "display": "flex",
        "flex-direction": "column"
    }
)


@app.callback(
    Output('flammability_data', 'children'),
    [Input('selected_experiment', 'children')])
def update_flammability_data(experiment):
    """ Load experiment data based on selected experiment. """
    data = None
    if experiment:
        data = get_flammability_data(json.loads(experiment))

    return json.dumps(data)


@app.callback(
    Output('summary_table', 'data'),
    [Input('flammability_data', 'children')])
def update_summary_table(flammability_data):
    """ Update summary table based on selected experiment. """
    data = [{'param': 'Lower Flammability Limit', 'value': '%'},
            {'param': 'Upper Flammability Limit', 'value': '%'},
            {'param': 'Laminar Flame Speed', 'value': 'm/s'},
            {'param': 'Max Adiabatic Pressure', 'value': 'bar'}]

    flammability_data = json.loads(flammability_data)

    if flammability_data is not None:
        flammability_data.pop('_id')
        df = pd.DataFrame.from_dict(flammability_data,
                                    orient='index').transpose()

        ufl = max(df[(df.Xi == 0) & (df.Flammable == 1)].Xf) * 100
        lfl = min(df[(df.Xi == 0) & (df.Flammable == 1)].Xf) * 100
        su = max(df.Su)
        p_max = max(df.Pmax)

        data = [{'param': 'Lower Flammability Limit',
                 'value': '{0:.2f} %'.format(lfl)},
                {'param': 'Upper Flammability Limit',
                 'value': '{0:.2f} %'.format(ufl)},
                {'param': 'Laminar Flame Speed',
                 'value': '{0:.2f} m/s'.format(su)},
                {'param': 'Max Adiabatic Pressure',
                 'value': '{0:.2f} bar'.format(p_max)}]

    return data


@app.callback(
    Output('summary_graph', 'figure'),
    [
        Input('flammability_data', 'children'),
        Input('x_axis', 'value'),
        Input('y_axis', 'value'),
        Input('x_axis', 'label'),
        Input('y_axis', 'label'),
    ])
def make_summary_plot(flammability_data, x_axis, y_axis, x_label, y_label):
    data = []
    x_axis = x_axis or 'phi'
    y_axis = y_axis or 'Su'
    x_label = x_label or 'Equivalence Ratio'
    y_label = y_label or 'Laminar Flame Speed'

    flammability_data = json.loads(flammability_data)

    if flammability_data is not None:
        flammability_data.pop('_id')
        df = pd.DataFrame.from_dict(flammability_data,
                                    orient='index').transpose()
        x_data = list(df[(df.Xi == 0) & (df.Flammable == 1)][x_axis])
        y_data = list(df[(df.Xi == 0) & (df.Flammable == 1)][y_axis])

        data = [
            dict(
                type="scatter",
                mode="lines+markers",
                x=x_data,
                y=y_data
            )
        ]

    layout = copy.deepcopy(plot_layout)
    layout['title'] = f'{y_label} vs. {x_label}'
    layout['xaxis'] = dict(title={'text': x_label})
    layout['yaxis'] = dict(title={'text': y_label})

    figure = dict(data=data, layout=layout)
    return figure


@app.callback(
    Output('ternary_graph', 'figure'),
    [
        Input('flammability_data', 'children'),
        Input('ternary_dropdown', 'value'),
    ])
def make_ternary_plot(flammability_data, dropdown_value):
    """ Make ternary graph from flammability data. """
    data = []

    if flammability_data and dropdown_value:
        flammability_data = json.loads(flammability_data)

        xf = flammability_data['Xf']
        xa = flammability_data['Xa']
        xi = flammability_data['Xi']
        z = np.array(flammability_data[dropdown_value])

        colorscale = 'Hot'
        ncontours = None
        showscale = True

        if dropdown_value == 'phi':
            # Cap phi values at 2
            for i, value in enumerate(z):
                if value > 2:
                    z[i] = 2

            ncontours = 8
            colorscale = 'Rainbow'

        if dropdown_value == 'Flammable':
            ncontours = 2
            showscale = False

        figure = create_ternary_contour(np.array([xf, xa, xi]), z,
                                        pole_labels=['Fuel', 'Air', 'Inert'],
                                        interp_mode='cartesian',
                                        colorscale=colorscale,
                                        showscale=showscale,
                                        ncontours=ncontours)

        data = figure.to_plotly_json()['data']

        # Clean up
        for item in data:
            item.pop('showlegend', None)

    layout = copy.deepcopy(plot_layout)
    layout['title'] = 'Ternary Contour Plot'
    layout['showlegend'] = False
    layout['ternary'] = dict(
        sum=1,
        aaxis=dict(title='Fuel'),
        baxis=dict(title='Air'),
        caxis=dict(title='Inert'),
        showlegend=False,
        width=700,
    )

    figure = dict(data=data, layout=layout)
    return figure
