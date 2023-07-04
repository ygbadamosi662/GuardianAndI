#!/usr/bin/python3
"""Defines the Guard class."""
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Enum, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from Enums import guardian_enum, status_enum



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
    id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), primary_key=True, name="guard_id")
    tag: Mapped[guardian_enum.Guardian]
    status: Mapped[status_enum.Status]
    guard_student_id: Mapped[int] = mapped_column(ForeignKey("students.student_id"))
    guard_student = relationship("Student", back_populates="student_guards")

    guard_guardian_id: Mapped[int] = mapped_column(ForeignKey("guardians.guardian_id"))
    guard_guardian = relationship("Guardian", back_populates="guardian_guards")

    guard_PADs = relationship("PickAndDrop", back_populates="PAD_guard")

    __mapper_args__ = {
        "polymorphic_identity": "guard",
    }
    # id
    # id = Column(Integer, primary_key=True)
    # student_id = Column(Integer, ForeignKey('students.student_id'))
    # guardian_id = Column(Integer, ForeignKey('guardians.guardian_id'))
    # tag = Column(Enum(guardian_enum.Guardian))
    
    
    # guards_student = relationship("Student", back_populates="guard_student")
    # guards_guardian = relationship("Guardian", back_populates="guardian_guard")
    # pick_and_drops_guard = relationship("PickAndDrop", back_populates='pick_and_drop_guard')

    def __init__(self, *args, **kwargs):
        """initialize the guards"""
        super().__init__(*args, **kwargs)