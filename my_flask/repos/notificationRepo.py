"Defines NotificationRepo class"
from models import storage
from typing import List
from sqlalchemy import func, or_
from Enums.permit_enum import Permit
from Enums.activity_enum import Activity
from models.subjectBase import Subject
from models.userBase import User
from models.guardian import Guardian
from models.student import Student
from models.notification import Notification
from sqlalchemy.exc import SQLAlchemyError


class NotificationRepo:

    session = None
    page_size = None

    def __init__(self):
        self.session = storage.get_session()
        self.page_size = 10

    def findById(self, id: int) -> Notification:
        return self.session.query(Notification).filter(Notification.id == id).first()

    def pageByNote_receiver(self, receiver: User, page: int) -> List[Notification]:
        if receiver and page:
            offset = (page - 1) * self.page_size
            query = self.session.query(Notification).filter(Notification.note_receiver == receiver).limit(self.page_size).offset(offset)

            return query.all()
        
    def pageByNote_sender(self, sender: User, page: int) -> List[Notification]:
        if sender and page:
            offset = (page - 1) * self.page_size
            query = self.session.query(Notification).filter(Notification.note_sender == sender).limit(self.page_size).offset(offset)

            return query.all()
        
    def pageBySubject(self, subject: User, page: int) -> List[Notification]:
        if subject and page:
            offset = (page - 1) * self.page_size
            query = self.session.query(Notification).filter(Notification.subject == subject).limit(self.page_size).offset(offset)

            return query.all()
        
    def pageByReceiverAndActivity(self, receiver: User, activity: Activity, page: int) -> List[Notification]:
        if receiver and activity and page:
            offset = (page - 1) * self.page_size
            query = self.session.query(Notification).filter(Notification.note_receiver == receiver, 
                                                            Notification.activity == activity).limit(self.page_size).offset(offset)

            return query.all()
        
    def pageByReceiverAndPermit(self, receiver: User, permit: Permit, page: int) -> List[Notification]:
        if receiver and permit and page:
            offset = (page - 1) * self.page_size
            query = self.session.query(Notification).filter(Notification.note_receiver == receiver, 
                                                            Notification.   permit == permit).limit(self.page_size).offset(offset)

            return query.all()
        
    def pageByReceiverAndActivityAndPermit(self, receiver: User, activity: Activity, permit: Permit, page: int) -> List[Notification]:
        if receiver and permit and page:
            offset = (page - 1) * self.page_size
            query = self.session.query(Notification).filter(Notification.note_receiver == receiver, 
                                                            Notification.activity == activity, Notification.permit == permit).limit(self.page_size).offset(offset)

            return query.all()
        
    def pageByReceiverAndPermitAndNotActivity(self, receiver: User, activity: Activity, permit: Permit, page: int) -> List[Notification]:
        if receiver and permit and page:
            offset = (page - 1) * self.page_size
            query = self.session.query(Notification).filter(Notification.note_receiver == receiver, 
                                                             Notification.permit == permit, Notification.activity != activity).limit(self.page_size).offset(offset)

            return query.all()
        
    def countByReceiverAndActivityAndPermit(self, receiver: User, activity: Activity) -> int:
        if receiver and activity:
            return self.session.query(func.count(Notification)).filter(Notification.activity == activity).scalar()
        
    def countByReceiverAndPermitAndNotActivity(self, receiver: User, permit: Permit, activity: Activity) -> int:
        if receiver and activity:
            return self.session.query(func.count(Notification)).filter(Notification.permit == permit, 
                                                                       Notification.activity != activity).scalar()




note_repo = NotificationRepo()         