#!/usr/bin/python3
"""Defines the Notification class."""
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from Enums import permit_enum, note_enum


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
    note: Mapped[note_enum.Note]
    permit: Mapped[permit_enum.Permit]
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    note_sender = relationship("User", back_populates="sender_notes", foreign_keys="Notification.sender_id")

    receiver_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    note_receiver = relationship("User", back_populates="receiver_notes", foreign_keys="Notification.receiver_id")

    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    note_subject = relationship("Subject", back_populates="note_subjects")

    __mapper_args__ = {
        "polymorphic_identity": "notification",
    }
    # id = Column(Integer, primary_key=True)
    # note = Column(Enum(note_enum.Note))
    # permit = Column(Enum(permit_enum.Permit))
    
    # sender_id = Column(Integer, ForeignKey('users.id'))
    # sender_type = Column(String(128), nullable=False)
    # sender = relationship(
    #     "User",
    #     primaryjoin="and_(Notification.sender_id == User.id)",
    #     back_populates="sender_notes",
    #     uselist=False,
    #     viewonly=True
    # )

    # receiver_id = Column(Integer, ForeignKey('users.id'))
    # receiver_type = Column(String(128), nullable=False)
    # receiver = relationship(
    #     "User",
    #     primaryjoin="and_(Notification.receiver_id == User.id)",
    #     back_populates="receiver_notes",
    #     uselist=False,
    #     viewonly=True
    # )
    

    
    # subject_id = Column(Integer, ForeignKey('subjects.id'))
    # subject_type = Column(String(128), nullable=False)
    # subject = relationship(
    #     "Subject",
    #     primaryjoin="and_(Notification.subject_id == Subject.id)",
    #     back_populates="subjects",
    #     uselist=False,
    #     viewonly=True
    # )

    def __init__(self, *args, **kwargs):
        """initialize the pick_and_drop"""
        super().__init__(*args, **kwargs)