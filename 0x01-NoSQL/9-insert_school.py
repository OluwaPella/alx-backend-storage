#!/usr/bin/env python3
"""
Python function that inserts a new document
"""
def insert_school(mongo_collection, **kwargs):
    """
    """
    return mongo_collection.insert_one(kwargs).inserted_id