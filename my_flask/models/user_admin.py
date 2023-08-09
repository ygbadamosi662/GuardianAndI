#!/usr/bin/python3
""" Define admin table """
from models.base_model import Base, BaseModel
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from typing import Dict, Any, List
from global_variables import globalBcrypt


class UserAdmin(BaseModel, Base):
    """
        Setup of admin user
        Args:
            BaseModel (_type_): BaseModel to inherit from.
            Base (_type_): Declarative base
    """
    __tablename__ = "useradmins"
    id: Mapped[int] = mapped_column(primary_key=True)
    username = mapped_column(String(128), unique=True, nullable=False)
    password = mapped_column(String(128), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "useradmin",
    }

    def __init__(self, *args: List[Any], **kwargs: Dict[str, Any]) -> None:
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value) -> None:
        """sets a password with bcrypt encryption"""
        if name == "password":
            value = globalBcrypt.hashpw(value.encode('utf-8'), globalBcrypt.gensalt())
        super().__setattr__(name, value)

    def __repr__(self) -> None:
        return self.username
