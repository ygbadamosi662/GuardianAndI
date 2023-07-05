#!/usr/bin/python3
"""Defines the Guard class."""
from models.base_model import BaseModel, Base
from models.subjectBase import Subject
from sqlalchemy import Column, Enum, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from Enums import tag_enum, status_enum



class Guard(BaseModel, Subject):
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
    id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), primary_key=True, name="guard_id")
    # id: Mapped[int] = mapped_column(primary_key=True, name="guard_id")
    tag: Mapped[tag_enum.Tag]
    status: Mapped[status_enum.Status]

    guard_student_id: Mapped[int] = mapped_column(ForeignKey("students.student_id"))
    guard_student = relationship("Student", foreign_keys=guard_student_id)

    guard_guardian_id: Mapped[int] = mapped_column(ForeignKey("guardians.guardian_id"))
    guard_guardian = relationship("Guardian", foreign_keys=guard_guardian_id)

    guard_PADs = relationship("PickAndDrop", backref="PAD_guard", foreign_keys=id)

    __mapper_args__ = {
        "polymorphic_identity": "guard",
    }

    def __init__(self, *args, **kwargs):
        """initialize the guards"""
        super().__init__(*args, **kwargs)