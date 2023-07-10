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
    SG_PENDING = 'SG_PENDING'\n
    SG_OUT = 'SG_OUT'\n
    SG_IN = 'SG_IN'\n
    IN_TRANSIT = 'IN_TRANSIT'\n
    ARRIVED = 'ARRIVED'\n
    """

    # should go:
    # INITIATED ➡ SCHOOL_IN ➡ SG_IN ➡ IN_TRANSIT ➡ ARRIVED
    #            ⬇                ⬇                      ⬇                             
    #         SCHOOL_OUT        SG_OUT                FALSE  


    INITIATED = 'INITIATED'
    SCHOOL_IN = 'SCHOOL_IN'
    SCHOOL_OUT = 'SCHOOL_OUT'
    SG_OUT = 'SG_OUT'
    SG_IN = 'SG_IN'
    READY = 'READY'
    CONFLICT = 'CONFLICT'
    IN_TRANSIT = 'IN_TRANSIT'
    ARRIVED = 'ARRIVED'
    FALSE = 'FALSE'

    def initiate():
        """sets Auth.INITIATED"""
        return Auth.INITIATED
    
    def nextOfInit(self, choice: bool) -> Enum:
        """
        sets next in sequence according to the should go map, conditionally, 
        choice is a bool, True moves ahead in the sequence and False goes the OUT route
        """
        if self == Auth.INITIATED:
            if choice:
                return Auth.SCHOOL_IN
            return Auth.SCHOOL_OUT
        
    def nextOfSchool_in(self, choice: bool) -> Enum:
        """
        sets next in sequence according to the should go map, conditionally, 
        choice is a bool, True moves ahead in the sequence and False goes the OUT route
        """
        if self == Auth.SCHOOL_IN:
            if choice:
                return Auth.SG_IN
            return Auth.SCHOOL_OUT
        
    def nextOfSG_IN(self, choice: bool) -> Enum:
        """
        sets next in sequence according to the should go map, conditionally, 
        choice is a bool, True moves ahead in the sequence and False goes the OUT route
        """
        if self == Auth.SG_IN:
            if choice:
                return Auth.READY
            return Auth.CONFLICT
        
    def nextOfREADY(self) -> Enum:
        """
        sets next in sequence according to the should go map
        in this case it returns Auth.IN_TRANSIT, no backsies
        """
        if self == Auth.READY:
            return Auth.IN_TRANSIT
        
    def nextOfIN_TRANSIT(self, choice: bool) -> Enum:
        """
        sets next in sequence according to the should go map, conditionally, 
        choice is a bool, True moves ahead in the sequence and False goes the OUT route
        """
        if self == Auth.IN_TRANSIT:
            if choice:
                return Auth.ARRIVED
            return Auth.FALSE
            
    def next(self, choice: bool) -> Enum:
        """
        defines one function to call all the mextOf.... functions defined conditionally
        based on the current Auth Enum
        """
        if self == Auth.INITIATED:
            return self.nextOfInit(choice)
        if self == Auth.SCHOOL_IN:
            return self.nextOfSchool_in(choice)
        if self == Auth.SG_IN:
            return self.nextOfSG_IN(choice)
        if self == Auth.IN_TRANSIT:
            return self.nextOfIN_TRANSIT(choice)


    

