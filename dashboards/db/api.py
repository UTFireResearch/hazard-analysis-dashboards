# -*- coding: utf-8 -*-

import os

from pymongo import MongoClient


DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_USER = os.environ.get('DB_USER')
DB_NAME = os.environ.get('DB_NAME')
DB_URI = (f'mongodb+srv://{DB_USER}:{DB_PASSWORD}@cluster-27rhpgwj.lojyr.mongodb.net/heroku_27rhpgwj?retryWrites=true&w=majority')
#DB_URI = (f'mongodb://{DB_USER}:{DB_PASSWORD}@ds045897.mlab.com:45897'
          #f'/{DB_NAME}?retryWrites=false')


def insert_data(collection, dct):
    """ Add a single data entry to database.

    Parameters
    ----------
    collection : Unicode
        Name of the collection to insert data.
    dct : Dict
        The data to add to the specified collection.

    Returns
    -------
    Int
        The id of the data inserted.
    """
    client = MongoClient(DB_URI)
    db = client[DB_NAME]

    post_id = db[collection].insert_one(dct).inserted_id
    return post_id


def find(collection, search={}, projection=None):
    """ Find items in a given collection matching a search.

    Parameters
    ----------
    collection : Unicode
        Name of the collection to search in.
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
        Name of the collection to search in.
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
