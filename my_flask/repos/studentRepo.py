"Defines StudentRepo class"
from models import storage
from models.guard import Guard
from models.guardian import Guardian
from models.student import Student
from models.school import School
from sqlalchemy.exc import SQLAlchemyError


class StudentRepo:
    """
    Defines a repository for Student model
    provides methods for querying its table in the db
    """

    session = None

    def __init__(self):
        self.session = storage.get_session()

    def findByEmail(self, email):
        if email:
            try:
                student = self.session.query(Student).filter_by(email=email).first()
                return student
            except SQLAlchemyError:
                return

    def findAll(self):
        try:
            students = self.session.query(Student).all()
            return students
        except SQLAlchemyError:
            return