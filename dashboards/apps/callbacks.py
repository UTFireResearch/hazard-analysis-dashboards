# -*- coding: utf-8 -*-

import copy
import json

from dash.dependencies import Input, Output, State
import pandas as pd

from app import app
from .controls import GAS_COLORS, plot_layout
from db.api import get_unique
from .util import (
    _clean_search_dict, _get_fuel_species, _add_search_filter, MAIN_COLLECTION,
    make_options
)


@app.callback(
    [
        Output('vent_ref_pub', 'options'),
        Output('vent_cell_types', 'options'),
        Output('vent_cell_chemistry', 'options'),
        Output('vent_cell_electrolytes', 'options'),
        Output('vent_cell_soc', 'options')],
    [
        Input('db_data', 'children'),
        Input('vent_ref_pub', 'value'),
        Input('vent_cell_types', 'value'),
        Input('vent_cell_chemistry', 'value'),
        Input('vent_cell_electrolytes', 'value'),
        Input('vent_cell_soc', 'value')
    ])
def update_dropdowns(data, publication, cell_type, chemistry, electrolyte,
                     soc):
    """ Update gas dropdown databa based on selections. """
    df = pd.DataFrame(json.loads(data))

    if publication:
        df = df[df['Publication'] == publication]
    if cell_type:
        df = df[df['Format'] == cell_type]
    if chemistry:
        df = df[df['Chemistry'] == chemistry]
    if electrolyte:
        df = df[df['Electrolyte'] == electrolyte]
    if soc:
        df = df[df['SOC'] == soc]

    fields = ['Publication', 'Format', 'Chemistry', 'Electrolyte', 'SOC']
    results = []
    for field in fields:
        result = list(df[field].unique())
        results.append(make_options(result))
    return results


@app.callback(
    [
        Output('vent_ref_pub', 'value'),
        Output('vent_cell_types', 'value'),
        Output('vent_cell_chemistry', 'value'),
        Output('vent_cell_electrolytes', 'value'),
        Output('vent_cell_soc', 'value')],
    [
        Input('clear_button', 'n_clicks')],
    [
        State('vent_ref_pub', 'value'),
        State('vent_cell_types', 'value'),
        State('vent_cell_chemistry', 'value'),
        State('vent_cell_electrolytes', 'value'),
        State('vent_cell_soc', 'value')]
)
def clear_dropdowns(n_clicks, publication, cell_type, chemistry, electrolyte,
                    soc):
    """ Clear dropdown menus. """
    if n_clicks > 0:
        return [], [], [], [], []
    else:
        return publication, cell_type, chemistry, electrolyte, soc


@app.callback(
    Output('selected_experiment', 'children'),
    [
        Input('vent_ref_pub', 'value'),
        Input('vent_cell_types', 'value'),
        Input('vent_cell_chemistry', 'value'),
        Input('vent_cell_electrolytes', 'value'),
        Input('vent_cell_soc', 'value')
    ],
    [State('selected_experiment', 'children')])
def update_selected_experiment(publication, cell_type, chemistry,
                               electrolyte, soc, current_experiment):
    """ Update search experiment data based dropdown selections. """
    if all([publication, cell_type, chemistry, soc]):
        dct = {'Publication': publication, 'Format': cell_type,
               'Chemistry': chemistry, 'Electrolyte': electrolyte, 'SOC': soc}
        search = json.dumps(dct)
    elif any([publication, cell_type, chemistry, electrolyte, soc]):
        search = current_experiment
    else:
        search = None

    return search


@app.callback(
    Output('gas_composition', 'children'),
    [Input('selected_experiment', 'children')])
def update_gases(selected_experiment):
    """ Update gas data based on dropdown selections. """
    if selected_experiment:
        search = json.loads(selected_experiment)
        _clean_search_dict(search)
        search = _add_search_filter(search)
        values = get_unique(MAIN_COLLECTION, field='Gases', search=search)
        gases = values[-1] if values else ''
        return json.dumps(gases)


@app.callback(
    Output("composition_plot", "figure"),
    [Input("gas_composition", "children")],
)
def make_gas_composition_plot(gases):
    """ Create gas composition plot. """
    gases = json.loads(gases) if gases else {}
    data = []

    if gases:
        fuel_species = _get_fuel_species(gases)

        data = [
            dict(
                type="pie",
                labels=[key for key, val in fuel_species.items() if val > 0],
                values=[val for val in fuel_species.values() if val > 0],
                name="Fuel Species Composition",
                textinfo="label",
                textfont=dict(size="18", color="#FFFFFF"),
                hoverinfo="label+percent",
                marker=dict(colors=[GAS_COLORS[gas] for gas in fuel_species]),
            ),
        ]

    layout = copy.deepcopy(plot_layout)
    layout["title"] = "Fuel Species Composition"
    layout["margin"] = dict(l=30, r=30, b=20, t=40)  # noqa
    layout["legend"] = dict(
        font=dict(color="#777777", size="12"),
        orientation="h",
    )

    figure = dict(data=data, layout=layout)
    return figure
