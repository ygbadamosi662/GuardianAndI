"""Defines Permit Enum"""
from Enums import Enum


class Permit(Enum):
    """ 
    represents Permit enum
    extends Enum from python enum

    Attributes:\n
    READONLY = 'READONLY' \n
    READ_AND_WRITE = 'READ_AND_WRITE'
    """
    READONLY = 'READONLY'
    READ_AND_WRITE = 'READ_AND_WRITE'