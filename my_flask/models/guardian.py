#!/usr/bin/python3
"""Defines the Guardian class."""
from models.base_model import BaseModel
from models.userBase import User
from sqlalchemy import ForeignKey, Date
from sqlalchemy import String
from sqlalchemy import Integer
from global_variables import globalBcrypt
from sqlalchemy.orm import relationship, Mapped, mapped_column
from Enums import gender_enum


class Guardian(BaseModel, User):
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
    id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True, name="guardian_id")
    first_name: Mapped[str] = mapped_column(String(128))
    last_name: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    gender: Mapped[gender_enum.Gender]
    dob = mapped_column(Date)
    guardian_guards = relationship("Guard", back_populates="guard_guardian")
    
    __mapper_args__ = {
        "polymorphic_identity": "guardian",
    }

    # id = Column(Integer, primary_key=True, name='guardian_id')
    # user_id = Column(Integer, ForeignKey('users.id'))
    # first_name = Column(String(128), nullable=False)
    # last_name = Column(String(128), nullable=False)
    # email = Column(String(128), nullable=False, unique=True)
    # password = Column(String(128), nullable=False)
    # gender = Column(Enum(gender_enum.Gender))
    # dob = Column(Date)

    # pick_and_drops_guardian = relationship("PickAndDrop", back_populates="pick_and_drop_guardian")
    guardian_guard = relationship("Guard", back_populates="guards_guardian")

    polymorphic_identity = 'guardian'

    def __init__(self, *args, **kwargs):
        """Initialize guardian"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with bcrypt encryption"""
        if name == "password":
            value = globalBcrypt.hashpw(value.encode('utf-8'), globalBcrypt.gensalt())
        super().__setattr__(name, value)       
