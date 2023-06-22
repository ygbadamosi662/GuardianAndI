#!/usr/bin/python3
"""Defines the Student class."""
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Enum, Date
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Student(Base, BaseModel):
    """Represents a student for a MySQL database.
    Inherits from SQLAlchemy Base and links to the MySQL table students.
    Attributes:
        __tablename__ (str): The name of the MySQL table to store students.
        id: (sqlalchemy Integer, Primary_key): student's id
        first_name: (sqlalchemy String): The student's first name.
        last_name: (sqlalchemy String): The student's last name.
        grade: (sqlalchemy String): The student's grade.
        age: (sqlalchemy Integer): The student's age.
        gender: (sqlalchemy Enum): The student's gender.
        school_id: (sqlalchemy Integer): student's schools
        school: (sqlalchemy relationship): The Student-School relationship.
        
    """
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128))
    grade = Column(String(128), nullable=False)
    dob = Column(Date)
    gender = Column(Enum('MALE', 'FEMALE'))
    school_id = Column(Integer, ForeignKey('school_id'))

    pick_and_drop = relationship("PickAndDrop", uselist=False, back_populates="student")
    school = relationship("School", back_populates="students", cascade="delete")
    guardians = relationship("Guardian", back_populates="student", cascade="delete")

    def __init__(self):
        """ Initializes pupil """
        super().__init__()
