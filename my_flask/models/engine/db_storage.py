#!/usr/bin/python3
"""Defines the DBStorage engine."""
from os import getenv
from dotenv import load_dotenv, find_dotenv
from models.base_model import Base
from models.student import Student
from models.school import School
from models.guardian import Guardian
from models.pick_and_drop import PickAndDrop
from models.guard import Guard
from models.notification import Notification
from models.registry import Registry
from models.jwt_blacklist import Jwt_Blacklist
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


path = find_dotenv('gi_dev_sql.env')
load_dotenv(path)

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
        self.__engine = create_engine("mysql+mysqlconnector://{}:{}@{}/{}".
                                      format(user, password, host, db),
                                      pool_pre_ping=True)
        if getenv("GI_DEV_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session all objects of the given class.
        If cls is None, queries all types of objects.
        Return:
            Dict of queried classes in the format <class name>.<obj id> = obj.
        """
        if cls is None:
            objs = self.__session.query(Student).all()
            objs.extend(self.__session.query(School).all())
            objs.extend(self.__session.query(Guardian).all())
            objs.extend(self.__session.query(PickAndDrop).all())
            objs.extend(self.__session.query(Guard).all())
            objs.extend(self.__session.query(Notification).all())
            objs.extend(self.__session.query(Registry).all())
            objs.extend(self.__session.query(Jwt_Blacklist).all())
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

    def deleteAll(self):
        """drops all table, commit and close the session."""
        self.reload()
        Base.metadata.drop_all(self.__engine)
        self.get_session()
        self.save()
        self.close()
        return True  

    def close(self):
        """Close the working SQLAlchemy session."""
        self.__session.close()

    def get_session(self):
        """Get the current session."""
        return self.__session