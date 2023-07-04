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

    def findByGuards_guardian(self, guardian: Guardian ):
        if guardian:
            try:
                guard = self.session.query(Guard).filter_by(guards_guardian=guardian).first()
                return guard
            except SQLAlchemyError:
                return

    def findByGuards_student(self, student: Student):
        try:
            guard = self.session.query(Guard).filter_by(guards_student=student).first()
            return guard
        except SQLAlchemyError:
            return