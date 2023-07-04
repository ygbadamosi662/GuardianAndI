"""Defines the Utility class"""
from models import storage
from flask_jwt_extended import get_jwt_identity
from models.guardian import Guardian
from models.school import School
from global_variables import GUARDIAN, SCHOOL

class Utility():
    
    session = None

    def __init__(self):
        self.session = storage.get_session()

    def getInstanceFromJwt(self, instance):
        # decoded = decode_token(jwtToken)
        payload = get_jwt_identity()

        if instance == GUARDIAN:
            guardian = self.session.query(Guardian).filter_by(email=payload['email']).first()

            if guardian:
                return guardian
            
        if instance == SCHOOL:
            if payload['model'] != SCHOOL:
                return False 
            
            school = self.session.query(School).filter_by(email=payload['email']).first()
               

            if school:
                return school
            
        return None
    

    
util = Utility()  