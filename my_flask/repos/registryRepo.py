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