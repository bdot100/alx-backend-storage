#!/usr/bin/env python3
"""
a Python function that lists all documents in a collection:

Prototype: def list_all(mongo_collection):
Return an empty list if no document in the collection
mongo_collection will be the pymongo collection object
"""

#import pymongo


def list_all(mongo_collection):
    """
    This function lists documents in a collection
    """
    if not mongo_collection:
        return []
    return list(mongo_collection.find())
