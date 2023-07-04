"""Defines Auth Enum"""
from Enums import Enum


class Auth(Enum):
    """ 
    represents Action enum
    extends Enum from python enum

    
    Attributes:\n
    INITIATED = 'INITIATED'\n
    SCHOOL_IN = 'SCHOOL_IN'\n
    SCHOOL_OUT = 'SCHOOL_OUT'\n
    SG_bothPENDING = 'SG_bothPENDING'\n
    SG_oneIn_oneOut = 'SG_oneIn_oneOut'\n
    SG_oneIn_onePending = 'SG_oneIn_onePending'\n
    SG_BOTH_OUT = 'SG_BOTH_OUT'\n
    SG_BOTH_IN = 'BOTH_SG_IN'\n
    IN_TRANSIT = 'IN_TRANSIT'\n
    DONE = 'DONE'\n
    """

    # should go:
    # INITIATED ➡ SCHOOL_IN ➡ SG_bothPENDING ➡ SG_oneIn_onePending ➡ SG_BOTH_IN ➡ IN_TRANSIT ➡ ARRIVED
    #            ⬇                     ⬇                  ⬇
    #         SCHOOL_OUT     SG_OneOut_OnePending ➡ SG_oneIn_oneOut
    #                                   ⬇                   ⬇
    #                             SG_BOTH_OUT             SG_BOTH_OUT


    INITIATED = 'INITIATED'
    SCHOOL_IN = 'SCHOOL_IN'
    SCHOOL_OUT = 'SCHOOL_OUT'
    SG_bothPENDING = 'SG_bothPENDING'
    SG_OneOut_OnePending = 'SG_OneOut_OnePending'
    SG_oneIn_oneOut = 'SG_oneIn_oneOut'
    SG_oneIn_onePending = 'SG_oneIn_onePending'
    SG_BOTH_OUT = 'SG_BOTH_OUT'
    SG_BOTH_IN = 'BOTH_SG_IN'
    IN_TRANSIT = 'IN_TRANSIT'
    ARRIVED = 'ARRIVED'

    def init():
        return Auth.INITIATED
    
    def nextOfInit(self, choice):
        if self == Auth.INITIATED:
            if choice:
                return Auth.SCHOOL_IN
            return Auth.SCHOOL_OUT
        
    def nextOfSchool_in(self):
        if self == Auth.SCHOOL_IN:
            return Auth.SG_bothPENDING
        
    def nextOfSG_bothPending(self, choice):
        if self == Auth.SG_bothPENDING:
            if choice:
                return Auth.SG_oneIn_onePending
            return Auth.SG_OneOut_OnePending
        
    def nextOfSG_OneOut_OnePending(self, choice):
        if self == Auth.SG_OneOut_OnePending:
            if choice:
                return Auth.SG_oneIn_oneOut
            return Auth.SG_BOTH_OUT
        
    def nextOfSG_OneOut_OnePending(self, choice):
        if self == Auth.SG_OneOut_OnePending:
            if choice:
                return Auth.SG_oneIn_oneOut
            return Auth.SG_BOTH_OUT
        
    def nextOfSG_oneIn_oneOut(self, choice):
        self.nextOfSG_OneOut_OnePending(self, False)

    def nextOfSG_oneIn_onePending(self, choice):
        if self == Auth.SG_oneIn_onePending:
            if choice:
                return Auth.SG_BOTH_IN
            return Auth.SG_oneIn_oneOut
        
    def nextOfSG_BOTH_IN(self):
        if self == Auth.SG_BOTH_IN:
            return Auth.IN_TRANSIT
        
    def nextOfIN_TRANSIT(self):
        if self == Auth.IN_TRANSIT:
            return Auth.ARRIVED




    

