#!/usr/bin/python3
"""Defines the School class."""
from models.base_model import Base, BaseModel
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import relationship
from hashlib import md5

class School(Base, BaseModel):
    """Represents a school for a MySQL database.
    Inherits from SQLAlchemy Base and links to the MySQL table schools.
    Attributes:
        __tablename__ (str): The name of the MySQL table to store schools.
        id: (sqlalchemy Integer, Primary_key): school's id
        name: (sqlalchemy String): The school's name.
        email: (sqlalchemy String): The school's email address.
        password (sqlalchemy String): The school's password.
        address: (sqlalchemy String): The school's address.
        city: (sqlalchemy String): The school's city.
        students (sqlalchemy relationship): The School-Student relationship.
        
    """
    __tablename__ = "schools"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    address = Column(String(128))
    city = Column(String(128))

    students = relationship("Student", back_populates="school", cascade="delete")
    pick_and_drop = relationship("PickAndDrop", uselist=False, back_populates="school")

    def __init__(self):
        """Initialize school"""
        super.__init__()

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)
