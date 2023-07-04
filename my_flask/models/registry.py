#!/usr/bin/python3
"""Defines the Registry class."""
from models.base_model import BaseModel
from models.subjectBase import Subject
from sqlalchemy import Column, Enum, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from Enums import status_enum


class Registry(BaseModel, Subject):
    """Represents a registry for a MySQL database.
    Inherits from SQLAlchemy Base and links to the MySQL table
    registries.
    Attributes:
        __tablename__ (str): The name of the MySQL table to store
        guards.
        student_id: (sqlalchemy Integer): registries student
        school_id: (sqlalchemy Integer): registries school
    """
    __tablename__ = "registries"
    id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), primary_key=True, name="registry_id")
    status: Mapped[status_enum.Status]
    registry_student_id: Mapped[int] = mapped_column(ForeignKey("students.student_id"))
    registry_student = relationship("Student", back_populates="student_registries", foreign_keys="Registry.registry_student_id")

    registry_school_id: Mapped[int] = mapped_column(ForeignKey("schools.school_id"))
    registry_school = relationship("School", back_populates="school_registries")

    registry_PADs = relationship("PickAndDrop", back_populates="PAD_registry")

    __mapper_args__ = {
        "polymorphic_identity": "registry",
    }
    # id = Column(Integer, primary_key=True, name='registry_id')
    # subject_id = Column(Integer, ForeignKey('subjects.id'))
    # student_id = Column(Integer, ForeignKey('students.student_id'))
    # school_id = Column(Integer, ForeignKey('schools.school_id'))
    # status = Column(Enum(status_enum.Status))
    
    
    # registry_student = relationship("Student", back_populates="student_registries")
    # registry_school = relationship("School", back_populates="school_registries")
    # registry_pick_and_drops = relationship("PickAndDrop", back_populates="pick_and_drop_registry")
    # pick_and_drops_guard = relationship("PickAndDrop", back_populates='pick_and_drop_guard')

    # polymorphic_identity = 'registry'

    def __init__(self, *args, **kwargs):
        """initialize the guards"""
        super().__init__(*args, **kwargs)