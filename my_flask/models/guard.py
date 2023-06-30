#!/usr/bin/python3
"""Defines the Guard class."""
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Enum, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Guard(BaseModel, Base):
    """Represents a guards for a MySQL database.
    Inherits from SQLAlchemy Base and links to the MySQL table
    guards.
    Attributes:
        __tablename__ (str): The name of the MySQL table to store
        guards.
        student_id: (sqlalchemy Integer): guard's student
        school_id: (sqlalchemy Integer): guard's school
        guardian_id: (sqlalchemy Integer): guard's guardian
    """
    __tablename__ = "guards"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    guardian_id = Column(Integer, ForeignKey('guardians.id'))
    tag = Column(Enum('SUPER_GUARDIAN', 'AUXILLARY_GUARDIAN'))
    
    
    guards_student = relationship("Student", back_populates="guard_student")
    guards_guardian = relationship("Guardian", back_populates="guardian_guard")

    def __init__(self, *args, **kwargs):
        """initialize the guards"""
        super().__init__(*args, **kwargs)