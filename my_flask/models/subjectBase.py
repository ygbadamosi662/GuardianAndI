#!/usr/bin/python3
"""Defines the Subject class."""
from models.base_model import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column



class Subject(Base):
    """Represents a Subject class, a super class extends Base from sqlalchemy
    Attributes:
        __tablename__ (str): The name of the MySQL table to store
        subjects.
    """
    __tablename__ = "subjects"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))

    note_subjects = relationship("Notification", back_populates="note_subject")
    # type: Mapped[str]

    __mapper_args__ = {
        "polymorphic_identity": "subject",
        "polymorphic_on": "name",
    }
    # id = Column(Integer, primary_key=True)
    # name = Column(String(255))

    # subjects = relationship("Notification", back_populates="subject", foreign_keys="[Notification.subject_id]")

    # polymorphic_identity = 'subject'

    def __init__(self, name):
        self.name = name