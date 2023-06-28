#!/usr/bin/python3
"""Defines the PickAndDrop class."""
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Enum, Integer, ForeignKey
from sqlalchemy.orm import relationship


class PickAndDrop(BaseModel, Base):
    """Represents a pick and drops for a MySQL database.
    Inherits from SQLAlchemy Base and links to the MySQL table
    pick_and_drops.
    Attributes:
        __tablename__ (str): The name of the MySQL table to store
        pick_and_drop.
        student_id: (sqlalchemy Integer): pick_and_drop's student
        school_id: (sqlalchemy Integer): pick_and_drop's school
        guardian_id: (sqlalchemy Integer): pick_and_drop's guardian
    """
    __tablename__ = "pick_and_drops"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    school_id = Column(Integer, ForeignKey('schools.id'))
    guardian_id = Column(Integer, ForeignKey('guardians.id'))
    action = Column(Enum('PICK-UP', 'DROP-OFF'))

    def __init__(self, *args, **kwargs):
        """initialize the pick_and_drop"""
        super().__init__(*args, **kwargs)
