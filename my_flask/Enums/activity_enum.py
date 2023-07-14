"""Defines Activity Enum"""
from Enums import Enum
from Enums.permit_enum import Permit


class Activity(Enum):
    """ 
    represents Note enum
    extends Enum from python enum

    Attributes:\n
    SENT = 'SENT'\n
    DELIVERED = 'DELIVERED'\n
    SEEN = 'SEEN'\n
    DONE = 'DONE'
    """
    SENT = 'SENT'
    DELIVERED = 'DELIVERED'
    SEEN = 'SEEN'
    DONE = 'DONE'

    def moveOn(self, permit=Permit.READONLY):
        if self == Activity.SEEN:
            if Permit.READ_AND_WRITE:
                return Activity.DONE
        if self == Activity.SENT:
            return Activity.DELIVERED
        if self == Activity.DELIVERED:
            return Activity.SEEN