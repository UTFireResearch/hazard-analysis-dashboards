# -*- coding: utf-8 -*-

import base64
import io
import json

import dash_html_components as html
import dash_table
import pandas as pd

from db.api import find, find_HD


# Constants
CANTERA_GASES = ['CO2', 'CO', 'H2', 'CH4', 'C2H4', 'C2H6', 'C3H8', 'N2', 'O2',
                 'CH3OH']
# Air composition
AIR_SPECIES = {'O2': 1, 'N2': 3.76}


# Ternary graph options
TERNARY_OPTIONS = [{'label': 'Adiabatic Temperature', 'value': 'Tad'},
                   {'label': 'Equivalence Ratio', 'value': 'phi'},
                   {'label': 'Flammability', 'value': 'Flammable'}]

# x-axis options for summary plot
X_AXIS_OPTIONS = [{'label': 'Equivalence Ratio', 'value': 'phi'},
                  {'label': 'Fuel Ratio', 'value': 'Xf'}]

# y-axis options for summary plot
Y_AXIS_OPTIONS = [{'label': 'Equivalence Ratio', 'value': 'phi'},
                  {'label': 'Laminar Flame Speed', 'value': 'Su'},
                  {'label': 'Adiabatic Pressure', 'value': 'Pmax'},
                  {'label': 'Adiabatic Temperature', 'value': 'Tad'}]

# Collection Names
MAIN_COLLECTION = 'main'
FLAMMABILITY_COLLECTION = 'flammability'
INCIDENT_COLLECTION = 'Battery_Incidents'


def _clean_search_dict(search):
    """ Replace 'N/A' values with None in search dict. """
    for key, value in search.items():
        if value == 'N/A':
            search[key] = None


def _get_fuel_species(gases):
    """ Make all non-Cantera gases Propane (C3H8). """
    fuel_species = gases.copy()

    for gas, quantity in gases.items():
        if gas not in CANTERA_GASES:
            fuel_species['C3H8'] += quantity
            fuel_species.pop(gas)

    return fuel_species


def _add_search_filter(search=None):
    """ Add filter to ensure presence of CO2, H2, CH4 or C3H8. """
    search_filter = {
        "$and": [
            {"$or": [{'Gases.CO2': {'$gt': 0}}, {'Gases.H2': {'$gt': 0}},
                     {'Gases.CH4': {'$gt': 0}}, {'Gases.C3H8': {'$gt': 0}}]}
        ]
    }
    if search:
        search_filter['$and'].append(search)

    return search_filter


def make_options(values):
    """ Create list of options from list of values. """
    options = []
    for value in values:
        label = 'N/A' if value == '' else value
        options.append({'label': label, 'value': value})
    return options


def get_main_data():
    """ Get data in main collection in JSON serialized form. """
    search = _add_search_filter()
    cols = {'Publication': 1, 'Format': 1, 'Chemistry': 1, 'Electrolyte': 1,
            'SOC': 1, '_id': 0}
    results = find(collection=MAIN_COLLECTION, search=search, projection=cols)
    data = json.dumps(list(results))
    return data


def get_flammability_data(experiment):
    """ Get flammability data for a selected experiment. """
    id = make_unique_id(experiment)
    results = list(find(collection=FLAMMABILITY_COLLECTION,
                        search={'_id': id}))
    return results[0]

def get_incident_data_lean():
    """Get data in incident collection in JSON serialized form."""
    cols = {'_id':1, 'date.stamp':1, 'place.placeName':1, 'place.location':1, 'incident':1, 'application.appID':1, 'description':1}
    results = find_HD(collection=INCIDENT_COLLECTION, search={"Live": True}, projection=cols)
    # dList = list(results)
    # dFlat = pd.json_normalize(dList)
    # data = pd.DataFrame(dFlat)
    # data = data.rename(columns=
    #         {"incident":"Incident",
    #          "date.stamp": "Date",
    #          "place.location.type": "Type",
    #          "place.location.coordinates": "Coordinates",
    #          "place.placeName": 'Place',
    #          "application.appID": 'appID',
    #          "casualties.killed": 'Killed',
    #          "casualties.injured": 'Injured',
    #         }
    #     )
    data = json.dumps(list(results),default=str)
    return data

def make_unique_id(experiment):
    """ Make id from selected experiment. """
    experiment.pop('Electrolyte')
    experiment.pop('Format')

    _id = []
    for value in experiment.values():
        value = str(value)
        value = value.lower()
        value = value.replace(',', '')
        _id.append('-'.join(value.split()))

    return '-'.join(_id)


def parse_contents(contents, filename, date):
    """ Parse the contents of a csv or xls file. """
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        dash_table.DataTable(
            id='upload_table',
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            fixed_rows={'headers': True, 'data': 0},
            style_table={
                'overflowX': 'scroll',
                'overflowY': 'scroll',
                'maxHeight': '300px',
            }
        ),

        html.Hr(),  # horizontal line
    ])
