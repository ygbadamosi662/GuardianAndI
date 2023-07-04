"Defines SchoolRepo class"
from models import storage
from models.guard import Guard
from models.guardian import Guardian
from models.student import Student
from models.school import School
from sqlalchemy.exc import SQLAlchemyError


class SchoolRepo:

    session = None

    def __init__(self):
        self.session = storage.get_session()