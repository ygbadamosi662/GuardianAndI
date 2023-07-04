"Defines PickAndDropRepo class"
from models import storage
from models.guard import Guard
from models.guardian import Guardian
from models.student import Student
from models.pick_and_drop import PickAndDrop
from sqlalchemy.exc import SQLAlchemyError


class PickAndDropRepo:

    session = None

    def __init__(self):
        self.session = storage.get_session()