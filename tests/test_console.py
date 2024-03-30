#!/usr/bin/python3
"""test for console"""
import unittest
from unittest.mock import patch
from io import StringIO
import pycodestyle
import os
import json
import console
import tests
from console import HBNBCommand
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage
import sqlalchemy
import MySQLdb


class TestConsole(unittest.TestCase):
    """this will test the console"""

    @classmethod
    def setUpClass(cls):
        """Setup for the test"""
        cls.consol = HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        """At the end of the test this will tear it down"""
        del cls.consol

    def tearDown(self):
        """Remove temporary file (file.json) created as a result"""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        except PermissionError as e:
            print(f"Permission error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def clear_stream(self, stream):
        """Clears the contents of the stream and resets the position."""
        stream.seek(0)
        stream.truncate(0)

    def test_pycodestyle_console(self):
        """pycodestyle console.py"""
        style = pycodestyle.StyleGuide(quiet=True)
        p = style.check_files(["console.py"])
        self.assertEqual(p.total_errors, 0)

    def test_docstrings_in_console(self):
        """checking for docstrings"""
        self.assertIsNotNone(console.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)
        self.assertIsNotNone(HBNBCommand.do_count.__doc__)
        self.assertIsNotNone(HBNBCommand.default.__doc__)

    def test_emptyline(self):
        """Test empty line input"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("\n")
            self.assertEqual('', f.getvalue())

    def test_quit(self):
        """test quit command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            with self.assertRaises(SystemExit):
                self.consol.onecmd("quit")

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_create(self):
        """Test create command inpout"""
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            cons.onecmd('create City name="Texas"')
            mdl_id = cout.getvalue().strip()
            self.clear_stream(cout)
            self.assertIn('City.{}'.format(mdl_id), storage.all().keys())
            cons.onecmd('show City {}'.format(mdl_id))
            self.assertIn("'name': 'Texas'", cout.getvalue().strip())
            self.clear_stream(cout)
            cons.onecmd('create User name="James" age=17 height=5.9')
            mdl_id = cout.getvalue().strip()
            self.assertIn('User.{}'.format(mdl_id), storage.all().keys())
            cons.onecmd('show User {}'.format(mdl_id))
            self.assertIn("'name': 'James'", cout.getvalue().strip())
            self.assertIn("'age': '17'", cout.getvalue().strip())
            self.assertIn("'height': '5.9'", cout.getvalue().strip())

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_create_with_db(self):
        """Tests the create command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
        self.clear_stream(cout)
        cons.onecmd('create User email="john25@gmail.com" password="123"')
        mdl_id = cout.getvalue().strip()
        dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
        )
        dbc.close()

    def test_show(self):
        """Test show command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show asdfsdrfs")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("show BaseModel")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())

    def test_destroy(self):
        """Test destroy command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy Galaxy")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("destroy User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())

    def test_all(self):
        """Test all command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.consol.onecmd("all asdfsdfsd")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())


if __name__ == "__main__":
    unittest.main()
