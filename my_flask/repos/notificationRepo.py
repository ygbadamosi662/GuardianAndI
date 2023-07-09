"Defines NotificationRepo class"
from models import storage
from models.guard import Guard
from models.guardian import Guardian
from models.student import Student
from models.notification import Notification
from sqlalchemy.exc import SQLAlchemyError


class NotificationRepo:

    session = None

    def __init__(self):
        self.session = storage.get_session()



note_repo = NotificationRepo()         