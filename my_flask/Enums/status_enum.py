"""Defines Status Enum"""
from Enums import Enum


class Status(Enum):
    """ 
    represents Status enum
    extends Enum from python enum

    Attributes:\n
    ACTIVE = 'ACTIVE'\n
    INACTIVE = 'INACTIVE'\n
    ACTIVE_PENDING = 'ACTIVE_PENDING' #waiting for linked guardian conformation\n
    ACTIVE_SYELLOW = 'ACTIVE_SYELLOW' #waiting for school confirmation\n
    ACTIVE_GYELLOW = 'ACTIVE_GYELLOW' #waiting for guardian confirmation\n
    INACTIVE_SYELLOW = 'INACTIVE_SYELLOW' #waiting for school confirmation\n
    INACTIVE_GYELLOW = 'INACTIVE_GYELLOW' #waiting for guardian confirmation\n
    """
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    ACTIVE_PENDING = 'ACTIVE_PENDING' #waiting for linked guardian conformation
    ACTIVE_SYELLOW = 'ACTIVE_SYELLOW' #waiting for school confirmation
    ACTIVE_GYELLOW = 'ACTIVE_GYELLOW' #waiting for guardian confirmation
    INACTIVE_SYELLOW = 'INACTIVE_SYELLOW' #waiting for school confirmation
    INACTIVE_GYELLOW = 'INACTIVE_GYELLOW' #waiting for guardian confirmation
