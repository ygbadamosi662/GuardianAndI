#!/usr/bin/python3
"""Defines the Jwt_Blacklist class."""
from models.base_model import Base, BaseModel
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column


class Jwt_Blacklist(BaseModel, Base):
    """Represents a jwt blacklist table for a MySQL database.
    Inherits from SQLAlchemy Base and links to the MySQL table
    blacklists.
    Attributes:
        __tablename__ (str): The name of the MySQL table to store
        jwt_blacklist.
        id: (sqlalchemy Integer): jwt_blacklists id
        jwt: (sqlalchemy String): jwt_blacklist's jwt token
        user_id: (sqlalchemy Integer): jwt_blacklist's user_id
    """
    __tablename__ = "jwt_blacklists"
    id: Mapped[int] = mapped_column(primary_key=True)
    jwt: Mapped[str] = mapped_column(String(1024))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user = relationship("User", foreign_keys=user_id)

    __mapper_args__ = {
        "polymorphic_identity": "jwt_blacklist",
    }
    

    def __init__(self, *args, **kwargs):
        """initialize the jwt_blacklist"""
        super().__init__(*args, **kwargs)