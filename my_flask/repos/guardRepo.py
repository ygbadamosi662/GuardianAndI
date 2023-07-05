"Defines GuardRepo class"
from models import storage
from models.guard import Guard
from models.guardian import Guardian
from models.student import Student
from sqlalchemy.exc import SQLAlchemyError


class GuardRepo:

    session = None

    def __init__(self):
        self.session = storage.get_session()

    def findByGuardian(self, guardian: Guardian ):
        if guardian:
            try:
                guard = self.session.query(Guard).filter_by(guards_guardian=guardian).all()
                return guard
            except SQLAlchemyError:
                return

    def findByStudent(self, student: Student):
        try:
            guard = self.session.query(Guard).filter_by(guard_student=student).all()
            return guard
        except SQLAlchemyError:
            return