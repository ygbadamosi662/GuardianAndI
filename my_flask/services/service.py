"""Defines Service class"""
from models import storage


class Service:
    session = None
    
    def __init__(self):
        self.session = storage.get_session()