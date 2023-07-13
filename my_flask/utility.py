"""Defines the Utility class"""
from models import storage
from sqlalchemy import exists
from typing import Union, List
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import get_jwt_identity
from repos.guardianRepo import guardian_repo, Guardian
from repos.schoolRepo import school_repo, School
from repos.guardRepo import guard_repo, Guard
from models.pick_and_drop import PickAndDrop
from repos.pick_and_dropRepo import pad_repo
from repos.registryRepo import registry_repo, Registry
from Enums.auth_enum import Auth
from Enums.action_enum import Action
from models.student import Student
from global_variables import GUARDIAN, SCHOOL, PICK_AND_DROP, REGISTRY, GUARD, STUDENT
from Enums.tag_enum import Tag
from Enums.status_enum import Status

class Utility():
    """
    Defines Utility class, just for utility functions
    """
    
    session = None
    guardianRepo = guardian_repo
    schoolRepo = school_repo
    guardRepo = guard_repo
    who_called = ''
    keep = {}

    def __init__(self):
        self.session = storage.get_session()

    def getInstanceFromJwt(self):
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
        self.discard()
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
        self.discard()
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
        self.discard()
        guards = student.student_guards
        limit = 0

        for guard in guards:
            if (guard.status == Status.ACTIVE) and (guard.tag == Tag.SUPER_GUARDIAN):
                limit = limit + 1

        return limit < 2
    
    def ifStudent(self, student: Student, school: School) -> bool:
        self.discard()
        session = storage.get_session()
        school_ish = session.get(School, school.id)
        
        if school_ish.school_students:
            for stud in school_ish.school_students:
                if stud == student:
                    
                    return True
        return False

    def validateRegistry(self, registry: Registry) -> bool:
        self.discard()
        if registry:
            return registry.status == Status.ACTIVE
        
    def validateGuard(self, guard: Guard, keep: bool = False) -> bool:
        if guard:
            return guard.status == Status.ACTIVE

    def discard(self, identity: str = ''):
        if identity == '':
            self.keep = {}
        
        self.keep[identity] = None

    def closeSession(self):
        self.discard()
        storage.close()

    def monitor(self, identity: str):
        self.who_called = identity

    def if_i_called(self, identity: str) -> bool:
        return self.who_called == identity
    
    def keep_it(self, treasure):
        self.keep[self.who_called] = treasure

    def get_keep(self, identity: str):
        if self.if_i_called(identity):
            return self.keep[identity]

    def check_for_active_registry_pad(self, registry: Registry, keep: bool = False) -> Union[bool, PickAndDrop]:
        if keep:
            self.monitor('check_for_active_registry_pad')

        if registry:
            pad = pad_repo.findOngoingPadByRegistry(registry)
            if pad:
                if keep:
                    self.keep_it(pad)
                    if pad:
                        return True
                    return False
                
                return pad
            
            return False
        
    def check_for_active_guard_pad(self, guard: Guard, keep: bool = False) -> Union[bool, PickAndDrop]:
        if keep:
            self.monitor('check_for_active_registry_pad')

        if guard:
            pad = pad_repo.findOngoingPadByRegistry(guard)
            if pad:
                if keep:
                    self.keep['check_for_active_registry_pad'] = pad
                    if pad:
                        return True
                    return False
                
                return pad
            
            return False

    def pad_validate_school(self, pad: PickAndDrop, school: School) -> bool:
        if pad and school:
            return pad.PAD_registry.registry_school == school
        
    def pad_validate_guardian(self, pad: PickAndDrop, guardian: Guardian, who: str = 'all') -> bool:
        if not pad or not guardian:
            return False
        
        if who == 'all':
            guardians = self.get_pad_guardians(pad)

        if who == 'super':
            guardians = self.get_pad_guardians(pad, Tag.SUPER_GUARDIAN)

        if who == 'school':
             guardians = self.get_pad_guardians(pad, Tag.SCHOOL_GUARDIAN)   

        if who == 'aux':
             guardians = self.get_pad_guardians(pad, Tag.AUXILLARY_GUARDIAN)

        for pad_guardian in guardians:
            if pad_guardian == guardian:
                return True
            
        return False

    def get_pad_guardians(self, pad: PickAndDrop, tag: Tag = None) -> List[Guardian]:
        
        if pad:
            if tag == None:
                guards = guard_repo.findByStudentAndStatus(pad.PAD_guard.guard_student, Status.ACTIVE)
                if guards:
                    return [guard.guard_guardian for guard in guards]
            
            guards = guard_repo.findByStudentAndStatusAndTag(pad.PAD_guard.guard_student, Status.ACTIVE, tag)
            return [guard.guard_guardian for guard in guards]
        
    def validate_table_integrity(self, email: str, model: str) -> bool:
        if model == SCHOOL:
            exists_query = self.session.query(exists().where(School.email == email))

        if model == GUARDIAN:    
            exists_query = self.session.query(exists().where(Guardian.email == email))

        if model == STUDENT:
            exists_query = self.session.query(exists().where(Student.email == email))

        return self.session.scalar(exists_query)

    def take_string_give_authEnum(self, filter: str) -> Auth:
        if filter == 'conflict':
            return Auth.CONFLICT
        if filter == 'initiated':
            return Auth.INITIATED
        if filter == 'school in':
            return Auth.SCHOOL_IN
        if filter == 'school out':
            return Auth.SCHOOL_OUT
        if filter == 'sg in':
            return Auth.SG_IN
        if filter == 'sg out':
            return Auth.SG_OUT
        if filter == 'in transit':
            return Auth.IN_TRANSIT
        if filter == 'arrived':
            return Auth.ARRIVED
        if filter == 'ready':
            return Auth.READY
        if filter == 'resolved':
            return Auth.ARRIVED

    def take_string_give_actionEnum(self, act: str) ->Action:
        if act == 'drop':
            return Action.DROP_OFF
        if act == 'pick':
            return Action.PICK_UP
    
    def get_student_guardians(self, student: Student, tag: Tag, status: Status) -> List[Guardian]:
        try:
            if student and tag and status:
                guards = guard_repo.findByStudentAndStatusAndTag(student, status, tag)

                return [guard.guard_guardian for guard in guards]
        except SQLAlchemyError as err:
            print(err._message())

util = Utility()  