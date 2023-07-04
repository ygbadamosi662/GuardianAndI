"Defines GuardianRepo class"
from models import storage
from models.guardian import Guardian
from sqlalchemy.exc import SQLAlchemyError


class GuardianRepo:

    session = None

    def __init__(self):
        self.session = storage.get_session()

    def findByEmail(self, email):
        if email:
            try:
                guardian = self.session.query(Guardian).filter_by(email=email).first()
                return guardian
            except SQLAlchemyError:
                return

    def findAllGuardian(self):
        try:
            guardian = self.session.query(Guardian).all()
            return guardian
        except SQLAlchemyError:
            return