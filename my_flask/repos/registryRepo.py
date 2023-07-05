"Defines RegistryRepo class"
from models import storage
from models.registry import Registry
from models.student import Student
from models.school import School
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

    def findAll(self):
        try:
            registries = self.session.query(Registry).all()
            return registries
        except SQLAlchemyError:
            return    