#!/usr/bin/python3

"""
    Initialize the storage module
"""

from models.engine.db_storage import DBStorage


storage = DBStorage()
storage.reload()
