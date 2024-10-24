#!/usr/bin/env python3
"""lists all documents in a collection."""
from typing import List
from pymongo.collection import Collection


def list_all(mongo_collection) -> List[dict]:
    """
    Lists all documents in a collection.

    :param mongo_collection: pymongoo collection object
    :return: list of documents otherwise an empty list
    """
    documents = list(mongo_collection.find())
    return documents if documents else []
