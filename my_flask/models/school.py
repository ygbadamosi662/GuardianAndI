#!/usr/bin/python3
"""Defines the School class."""
from models.base_model import BaseModel
# from typing import List
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
from global_variables import globalBcrypt
from models.userBase import User



class School(BaseModel, User):
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
    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True, name="school_id")
    school_name: Mapped[str] = mapped_column(String(128))
    grade: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(128))
    address: Mapped[str] = mapped_column(String(128))
    city: Mapped[str] = mapped_column(String(128))

    school_students = relationship("Student", back_populates="student_school")
    school_registries = relationship("Registry", back_populates="registry_school")

    __mapper_args__ = {
        "polymorphic_identity": "school",
    }
    # id = Column(Integer, primary_key=True, name='school_id')
    # user_id = Column(Integer, ForeignKey('users.id'))
    # school_name = Column(String(128))
    # email = Column(String(128), nullable=False, unique=True)
    # password = Column(String(128), nullable=False)
    # address = Column(String(128))
    # city = Column(String(128))

    students_list = relationship("Student", back_populates="school_relation")
    school_registries = relationship(
        "Registry", 
        back_populates="registry_school", 
        foreign_keys=[Column(Integer, ForeignKey("schools.school_id"))],
        )
    # pick_and_drops_school = relationship("PickAndDrop", back_populates="pick_and_drop_school")
    
    __mapper_args__ = {
        "polymorphic_identity": "school",
    }


    def __init__(self, *args, **kwargs):
        """Initialize school"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = globalBcrypt.hashpw(value.encode('utf-8'), globalBcrypt.gensalt())
            # value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)
