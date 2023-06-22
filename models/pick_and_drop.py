#!/usr/bin/python3
"""Defines the PickAndDrop class."""
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Enum, Integer, ForeignKey
from sqlalchemy.orm import relationship


class PickAndDrop(Base, BaseModel):
    """Represents a pick and drops for a MySQL database.
    Inherits from SQLAlchemy Base and links to the MySQL table pick_and_drops.
    Attributes:
        __tablename__ (str): The name of the MySQL table to store pick_and_drop.
        id: (sqlalchemy Integer, Primary_key): pick_and_drop's id
        first_name: (sqlalchemy String): The pick_and_drop's first name.
        last_name: (sqlalchemy String): The pick_and_drop's last name.
        email: (sqlalchemy String): The pick_and_drop's email.
        age: (sqlalchemy Integer): The pick_and_drop's age.
        tag: (sqlalchemy Enum): The pick_and_drop's tag
        gender: (sqlalchemy Enum): The pick_and_drop's gender
        student_id: (sqlalchemy Integer): pick_and_drop's student
        school_id: (sqlalchemy Integer): pick_and_drop's school
        guardian_id: (sqlalchemy Integer): pick_and_drop's guardian
        student: (sqlalchemy relationship): The PickAndDrop-Student relationship.
        school: (sqlalchemy relationship): The PickAndDrop-School relationship.
        guardian: (sqlalchemy relationship): The PickAndDrop-Guardian relationship.
        
    """
    __tablename__ = "pick_and_drops"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student_id'))
    school_id = Column(Integer, ForeignKey('school_id'))
    guardian_id = Column(Integer, ForeignKey('guardian_id'))
    action = Column(Enum('PICK-UP', 'DROP-OFF'))
    

    student = relationship("Student", back_populates="pick_and_drop")
    school = relationship("School", back_populates="pick_and_drop")
    guardian = relationship("Guardian", back_populates="pick_and_drop")

    def __init__(self):
        """initialize the pick_and_drop"""
        super.__init__()
