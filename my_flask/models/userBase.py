#!/usr/bin/python3
"""Defines the User class."""
from models.base_model import Base
from models.notification import Notification
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column



class User(Base):
    """Represents a User class, a super class extends Base from sqlalchemy
    Attributes:
        __tablename__ (str): The name of the MySQL table to store
        users.
    """
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))

    sender_notes = relationship("Notification", backref="note_sender", primaryjoin=id==Notification.sender_id)
    receiver_notes = relationship("Notification", backref="note_receiver", primaryjoin=id==Notification.receiver_id)
    # type: Mapped[str]

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": "name",
    }

    def __init__(self, name):
        self.name = name