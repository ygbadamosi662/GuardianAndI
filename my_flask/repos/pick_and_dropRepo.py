"Defines PickAndDropRepo class"
from models import storage
from typing import List, Union
from models.guard import Guard
from models.school import School
from models.guardian import Guardian
from models.student import Student
from models.pick_and_drop import PickAndDrop
from models.registry import Registry
from Enums.auth_enum import Auth
from Enums.action_enum import Action
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError


class PickAndDropRepo:

    session = None

    def __init__(self):
        self.session = storage.get_session()

    # def findOngoingPadByRegistry(self, reg: Registry) -> PickAndDrop:
    #     if reg:
    #         query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_registry == reg, PickAndDrop.auth != Auth.ARRIVED, PickAndDrop.auth != Auth.FALSE, PickAndDrop.auth != Auth.SCHOOL_OUT, PickAndDrop.auth != Auth.SG_OUT)

    #         return query.all()

    # byRegistry  
    def findOngoingPadByRegistry(self, reg: Registry) -> PickAndDrop:
        if reg:
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_registry == reg, ~PickAndDrop.auth.in_([Auth.ARRIVED, Auth.CONFLICT, Auth.SCHOOL_OUT, Auth.SG_OUT]))

            return query.first()
        
    def pageByRegistryAndAuth(self, registry: Registry, auth: Auth, page: int) -> List[PickAndDrop]:
        if registry and auth and page:
            page_size = 10 
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_registry == registry, 
                                                            PickAndDrop.auth == auth).limit(page_size).offset(offset)
            return query.all()
        
    def pageUnresolvedPadByRegistry(self, registry: Registry, page: int) -> List[PickAndDrop]:
        if registry and page:
            page_size = 10 
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_registry == registry, 
                                                            PickAndDrop.auth == Auth.SG_OUT, PickAndDrop.auth == Auth.SCHOOL_OUT, PickAndDrop.auth == Auth.CONFLICT).limit(page_size).offset(offset)
            return query.all()

    def pageUnresolvedPadByRegistryAndAction(self, registry: Registry, action: Action, page: int) -> List[PickAndDrop]:
        if registry and action and page:
            page_size = 10 
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_registry == registry, PickAndDrop.action == action, PickAndDrop.auth == Auth.SG_OUT, PickAndDrop.auth == Auth.SCHOOL_OUT, PickAndDrop.auth == Auth.CONFLICT).limit(page_size).offset(offset)

            return query.all()
        
    def pageByRegistryAndAuthAndAction(self, registry: Registry, auth: Auth, action: Action, page: int) -> List[PickAndDrop]:
        if registry and auth and action:
            page_size = 10 
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_registry == registry, PickAndDrop.action == action, PickAndDrop.auth == auth).limit(page_size).offset(offset)
            return query.all()


    # byGuard
    def findOngoingPadByGuard(self, guard: Guard) -> PickAndDrop:
        if guard:
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_guard == guard, PickAndDrop.auth != Auth.ARRIVED, PickAndDrop.auth != Auth.CONFLICT, PickAndDrop.auth != Auth.SCHOOL_OUT, PickAndDrop.auth != Auth.SG_OUT)

            return query.first()
        
    def pageByGuardAndAuth(self, guard: Guard, auth: Auth, page: int) -> List[PickAndDrop]:
        if guard and auth and page:
            page_size = 10 
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_guard == guard, 
                                                            PickAndDrop.auth == auth).limit(page_size).offset(offset)
            return query.all()
        
    def pageUnresolvedPadByGuard(self, guard: Guard, page: int) -> List[PickAndDrop]:
        if guard and page:
            page_size = 10 
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_guard == guard, 
                                                            PickAndDrop.auth == Auth.SG_OUT, PickAndDrop.auth == Auth.SCHOOL_OUT, PickAndDrop.auth == Auth.CONFLICT).limit(page_size).offset(offset)
            return query.all()
        
    def pageUnresolvedPadByGuardAndAction(self, guard: Guard, action: Action, page: int) -> List[PickAndDrop]:
        if guard and action and page:
            page_size = 10 
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_guard == guard, PickAndDrop.action == action, PickAndDrop.auth == Auth.SG_OUT, PickAndDrop.auth == Auth.SCHOOL_OUT, PickAndDrop.auth == Auth.CONFLICT).limit(page_size).offset(offset)

            return query.all()
        
    def pageByGuardAndAuthAndAction(self, guard: Guard, auth: Auth, action: Action, page: int) -> List[PickAndDrop]:
        if guard and auth and action and page:
            page_size = 10 
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_guard == guard, PickAndDrop.action == action, PickAndDrop.auth == auth).limit(page_size).offset(offset)
            return query.all()


    # byGuardian  
    def findOngoingPadByGuardian(self, guardian: Guardian) -> List[PickAndDrop]:
        if guardian:
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_guard.has(Guard.guard_guardian == guardian), PickAndDrop.auth != Auth.ARRIVED, PickAndDrop.auth != Auth.CONFLICT, PickAndDrop.auth != Auth.SCHOOL_OUT, PickAndDrop.auth != Auth.SG_OUT)

            return query.all()
        
    def pageOngoingPadByGuardian(self, guardian: Guardian, page: int) -> List[PickAndDrop]:
        if guardian and page:
            page_size = 10 
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_guard.has(Guard.guard_guardian == guardian), PickAndDrop.auth != Auth.ARRIVED, PickAndDrop.auth != Auth.CONFLICT, PickAndDrop.auth != Auth.SCHOOL_OUT, PickAndDrop.auth != Auth.SG_OUT).limit(page_size).offset(offset)

            return query.all()
        
    def pageByGuardianAndAuth(self, guardian: Guardian, auth: Auth, page: int) -> List[PickAndDrop]:
        if guardian and auth and page:
            
            page_size = 10
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(
                PickAndDrop.PAD_guard.has(Guard.guard_guardian == guardian),
                PickAndDrop.auth != Auth.ARRIVED,
                PickAndDrop.auth != Auth.CONFLICT,
                PickAndDrop.auth != Auth.SCHOOL_OUT,
                PickAndDrop.auth != Auth.SG_OUT
            ).limit(page_size).offset(offset)

            return query.all()
        
    def pageUnresolvedPadByGuardian(self, guardian: Guardian, page: int) -> List[PickAndDrop]:
        if guardian and page:
            page_size = 10 
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_guard.has(Guard.guard_guardian == guardian), PickAndDrop.auth == Auth.SG_OUT, PickAndDrop.auth == Auth.SCHOOL_OUT, PickAndDrop.auth == Auth.CONFLICT).limit(page_size).offset(offset)
            return query.all()
        
    def pageUnresolvedPadByGuardianAndAction(self, guardian: Guardian, action: Action, page: int) -> List[PickAndDrop]:
        if guardian and action and page:
            page_size = 10 
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_guard.guard_guardian_id == guardian.id, PickAndDrop.action == action, PickAndDrop.auth == Auth.SG_OUT, PickAndDrop.auth == Auth.SCHOOL_OUT, PickAndDrop.auth == Auth.CONFLICT).limit(page_size).offset(offset)

            return query.all()
        
    def pageByGuardianAndAuthAndAction(self, guardian: Guardian, auth: Auth, action: Action, page: int) -> List[PickAndDrop]:
        if guardian and auth and action and page:
            page_size = 10 
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_guard.has(Guard.guard_guardian == guardian), PickAndDrop.action == action, PickAndDrop.auth == auth).limit(page_size).offset(offset)

            return query.all()
        
    def pageOngoingPadByGuardianAndAction(self, guardian: Guardian, action: Action, page: int) -> List[PickAndDrop]:
        if guardian and action and page:
            page_size = 10 
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_guard.has(Guard.guard_guardian == guardian), PickAndDrop.action == action, PickAndDrop.auth != Auth.ARRIVED, PickAndDrop.auth != Auth.CONFLICT, PickAndDrop.auth != Auth.SCHOOL_OUT, PickAndDrop.auth != Auth.SG_OUT).limit(page_size).offset(offset)

            return query.all()
        
    def pageByGuardianAndAction(self, guardian: Guardian, action: Action, page: int) -> List[PickAndDrop]:
        if guardian and action and page:
            page_size = 10 
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_guard.has(Guard.guard_guardian == guardian), PickAndDrop.action == action).limit(page_size).offset(offset)

            return query.all()
        
    def pageByGuardian(self, guardian: Guardian, page: int) -> List[PickAndDrop]:
        if guardian and page:
            page_size = 10 
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_guard.has(Guard.guard_guardian == guardian)).limit(page_size).offset(offset)

            return query.all()


    # byiD
    def findById(self, id: int) -> PickAndDrop:
        return self.session.query(PickAndDrop).filter_by(id=id).first()
    
    
    # bySchool
    def pageBySchoolAndAuth(self, school: School, auth: Auth, page: int) -> List[PickAndDrop]:
        if school and auth and page:
            page_size = 10 
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_registry.has(Registry.registry_school == school), PickAndDrop.auth == auth).limit(page_size).offset(offset)
            return query.all()
        
    def pageUnresolvedPadBySchool(self, school: School, page: int) -> List[PickAndDrop]:
        if school and page:
            page_size = 10 
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_registry.has(Registry.registry_school == school), PickAndDrop.auth == Auth.SG_OUT, PickAndDrop.auth == Auth.SCHOOL_OUT, PickAndDrop.auth == Auth.CONFLICT).limit(page_size).offset(offset)
            return query.all()
        
    def pageOngoingPadBySchool(self, school: School, page: int) -> List[PickAndDrop]:
        if school and page:
            page_size = 10 
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_registry.has(Registry.registry_school == school), PickAndDrop.auth != Auth.ARRIVED, PickAndDrop.auth != Auth.CONFLICT, PickAndDrop.auth != Auth.SCHOOL_OUT, PickAndDrop.auth != Auth.SG_OUT).limit(page_size).offset(offset)

            return query.all()
        
    def pageUnresolvedPadBySchoolAndAction(self, school: School, action: Action, page: int) -> List[PickAndDrop]:
        if school and action and page:
            page_size = 10 
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_registry.has(Registry.registry_school == school), PickAndDrop.action == action, PickAndDrop.auth == Auth.SG_OUT, PickAndDrop.auth == Auth.SCHOOL_OUT, PickAndDrop.auth == Auth.CONFLICT).limit(page_size).offset(offset)

            return query.all()
        
    def pageBySchoolAndAuthAndAction(self, school: School, auth: Auth, action: Action, page: int) -> List[PickAndDrop]:
        if school and auth and action and page:
            page_size = 10 
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(and_(PickAndDrop.PAD_registry.has(Registry.registry_school == school), PickAndDrop.action == action, PickAndDrop.auth == auth)).limit(page_size).offset(offset)

            return query.all()
        
    def pageOngoingPadBySchoolAndAction(self, school: School, action: Action, page: int) -> List[PickAndDrop]:
        if school and action and page:
            page_size = 10 
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_registry.has(Registry.registry_school == school), PickAndDrop.action == action, PickAndDrop.auth != Auth.ARRIVED, PickAndDrop.auth != Auth.CONFLICT, PickAndDrop.auth != Auth.SCHOOL_OUT, PickAndDrop.auth != Auth.SG_OUT).limit(page_size).offset(offset)

            return query.all()
        
    def pageBySchoolAndAction(self, school: School, action: Action, page: int) -> List[PickAndDrop]:
        if school and action and page:
            page_size = 10 
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_registry.has(Registry.registry_school == school), PickAndDrop.action == action).limit(page_size).offset(offset)

            return query.all()
        
    def pageBySchool(self, school: School, page: int) -> List[PickAndDrop]:
        if school and page:
            page_size = 10 
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_registry.has(Registry.registry_school == school)).limit(page_size).offset(offset)

            return query.all()


    # byStudent
    def pageByStudentAndAuth(self, student: Student, auth: Auth, page: int) -> List[PickAndDrop]:
        if student and auth and page:
            page_size = 10
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_registry.has(Registry.registry_student == student), PickAndDrop.auth == auth).limit(page_size).offset(offset)

            return query.all()
        
    def pageUnresolvedPadByStudent(self, student: Student, page: int) -> List[PickAndDrop]:
        if student and page:
            page_size = 10 
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_registry.has(Registry.registry_student == student), PickAndDrop.auth == Auth.SG_OUT, PickAndDrop.auth == Auth.SCHOOL_OUT, PickAndDrop.auth == Auth.CONFLICT).limit(page_size).offset(offset)
            return query.all()
        
    def pageUnresolvedPadByStudentAndAction(self, student: Student, action: Action, page: int) -> List[PickAndDrop]:
        if student and action and page:
            page_size = 10 
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_registry.has(Registry.registry_student == student), PickAndDrop.action == action, PickAndDrop.auth == Auth.SG_OUT, PickAndDrop.auth == Auth.SCHOOL_OUT, PickAndDrop.auth == Auth.CONFLICT).limit(page_size).offset(offset)

            return query.all()
        
    def pageByStudentAndAuthAndAction(self, student: Student, auth: Auth, action: Action, page: int) -> List[PickAndDrop]:
        if student and auth and action and page:
            page_size = 10
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_registry.has(Registry.registry_student == student), PickAndDrop.action == action, PickAndDrop.auth == auth).limit(page_size).offset(offset)

            return query.all()
        
    def pageByStudentAndAction(self, student: Student, action: Action, page: int) -> List[PickAndDrop]:
        if student and action and page:
            page_size = 10 
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_registry.has(Registry.registry_student == student), PickAndDrop.action == action).limit(page_size).offset(offset)

            return query.all()

    def pageByStudent(self, student: Student, page: int) -> List[PickAndDrop]:
        if student and page:
            page_size = 10 
            offset = (page - 1) * page_size
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_registry.has(Registry.registry_student == student)).limit(page_size).offset(offset)

            return query.all()


pad_repo = PickAndDropRepo()