# -*- coding: utf-8 -*-

import os

from pymongo import MongoClient


DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_URI = (f'mongodb://trejo:{DB_PASSWORD}@ds333238.mlab.com:33238'
          '/heroku_2c1mks3g?retryWrites=false')
DB_NAME = 'heroku_2c1mks3g'


def find(collection, search={}, projection=None):
    """ Find items in a given collection matching a search.

    Parameters
    ----------
    collection : Unicode
        Name of te collection to search in.
    search : Dict
        The search dictionary with the search parameters.
    projection : Dict
        projection dictionary to specify or restrict fields to return.

    Returns
    -------
    List
        List of items in the collection.
    """
    client = MongoClient(DB_URI)
    db = client[DB_NAME]

    return db[collection].find(search, projection)


def get_unique(collection, field, search={}):
    """ Get all unique values for a given field in a collection.

    Parameters
    ----------
    collection : Unicode
        Name of te collection to search in.
    field : Unicode
        Name of the field to retrieve.
    search : Dict
        The search dictionary with the search parameters.

    Returns
    -------
    List
        List of unique values for a given field in a collection.
    """
    client = MongoClient(DB_URI)
    db = client[DB_NAME]

    return db[collection].find(search).distinct(field)
