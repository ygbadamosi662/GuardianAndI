#!/usr/bin/python3
"""Defines the Registry class."""
from models.base_model import BaseModel, Base
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
    # id: Mapped[int] = mapped_column(primary_key=True, name="registry_id")
    status: Mapped[status_enum.Status]

    student_id: Mapped[int] = mapped_column(ForeignKey("students.student_id"))
    registry_student = relationship("Student", foreign_keys=student_id)

    registry_school_id: Mapped[int] = mapped_column(ForeignKey("schools.school_id"))
    registry_school = relationship("School", foreign_keys=registry_school_id)

    registry_PADs = relationship("PickAndDrop", backref="PAD_registry", foreign_keys=id)

    __mapper_args__ = {
        "polymorphic_identity": "registry",
    }

    def __init__(self, *args, **kwargs):
        """initialize the guards"""
        super().__init__(*args, **kwargs)