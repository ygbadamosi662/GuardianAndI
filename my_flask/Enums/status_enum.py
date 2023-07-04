"""Defines Status Enum"""
from Enums import Enum


class Status(Enum):
    """ 
    represents Status enum
    extends Enum from python enum

    Attributes:\n
    ACTIVE = 'ACTIVE' \n
    INACTIVE = 'INACTIVE'
    ACTIVE_PENDING = 'ACTIVE_PENDING'
    INACTIVE_PENDING = 'INACTIVE_PENDING'
    """
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    ACTIVE_PENDING = 'ACTIVE_PENDING'
    INACTIVE_PENDING = 'INACTIVE_PENDING'