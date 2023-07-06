"""Defines the Utility class"""
from models import storage
from flask_jwt_extended import get_jwt_identity
from repos.guardianRepo import GuardianRepo, Guardian
from repos.schoolRepo import SchoolRepo, School
from repos.guardRepo import GuardRepo, Guard
from models.student import Student
from global_variables import GUARDIAN, SCHOOL
from Enums.tag_enum import Tag
from Enums.status_enum import Status

class Utility():
    """
    Defines Utility class, just for utility functions
    """
    
    session = None
    guardianRepo = GuardianRepo()
    schoolRepo = SchoolRepo()
    guardRepo = GuardRepo()

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

    def isGuardian(self, student: Student, guardian: Guardian, andIsSuper=False, andIsActive=False) -> bool:

        """
        defines a function that checks if a user is a guardian to a student
        returns True if guardian is a student guardian
        params:
            student, guardian, 
            andIsSuper: if True,function will return True if the guardian is student's super-guardian
                        returns False otherwise(defaults to False if not set), 
            andIsActive: if True, function will return True if guard is Active, 
                         returns False otherwise(defaults to False if not set)
        """
        guards = self.guardRepo.findByStudent(student)
        returnee = False
        
        if guards:
            for guard in guards:
                if guard.guard_guardian == guardian:
                    returnee = True
                    if andIsSuper:
                        if guard.tag != Tag.SUPER_GUARDIAN:
                            return False
                    if andIsActive:  
                        if guard.status != Status.ACTIVE:     
                            return False

                if returnee:
                    return returnee
            
        return returnee

    def superLimit(self, student: Student) -> bool:
        guards = student.student_guards
        limit = 0

        for guard in guards:
            if (guard.status == Status.ACTIVE) and (guard.tag == Tag.SUPER_GUARDIAN):
                limit = limit + 1

        return limit < 2
    
    def ifStudent(self, student: Student, school: School) -> bool:
        session = storage.get_session()
        school_ish = session.get(School, school.id)
        
        if school_ish.school_students:
            for stud in school_ish.school_students:
                if stud == student:
                    
                    return True
        return False

util = Utility()  