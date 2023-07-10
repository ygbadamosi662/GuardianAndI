"""Defines Tag Enum"""
from Enums import Enum


class Tag(Enum):
    """ 
    represents Tag enum
    extends Enum from python enum

    Attributes:\n
    SUPER_GUARDIAN = 'SUPER_GUARDIAN'\n
    AUXILLARY_GUARDIAN = 'AUXILLARY_GUARDIAN'
    """
    SUPER_GUARDIAN = 'SUPER_GUARDIAN'
    AUXILLARY_GUARDIAN = 'AUXILLARY_GUARDIAN'
    SCHOOL_GUARDIAN = 'SCHOOL_GUARDIAN'