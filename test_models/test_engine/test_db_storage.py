#!/usr/bin/python3

"""
    Contains the TestDBStorage.
"""

import inspect
import models
from models import storage
import pycodestyle
import unittest

DBStorage = models.engine.db_storage.DBStorage
dbstorage_doc = models.engine.db_storage.__doc__
School = models.school.School


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance(self):
        """
           Test that models/engine/db_storage.py
           conforms to PEP8 (pycodestyle).
        """
        for path in ['models/engine/db_storage.py',
                     'test_db_storage.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(dbstorage_doc, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(dbstorage_doc) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""
    def test_all(self):
        """
           Test that all returns all data based on the provided cls.
        """

        dic = {'email': 'ice@ice.com', 'password': 'Ice1231#'}
        # create an instance to test
        instance = School(**dic)
        storage.new(instance)
        storage.save()

        data = storage.all(School)
        self.assertGreater(len(data), 0)

    def test_new_save(self):
        """Test that save properly saves objects to db"""

        dic = {'email': 'gi@gmail.com', 'password': 'GuardianI1'}
        # fetch old data
        objs_old = storage.all(School)

        # create instance
        instance = School(**dic)
        storage.new(instance)
        storage.save()

        # fetch new data
        objs_new = storage.all(School)

        self.assertNotEqual(len(objs_old), len(objs_new))

    def test_delete(self):
        """Test that delete properly remove the obj from the db"""

        dic = {'email': 'gandi@gandi.com', 'password': 'Guardian1'}
        # create instance
        instance = School(**dic)
        storage.new(instance)
        storage.save()

        # before delete
        objs_old = storage.all(School)
        # delete
        storage.delete(instance)
        #after delete
        objs_new = storage.all(School)
        self.assertNotEqual(len(objs_old), len(objs_new))

if __name__ == "__main__":
    unittest.main()
