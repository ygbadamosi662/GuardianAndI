#!/usr/bin/python3
"""Defines the Notification class."""
from models.base_model import Base, BaseModel
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from Enums import permit_enum, activity_enum


class Notification(BaseModel, Base):
    """Represents a notification for a MySQL database.
    Inherits from SQLAlchemy Base and links to the MySQL table
    notifications.
    Attributes:
        __tablename__ (str): The name of the MySQL table to store
        notification.
        sender_id: (sqlalchemy Integer): notification's sender
        sender_type: (sqlalchemy Enum): notification's sender_type
        receiver_id: (sqlalchemy Integer): notification's receiver
        receiver_type: (sqlalchemy Enum): notification's receiver_type
    """
    __tablename__ = "notifications"
    id: Mapped[int] = mapped_column(primary_key=True, name="notification_id")
    activity: Mapped[activity_enum.Activity]
    permit: Mapped[permit_enum.Permit]
    note: Mapped[str] = mapped_column(String(255), nullable=True)
    
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    note_sender = relationship("User", foreign_keys=sender_id,  back_populates="sender_notes")

    receiver_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    note_receiver = relationship("User", foreign_keys=receiver_id, back_populates="receiver_notes")

    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    subject = relationship("Subject" , back_populates="subjects")

    __mapper_args__ = {
        "polymorphic_identity": "notification",
    }
    

    def __init__(self, *args, **kwargs):
        """initialize the pick_and_drop"""
        super().__init__(*args, **kwargs)