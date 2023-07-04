"""Defines Note Enum"""
from Enums import Enum
from Enums.permit_enum import Permit


class Note(Enum):
    """ 
    represents Note enum
    extends Enum from python enum

    Attributes:\n
    PICK_UP = 'PICK_UP' \n
    DROP_OFF = 'DROP_OFF'
    """
    SENT = 'SENT'
    DELIVERED = 'DELIVERED'
    SEEN = 'SEEN'
    DONE = 'DONE'

    def moveOn(self, permit=Permit.READONLY):
        if self == Note.SEEN:
            if Permit.READ_AND_WRITE:
                return Note.DONE
        if self == Note.SENT:
            return Note.DELIVERED
        if self == Note.DELIVERED:
            return Note.SEEN