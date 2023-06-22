#!/usr/bin/python3
"""Defines the DBStorage engine."""
from os import getenv
from dotenv import load_dotenv
from models.base_model import Base
from models.student import Student
from models.school import School
from models.guardian import Guardian
from models.pick_and_drop import PickAndDrop
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

load_dotenv('name-of-env-file')

user = getenv("GI_DEV")
password = getenv("GI_DEV_PWD")
host = getenv("GI_DEV_HOST")
db = getenv("GI_DEV_DB")


class DBStorage:
    """Represents a database storage engine.
    Attributes:
        __engine (sqlalchemy.Engine): The working SQLAlchemy engine.
        __session (sqlalchemy.Session): The working SQLAlchemy session.
    """

    __engine = None
    __session = None

    def __init__(self):
        """Initialize a new DBStorage instance."""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(user, password, host, db),
                                      pool_pre_ping=True)
        if getenv("GI_DEV_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the curret database session all objects of the given class.
        If cls is None, queries all types of objects.
        Return:
            Dict of queried classes in the format <class name>.<obj id> = obj.
        """
        if cls is None:
            objs = self.__session.query(Student).all()
            objs.extend(self.__session.query(School).all())
            objs.extend(self.__session.query(Guardian).all())
            objs.extend(self.__session.query(PickAndDrop).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            objs = self.__session.query(cls)
        return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}

    def new(self, obj):
        """Add obj to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session."""
        if obj is not None:
            self.__session.delete(obj)
            self.__session.commit()

    def reload(self):
        """Create all tables in the database and initialize a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the working SQLAlchemy session."""
        self.__session.close()
