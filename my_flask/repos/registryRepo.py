"Defines RegistryRepo class"
from models import storage
from models.registry import Registry
from models.student import Student
from models.school import School
from Enums.status_enum import Status
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError


class RegistryRepo:

    session = None

    def __init__(self):
        self.session = storage.get_session()

    def findByStudent(self, student):
        if student:
            try:
                registry = self.session.query(Registry).filter_by(registry_student=student).first()
                return registry
            except SQLAlchemyError:
                return
            
    def findBySchool(self, school):
        if school:
            try:
                registry = self.session.query(Registry).filter_by(registry_school=school).first()
                return registry
            except SQLAlchemyError:
                return
            
    def findByStudentAndSchool(self, student: Student, school: School) -> Registry:
        try:
            registry = self.session.query(Registry).filter(and_(Registry.registry_student == student, 
                                                                Registry.registry_school == school)).first()
            return registry
        except SQLAlchemyError:
            return
        
    def findByStudentAndSchoolAndStatus(self, student: Student, school: School, status: Status) -> Registry:
        try:
            registry = self.session.query(Registry).filter(and_(Registry.registry_student == student, 
                                                                Registry.registry_school == school,
                                                                Registry.status == status)).first()
            return registry
        except SQLAlchemyError:
            return 

    def findByStudentAndStatus(self, student: Student, status: Status) -> Registry:
        if student:
            try:
                registry = self.session.query(Registry).filter(and_(Registry.registry_student == student, 
                                                                    Registry.status == status)).first()
                return registry
            except SQLAlchemyError:
                return
            
    def findBySchoolAndStatus(self, school: School, status: Status) -> Registry:
        if school:
            try:
                registry = self.session.query(Registry).filter(and_(Registry.registry_school == school, 
                                                                    Registry.status == status)).first()
                return registry
            except SQLAlchemyError:
                return
            
    def findAll(self):
        try:
            registries = self.session.query(Registry).all()
            return registries
        except SQLAlchemyError:
            return    