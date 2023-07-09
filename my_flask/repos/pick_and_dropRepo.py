"Defines PickAndDropRepo class"
from models import storage
from typing import List, Union
from models.guard import Guard
from models.guardian import Guardian
from models.student import Student
from models.pick_and_drop import PickAndDrop
from models.registry import Registry
from Enums.auth_enum import Auth
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError


class PickAndDropRepo:

    session = None

    def __init__(self):
        self.session = storage.get_session()

    # def findOngoingPadByRegistry(self, reg: Registry) -> PickAndDrop:
    #     if reg:
    #         query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_registry == reg, PickAndDrop.auth != Auth.ARRIVED, PickAndDrop.auth != Auth.FALSE, PickAndDrop.auth != Auth.SCHOOL_OUT, PickAndDrop.auth != Auth.SG_OUT)

    #         return query.all()
        
    def findOngoingPadByRegistry(self, reg: Registry) -> PickAndDrop:
        if reg:
            query = self.session.query(PickAndDrop).filter(PickAndDrop.PAD_registry == reg, ~PickAndDrop.auth.in_([Auth.ARRIVED, Auth.FALSE, Auth.SCHOOL_OUT, Auth.SG_OUT]))

            return query.first()
        
    def findOngoingPadByGuard(self, guard: Guard) -> PickAndDrop:
        if guard:
            query = self.session.query(PickAndDrop).filter(and_(PickAndDrop.PAD_guard == guard, PickAndDrop.auth != Auth.ARRIVED, PickAndDrop.auth != Auth.FALSE, PickAndDrop.auth != Auth.SCHOOL_OUT, PickAndDrop.auth != Auth.SG_OUT))

            return query.first()
        
    def findOngoingPadByGuardian(self, guardian: Guardian) -> List[PickAndDrop]:
        if guardian:
            query = self.session.query(PickAndDrop).filter(and_(PickAndDrop.PAD_guard.guard_guardian == guardian, PickAndDrop.auth != Auth.ARRIVED, PickAndDrop.auth != Auth.FALSE, PickAndDrop.auth != Auth.SCHOOL_OUT, PickAndDrop.auth != Auth.SG_OUT))

            return query.all()


pad_repo = PickAndDropRepo()