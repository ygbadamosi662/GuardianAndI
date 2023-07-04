#!/usr/bin/python3
"""Defines the Student class."""
from models.base_model import BaseModel
from typing import List
from models.subjectBase import Subject
from sqlalchemy import Column, Enum, Date
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from Enums import gender_enum


class Student(BaseModel, Subject):
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
    id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), primary_key=True, name="student_id")
    first_name: Mapped[str] = mapped_column(String(128))
    last_name: Mapped[str] = mapped_column(String(128))
    grade: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(String(128) , nullable=False, unique=True)
    gender: Mapped[gender_enum.Gender]
    dob = mapped_column(Date)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.school_id"))
    student_school = relationship("School", back_populates="school_students")

    stuedent_guards = relationship("Guard", back_populates="guard_student")
    student_registries = relationship("Registry", back_populates="registry_student", foreign_keys="Student.id")

    __mapper_args__ = {
        "polymorphic_identity": "student",
    }
    # id = Column(Integer, primary_key=True, name='student_id')
    # subject_id = Column(Integer, ForeignKey('subjects.id'))
    # first_name = Column(String(128), nullable=False)
    # last_name = Column(String(128), nullable=False)
    # email = Column(String(128), nullable=False, unique=True)
    # grade = Column(String(128), nullable=False)
    # dob = Column(Date)
    # gender = Column(Enum(gender_enum.Gender))
    # school_id = Column(Integer, ForeignKey('schools.school_id'))

    # school_relation = relationship("School", back_populates="students_list")
    # student_registries = relationship(
    #     "Registry", 
    #     back_populates="registry_student", 
    #     foreign_keys=[Column(Integer, ForeignKey("students.student_id"))],
    #     )
    # guard_student = relationship("Guard", back_populates="guards_student")
    

    __mapper_args__ = {
        "polymorphic_identity": "student",
    }

    def __init__(self, *args, **kwargs):
        """ Initializes pupil """
        super().__init__(*args, **kwargs)
