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
    # INITIATED ➡ SCHOOL_IN ➡ SG_PENDING ➡ SG_IN ➡ IN_TRANSIT ➡ ARRIVED
    #            ⬇                   ⬇                  
    #         SCHOOL_OUT           SG_OUT                  


    INITIATED = 'INITIATED'
    SCHOOL_IN = 'SCHOOL_IN'
    SCHOOL_OUT = 'SCHOOL_OUT'
    SG_PENDING = 'SG_PENDING'
    SG_OUT = 'SG_OUT'
    SG_IN = 'SG_IN'
    IN_TRANSIT = 'IN_TRANSIT'
    ARRIVED = 'ARRIVED'

    def initiate():
        """sets Auth.INITIATED"""
        return Auth.INITIATED
    
    def nextOfInit(self, choice):
        """
        sets next in sequence according to the should go map, conditionally, 
        choice is a bool, True moves ahead in the sequence and False goes the OUT route
        """
        if self == Auth.INITIATED:
            if choice:
                return Auth.SCHOOL_IN
            return Auth.SCHOOL_OUT
        
    def nextOfSchool_in(self):
        """
        sets next in sequence according to the should go map, conditionally, 
        choice is a bool, True moves ahead in the sequence and False goes the OUT route
        """
        if self == Auth.SCHOOL_IN:
            return Auth.SG_PENDING
        
    def nextOfSG_PENDING(self, choice):
        """
        sets next in sequence according to the should go map, conditionally, 
        choice is a bool, True moves ahead in the sequence and False goes the OUT route
        """
        if self == Auth.SG_PENDING:
            if choice:
                return Auth.SG_IN
            return Auth.SG_OUT
        
    def nextOfSG_IN(self, choice):
        """
        sets next in sequence according to the should go map, conditionally, 
        choice is a bool, True moves ahead in the sequence and False goes the OUT route
        """
        if self == Auth.SG_IN:
            if choice:
                return Auth.IN_TRANSIT
        
    def nextOfIN_TRANSIT(self, choice):
        """
        sets next in sequence according to the should go map, conditionally, 
        choice is a bool, True moves ahead in the sequence and False goes the OUT route
        """
        if self == Auth.IN_TRANSIT:
            if choice:
                return Auth.ARRIVED
            
    def next(self, choice):
        """
        defines one function to call all the mextOf.... functions defined conditionally
        based on the current Auth Enum
        """
        if self == Auth.INITIATED:
            self.nextOfInit(self, choice)
        if self == Auth.SCHOOL_IN:
            self.nextOfSchool_in(self, choice)
        if self == Auth.SG_PENDING:
            self.nextOfSG_PENDING(self, choice)
        if self == Auth.SG_IN:
            self.nextOfSG_IN(self, choice)
        if self == Auth.IN_TRANSIT:
            self.nextOfIN_TRANSIT(self, choice)


    

