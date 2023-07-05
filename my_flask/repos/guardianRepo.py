"Defines GuardianRepo class"
from models import storage
from models.guardian import Guardian
from sqlalchemy.exc import SQLAlchemyError


class GuardianRepo:
    """
    Defines a repository for Guardian model
    provides methods for querying its table in the db
    """

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

    def findAll(self):
        try:
            guardians = self.session.query(Guardian).all()
            return guardians
        except SQLAlchemyError:
            return