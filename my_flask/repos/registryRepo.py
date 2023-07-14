"Defines RegistryRepo class"
from models import storage
from typing import List, Union
from models.registry import Registry
from models.student import Student
from models.school import School
from Enums.status_enum import Status
from Enums.tag_enum import Tag
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError


class RegistryRepo:

    session = None

    def __init__(self):
        self.session = storage.get_session()

    def findByStudent(self, student: Student) -> List[Registry]:
        if student:
            try:
                registries = self.session.query(Registry).filter_by(registry_student=student).all()
                return registries
            except SQLAlchemyError:
                return
            
    def findBySchool(self, school: School) -> List[Registry]:
        if school:
            try:
                registries = self.session.query(Registry).filter_by(registry_school=school).all()
                return registries
            except SQLAlchemyError:
                return
            
    def findByStudentAndSchool(self, student: Student, school: School) -> Registry:
        try:
            registries = self.session.query(Registry).filter(and_(Registry.registry_student == student, 
                                                                Registry.registry_school == school)).first()
            return registries
        except SQLAlchemyError:
            return
        
    def findByStudentAndSchoolAndStatus(self, student: Student, school: School, status: Status) -> Union[List[Registry], Registry]:
        try:
            if status == Status.INACTIVE:
                registries = self.session.query(Registry).filter(and_(Registry.registry_student == student, 
                                                                    Registry.registry_school == school,
                                                                    Registry.status == status)).all()
                return registries
            
            if status == Status.ACTIVE:
                registry = self.session.query(Registry).filter(and_(Registry.registry_student == student, 
                                                                    Registry.registry_school == school,
                                                                    Registry.status == status)).first()
                return registry
        except SQLAlchemyError:
            return 

    def findByStudentAndStatus(self, student: Student, status: Status) -> Union[Registry, List[Registry]]:
        if student:
            try:
                if status == Status.ACTIVE:
                    registry = self.session.query(Registry).filter(and_(Registry.registry_student == student, 
                                                                        Registry.status == status)).first()
                    return registry
                
                if status == Status.ACTIVE:
                    registries = self.session.query(Registry).filter(and_(Registry.registry_student == student, 
                                                                        Registry.status == status)).all()
                    return registries
            except SQLAlchemyError:
                return
            
    def findBySchoolAndStatus(self, school: School, status: Status) -> List[Registry]:
        if school:
            try:
                return self.session.query(Registry).filter(and_(Registry.registry_school == school, 
                                                                    Registry.status == status)).all()
            except SQLAlchemyError:
                return
            
    def pageBySchoolAndStatus(self, school: School, status: Status, page: int) -> List[Registry]:
        try:
            page_size = 10 
            offset = (page - 1) * page_size
            query = self.session.query(Registry).filter(and_(Registry.registry_school == school, 
                                                            Registry.status == status)).limit(page_size).offset(offset)
            return query.all()
        except SQLAlchemyError as err:
            return err._message()
        
    def pageByStudentAndStatus(self, student: Student, status: Status, page: int) -> List[Registry]:
        try:
            page_size = 10 
            offset = (page - 1) * page_size
            query = self.session.query(Registry).filter(and_(Registry.registry_student == student, 
                                                            Registry.status == status)).limit(page_size).offset(offset)
            return query.all()
        except SQLAlchemyError as err:
            print(err._message())
            
    def findAll(self):
        try:
            registries = self.session.query(Registry).all()
            return registries
        except SQLAlchemyError:
            return

    def findById(self, id: int) -> Registry:
        return self.session.query(Registry).filter(Registry.id == id).first()

registry_repo = RegistryRepo()          