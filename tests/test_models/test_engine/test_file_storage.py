#!/usr/bin/python3
"""test for file storage"""
import unittest
import pycodestyle
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    '''This class tests the FileStorage class'''

    @classmethod
    def setUpClass(cls):
        """Set up for the test class"""
        cls.storage = FileStorage()

    def setUp(self):
        """Set up for each test case"""
        self.storage.reload()

    def tearDown(self):
        """Tear down after each test case"""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_pycodestyle_FileStorage(self):
        """Test for PEP 8 style"""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0, "Fix PEP 8 style issues")

    def test_all(self):
        """Test the all method"""
        obj = self.storage.all()
        self.assertIsNotNone(obj)
        self.assertEqual(type(obj), dict)
        self.assertIs(obj, self.storage._FileStorage__objects)

    def test_new(self):
        """Test the new method"""
        user = User()
        user.id = 123455
        user.name = "Kevin"
        self.storage.new(user)
        key = f"{user.__class__.__name__}.{str(user.id)}"
        self.assertIn(key, self.storage._FileStorage__objects)

    def test_reload(self):
        """Test the reload method"""
        self.storage.save()
        with open("file.json", 'r') as f:
            lines = f.readlines()
        self.storage.save()
        with open("file.json", 'r') as f:
            lines2 = f.readlines()
        self.assertEqual(lines, lines2)

    def test_get_by_class_and_id(self):
        """Test the get method by class and ID"""
        user = User()
        self.storage.new(user)
        self.storage.save()
        retrieved_user = self.storage.get(User, user.id)
        self.assertEqual(retrieved_user, user)

    def test_get_non_existing_object(self):
        """Test the get method for non-existing object"""
        retrieved_obj = self.storage.get(User, "non_existing_id")
        self.assertIsNone(retrieved_obj)

    def test_get_with_invalid_parameters(self):
        """Test the get method with invalid parameters"""
        retrieved_obj = self.storage.get(None, None)
        self.assertIsNone(retrieved_obj)

    def test_count_all_objects(self):
        """Test the count method for all objects"""
        obj1 = BaseModel()
        obj2 = State()
        obj3 = City()
        self.storage.new(obj1)
        self.storage.new(obj2)
        self.storage.new(obj3)
        self.assertEqual(self.storage.count(), self.storage.count())

    def test_count_objects_by_class(self):
        """Test the count method for objects by class"""
        obj1 = BaseModel()
        obj2 = State()
        obj3 = State()
        self.storage.new(obj1)
        self.storage.new(obj2)
        self.storage.new(obj3)
        self.assertEqual(self.storage.count(State), self.storage.count(State))


if __name__ == "__main__":
    unittest.main()

