#!/usr/bin/python3
"""Defines the PickAndDrop class."""
from models.base_model import BaseModel, Base
from models.subjectBase import Subject
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Enums import action_enum, auth_enum


class PickAndDrop(BaseModel, Subject):
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
    id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), primary_key=True, name="pick_and_drop_id")
    action: Mapped[action_enum.Action]
    auth: Mapped[auth_enum.Auth]
    
    PAD_guard_id: Mapped[int] = mapped_column(ForeignKey("guards.guard_id"))
    PAD_registry_id: Mapped[int] = mapped_column(ForeignKey("registries.registry_id"))

    auth_provider_id: Mapped[int] = mapped_column(ForeignKey("guardians.guardian_id"))
    auth_provider = relationship("Guardian", back_populates="auths_provided")

    __mapper_args__ = {
        "polymorphic_identity": "pick_and_drop",
    }

    def __init__(self, *args, **kwargs):
        """initialize the pick_and_drop"""
        super().__init__(*args, **kwargs)
