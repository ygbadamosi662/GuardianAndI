"""Defines the Utility class"""
from models import storage
from flask_jwt_extended import get_jwt_identity
from repos.guardianRepo import GuardianRepo, Guardian
from repos.schoolRepo import SchoolRepo, School
from global_variables import GUARDIAN, SCHOOL

class Utility():
    """
    Defines Utility class, just for utility functions
    """
    
    session = None
    guardianRepo = GuardianRepo()
    schoolRepo = SchoolRepo()

    def __init__(self):
        self.session = storage.get_session()

    def getInstanceFromJwt(self):
        # decoded = decode_token(jwtToken)
        payload = get_jwt_identity()

        if payload['model'] == GUARDIAN:
            guardian = self.guardianRepo.findByEmail(payload['email'])

            if guardian:
                return guardian
            
        if payload['model'] == SCHOOL:
            school = self.schoolRepo.findByEmail(payload['email'])
               
            if school:
                return school
            
        return None
    
    def persistModel(self, model):
        storage.new(model)
        storage.save()

    

    
util = Utility()  