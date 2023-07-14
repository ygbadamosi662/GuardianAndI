"Defines GuardRepo class"
from models import storage
from typing import List, Union
from models.guard import Guard
from models.guardian import Guardian
from models.student import Student
from Enums.status_enum import Status
from Enums.tag_enum import Tag
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError


class GuardRepo:

    session = None

    def __init__(self):
        self.session = storage.get_session()

    def findByGuardian(self, guardian: Guardian ) -> List[Guard]:
        if guardian:
            try:
                guards = self.session.query(Guard).filter_by(guard_guardian=guardian).all()
                return guards
            except SQLAlchemyError:
                return
            
    def findByGuardianAndStatus(self, guardian: Guardian, status: Status) -> List[Guard]:
        if guardian:
            try:
                guards = self.session.query(Guard).filter(and_(Guard.guard_guardian == guardian, 
                                                               Guard.status == status)).all()
                return guards
            except SQLAlchemyError:
                return

    def pageByGuardianAndStatus(self, guardian: Guardian, status: Status, page: int) -> List[Guard]:
        if guardian:
            try:
                page_size = 10
                offSet = (page - 1) * page_size

                query = self.session.query(Guard).filter(and_(Guard.guard_guardian == guardian, 
                                                               Guard.status == status)).limit(page_size).offset(offSet)
                return query.all()
            except SQLAlchemyError:
                return
            
    def findByGuardianAndStatusAndTag(self, guardian: Guardian, status: Status, tag: Tag) -> List[Guard]:
        if guardian:
            try:
                guards = self.session.query(Guard).filter(and_(Guard.guard_guardian == guardian, 
                                                               Guard.status == status, Guard.tag == tag)).all()
                return guards
            except SQLAlchemyError:
                return

    def findByStudent(self, student: Student) -> List[Guard]:
        try:
            guards = self.session.query(Guard).filter_by(guard_student=student).all()
            return guards
        except SQLAlchemyError:
            return
        
    def findByStudentAndStatus(self, student: Student, status: Status) -> List[Guard]:
        if student:
            try:
                guards = self.session.query(Guard).filter(and_(Guard.guard_student == student, 
                                                               Guard.status == status)).all()
                return guards
            except SQLAlchemyError:
                return
            
    def pageByStudentAndStatus(self, student: Student, status: Status, page: int) -> List[Guard]:
        if student:
            try:
                page_size = 10
                offSet = (page - 1) * page_size

                query = self.session.query(Guard).filter(and_(Guard.guard_student == student, 
                                                               Guard.status == status)).limit(page_size).offset(offSet)
                return query.all()
            except SQLAlchemyError:
                return
            
    def findByStudentAndStatusAndTag(self, student: Student, status: Status, tag: Tag) -> List[Guard]:
        if student:
            try:
                guards = self.session.query(Guard).filter(and_(Guard.guard_student == student, 
                                                               Guard.status == status, Guard.tag == tag)).all()
                return guards
            except SQLAlchemyError:
                return
            
    def findByStudentAndGuardian(self, student: Student, guardian: Guardian) -> Guard:
        if student and guardian:
            try:
                guards = self.session.query(Guard).filter(and_(Guard.guard_student == student, 
                                                               Guard.guard_guardian == guardian)).first()
                return guards
            except SQLAlchemyError:
                return

    def findByStudentAndGuardianAndStatus(self, student: Student, guardian: Guardian, status: Status) -> Guard:
        if student and guardian:
            try:
                guards = self.session.query(Guard).filter(and_(Guard.guard_student == student, 
                                                               Guard.guard_guardian == guardian, 
                                                               Guard.status == status)).first()
                return guards
            except SQLAlchemyError:
                return

    def findByStudentAndGuardianAndStatusAndTag(self, student: Student, guardian: Guardian, status: Status, tag: Tag) -> Guard:
        if student and guardian:
            try:
                guards = self.session.query(Guard).filter(and_(Guard.guard_student == student, 
                                                               Guard.guard_guardian == guardian, 
                                                               Guard.status == status, 
                                                               Guard.tag == tag)).first()
                return guards
            except SQLAlchemyError:
                return
            
    def pageByGuardianAndStatusAndTag(self, guardian: Guardian, status: Status, tag: Tag, page: int) -> Guard:

        if guardian:
            page_size = 10
            offSet = (page - 1) * page_size

            try:
                query = self.session.query(Guard).filter(and_(Guard.guard_guardian == guardian, 
                                                               Guard.status == status, 
                                                               Guard.tag == tag)).limit(page_size).offset(offSet)
                return query.all()
            except SQLAlchemyError:
                return
            
    def findById(self, id: int) -> Guard:
        return self.session.query(Guard).filter(Guard.id == id).first()

guard_repo = GuardRepo()          