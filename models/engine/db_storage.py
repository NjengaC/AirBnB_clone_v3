#!/usr/bin/python3
"""dynamic database"""
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from sqlalchemy import create_engine
from models.base_model import BaseModel, Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity

classes = {'User': User,
           'State': State, 'City': City, 'Amenity': Amenity,
           'Place': Place, 'Review': Review}


class DBStorage():
    """New engine DBStorage"""

    __engine = None
    __session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        env = getenv("HBNB_ENV")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")

        self.__engine = (create_engine(f"mysql+mysqldb://{user}:"
            f"{passwd}@{host}/{db}", pool_pre_ping=True))

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session (self.__session) all objects
        depending of the class name (argument cls)
        """
        dictionary = {}
        if cls is not None:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)

            for item in query:
                k = f"{type(item).__name__}.{item.id}"
                dictionary[k] = item
            return dictionary
        else:
            alll = [State, City, User, Place, Review, Amenity]
            for i in alll:
                query = self.__session.query(i)
                for item in query:
                    k = f"{type(item).__name__}.{item.id}"
                    dictionary[k] = item
        return dictionary

    def new(self, obj):
        """adds an object to the current database session (self.__session)"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        sess = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess)
        self.__session = Session()

    def close(self):
        """Closes the session"""
        self.__session.close()

    def get(self, cls, id):
        """Retrieve only one object"""
        if cls is not None and id is not None:
            if type(cls) == str:
                cls = eval(cls)
            result = self.__session.query(cls).filter(id == id).first()
            return result
        else:
            return None

    def count(self, cls=None):
        """
        Count the number of objects in storage
        """
        total = 0
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            total = self.__session.query(cls).count()

        elif cls is None:
            for cls in classes.values():
                total += self.__session.query(cls).count()
        return total
