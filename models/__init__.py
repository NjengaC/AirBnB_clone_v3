#!/usr/bin/python3
"""
*This module instantiates an object of class FileStorage plus the
*previous filestorage. This “switch” allows change storage type
*directly by using an environment variable
"""

from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from os import getenv

if getenv("HBNB_TYPE_STORAGE") == "db":
    storage = DBStorage()
    storage.reload()

else:
    storage = FileStorage()
    storage.reload()
