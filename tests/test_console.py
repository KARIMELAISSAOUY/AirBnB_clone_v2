#!/usr/bin/python3
"""A unit test module for the console (command interpreter).
"""
import json
import MySQLdb
import os
import sqlalchemy
import unittest
from io import StringIO
from unittest.mock import patch

from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User
from tests import clear_stream

class TestHBNBCommand(unittest.TestCase):
    """Represents the test class for the HBNBCommand class.
    """

    def setUp(self):
        """Common setup for all tests.
        """
        self.cons = HBNBCommand()
        self.db_config = {
            "host": os.getenv('HBNB_MYSQL_HOST'),
            "port": 3306,
            "user": os.getenv('HBNB_MYSQL_USER'),
            "passwd": os.getenv('HBNB_MYSQL_PWD'),
            "db": os.getenv('HBNB_MYSQL_DB')
        }

    # ... (other tests)

    def _execute_query(self, query):
        """Helper method to execute a query on the database.
        """
        dbc = MySQLdb.connect(**self.db_config)
        cursor = dbc.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        dbc.close()
        return result

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_create(self):
        """Tests the create command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            # ... (rest of the test)
    
    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_show(self):
        """Tests the show command with the database storage.
        """
        # ... (rest of the test)
    
    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_count(self):
        """Tests the count command with the database storage.
        """
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            dbc = MySQLdb.connect(**self.db_config)
            cursor = dbc.cursor()
            cursor.execute('SELECT COUNT(*) FROM states;')
            res = cursor.fetchone()
            prev_count = int(res[0])
            cons.onecmd('create State name="Enugu"')
            clear_stream(cout)
            cons.onecmd('count State')
            cnt = cout.getvalue().strip()
            self.assertEqual(int(cnt), prev_count + 1)
            clear_stream(cout)
            cons.onecmd('count State')
            cursor.close()
            dbc.close()

if __name__ == '__main__':
    unittest.main()