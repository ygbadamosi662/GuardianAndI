"Defines StudentRepo class"
from models import storage
from typing import List, Union
from models.student import Student
from models.school import School
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_


class StudentRepo:
    """
    Defines a repository for Student model
    provides methods for querying its table in the db
    """

    session = None

    def __init__(self):
        self.session = storage.get_session()

    def findByEmail(self, email: str)-> Student:
        
        if email:
            
            try:
                student = self.session.query(Student).filter_by(email=email).first()
                
                return student
            except SQLAlchemyError as err:
                
                print(err)
                return
            
    def pageBySchoolAndGrade(self, school: School, grade: str, page: int) -> List[Student]:
        if school:
            try:
                page_size = 10
                offset = (page - 1) * page_size
                query = self.session.query(Student).filter(and_(Student.student_school == school, 
                                                                Student.grade == grade)).limit(page_size).offset(offset)
                return query.all()
            except SQLAlchemyError as err:
                return 

    def findAll(self):
        try:
            students = self.session.query(Student).all()
            return students
        except SQLAlchemyError:
            return
        
student_repo = StudentRepo()        