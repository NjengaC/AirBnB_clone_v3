#!/usr/bin/python3
"""File storage class"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import shlex


class FileStorage:
    """File storage start point
    Attributes:
        __file_path: path to the JSON file
        __objects: dictionary
    """
    __file_path = "file.json"
    __objects = {}
    all_classes = {'BaseModel': BaseModel, 'User': User,
                   'State': State, 'City': City, 'Amenity': Amenity,
                   'Place': Place, 'Review': Review}

    def all(self, cls=None):
        """returns a dictionary
        Return:
            returns a dictionary of __object
        """
        all_return = {}
        if cls is not None:
            if type(cls) == str:
                cls = eval(cls)
            cls_dict = {}

            for key, val in self.__objects.items():
                if type(val) == cls:
                    cls_dict[key] = val

            return cls_dict

        return self.__objects

    def new(self, obj):
        """sets __object to given obj
        Args:
            obj: given object
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """serialize the file path to JSON file path
        """
        my_dict = {}
        for key, value in self.__objects.items():
            my_dict[key] = value.to_dict()
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(my_dict, f)

    def reload(self):
        """serialize the file path to JSON file path
        """
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                for key, value in (json.load(f)).items():
                    value = eval(value["__class__"])(**value)
                    self.__objects[key] = value
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """ delete an existing element
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            del self.__objects[key]

    def close(self):
        """ calls reload()
        """
        self.reload()

    def get(self, cls, id):
        """Retrieve a single object"""
        if cls is not None and id is not None:
            objects = self.all(cls)
            for obj in objects.values():
                if obj.id == id:
                    return obj
#            key = str(cls) + '.' + id
#            key = eval(key)
#            obj = self.__objects.get(key, None)
            return obj

        else:
            return None

    def count(self, cls=None):
        """Count the number of objects in file storage"""
        total = 0
        if cls:
            if type(cls) == str:
                cls = eval(cls)
            total = len(self.all(cls))

        elif cls is None:
            total = len(self.__objects)

        return total
