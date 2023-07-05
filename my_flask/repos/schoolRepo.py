"Defines SchoolRepo class"
from models import storage
from models.guard import Guard
from models.guardian import Guardian
from models.student import Student
from models.school import School
from sqlalchemy.exc import SQLAlchemyError


class SchoolRepo:
    """
    Defines a repository for School model
    provides methods for querying its table in the db
    """
    session = None

    def __init__(self):
        self.session = storage.get_session()

    def findByEmail(self, email):
        if email:
            try:
                school = self.session.query(School).filter_by(email=email).first()
                return school
            except SQLAlchemyError:
                return

    def findAll(self):
        try:
            schools = self.session.query(School).all()
            return schools
        except SQLAlchemyError:
            return