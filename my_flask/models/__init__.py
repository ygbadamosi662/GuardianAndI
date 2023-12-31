#!/usr/bin/python3

"""
    Initialize the storage module
    imports enum files from Enums folder
"""
from models.engine import db_storage


storage = db_storage.DBStorage()
storage.reload()
    
__all__ = ["guard", "guardian", "student", "school", "pick_and_drop"]