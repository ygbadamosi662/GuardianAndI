"""Defines a Note_Service class"""
from services.service import Service
from typing import List
from models.notification import Notification
from models.guardian import Guardian
from models.userBase import User
from models.subjectBase import Subject
from models.pick_and_drop import PickAndDrop
from Enums.permit_enum import Permit
from Enums.activity_enum import Activity
from Enums.auth_enum import Auth
from Enums.tag_enum import Tag
from utility import util
from global_variables import AUTHORIZATION, CONFIRMATION
from repos.notificationRepo import note_repo


class Note_Service(Service):
    """
    Represents a service class for notifications
    """

    # who_called = ''
    note_repo = None
    
    def __init__(self):
        self.note_repo = note_repo

    def create_noti(self, sender: User, receiver: User, subject: Subject, permit: Permit, note: str = ''):
        if sender and receiver and subject and permit:
            noti = Notification(note_sender=sender, note_receiver=receiver, subject=subject, permit=permit, activity=Activity.SENT, note=note)

            util.persistModel(noti)

    def superG_pad_sanity_test(self, notis: List[Notification]) -> List[Notification]:
        if notis:
            for noti in notis:
                if noti:
                    if noti.subject.__tablename__ == 'pick_and_drops':
                        pad = noti.subject
                        if noti.note == AUTHORIZATION:
                            if (pad.auth == Auth.SG_IN) or (pad.auth == Auth.SG_OUT):
                                noti.permit = Permit.READONLY
                                util.persistModel(noti)
                                notis.remove(noti)

                        if noti.note == CONFIRMATION:
                            if pad.auth == Auth.ARRIVED:
                                noti.permit = Permit.READONLY
                                util.persistModel(noti)
                                notis.remove(noti)

            return notis

    def maintain_user_notification_sanity(self, notis: List[Notification], receiver: User) -> List[Notification]:
        # this checks what notification is about and corrects un-necessary permits +
        # like in the case of sending out multiple authorization notifications to super guardians +
        # and we only need one authorization from just one of them, when thats fulfilled, this method +
        # performs corrcts the permits on other super_guardian notification to read_only, to avoid un-necessary +
        # requests to our app
        if notis:
            # super_guardians sanity test
            if receiver.__tablename__ == 'guardians':
                notis = self.superG_pad_sanity_test(notis)

            return notis
    
    def get_needy_notis(self, receiver: User, page: int) -> List[Notification]:
        # get user's needy notifications
        if receiver:
            
            notis_read_and_write = note_repo.pageByReceiverAndPermitAndNotActivity(receiver, Activity.DONE,
                                                                     Permit.READ_AND_WRITE, page)
            # maintain read_and_write sanity
            notis_read_and_write = self.maintain_user_notification_sanity(notis_read_and_write, receiver)

            notis_read_only = note_repo.pageByReceiverAndPermitAndNotActivity(receiver, Activity.SEEN, 
                                                                              Permit.READONLY, page)

            return notis_read_and_write + notis_read_only
        
    
note_service = Note_Service()






        
