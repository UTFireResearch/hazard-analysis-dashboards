# -*- coding: utf-8 -*-

import json

from db.api import find

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


def make_unique_id(experiment):
    """ Make id from selected experiment. """
    experiment.pop('Electrolyte')
    experiment.pop('Format')

    id = []
    for value in experiment.values():
        value = str(value)
        value = value.lower()
        value = value.replace(',', '')
        id.append('-'.join(value.split()))

    return '-'.join(id)
