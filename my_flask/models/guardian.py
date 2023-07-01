#!/usr/bin/python3
"""Defines the Guardian class."""
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Enum, Date
from sqlalchemy import String
from sqlalchemy import Integer
from global_variables import globalBcrypt
from sqlalchemy.orm import relationship


class Guardian(BaseModel, Base):
    """Represents a guardian for a MySQL database.
    Inherits from SQLAlchemy Base and links to the MySQL table guardians.
    Attributes:
        __tablename__ (str): The name of the MySQL table to store guardians.
        id: (sqlalchemy Integer, Primary_key): guardian's id
        first_name: (sqlalchemy String): The guardian's first name.
        last_name: (sqlalchemy String): The guardian's last name.
        email: (sqlalchemy String): The guardian's email.
        age: (sqlalchemy Integer): The guardian's age.
        tag: (sqlalchemy Enum): The guardian's tag
        gender: (sqlalchemy Enum): The guardian's gender
        student_id: (sqlalchemy Integer): guardian's student
        student: (sqlalchemy relationship): The Guardian-Student relationship.

    """
    __tablename__ = "guardians"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    gender = Column(Enum('MALE', 'FEMALE'))
    dob = Column(Date)

    pick_and_drops_guardian = relationship("PickAndDrop", back_populates="pick_and_drop_guardian")
    guardian_guard = relationship("Guard", back_populates="guards_guardian")

    def __init__(self, *args, **kwargs):
        """Initialize guardian"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with bcrypt encryption"""
        if name == "password":
            value = globalBcrypt.hashpw(value.encode('utf-8'), globalBcrypt.gensalt())
        super().__setattr__(name, value)       
