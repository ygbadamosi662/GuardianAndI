#!/usr/bin/python3

"""
    Test module for the BaseModel, checking for expected behavior
    and documentation.
"""
from datetime import datetime
import time
import inspect
import models
import pycodestyle
import unittest

BaseModel = models.base_model.BaseModel
module_doc = models.base_model.__doc__


class TestBaseModelDocs(unittest.TestCase):
    """Tests to check the documentation and style of BaseModel class"""

    @classmethod
    def setUpClass(self):
        """Set up for docstring tests by extracting all the function
           object.
        """
        self.base_funcs = inspect.getmembers(BaseModel, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/base.py conforms to PEP8 (pycodestyle)."""
        for path in ['models/base.py',
                     'test_base.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for the existence of module docstring"""
        self.assertIsNot(module_doc, None,
                         "base.py needs a docstring")
        self.assertTrue(len(module_doc) > 1,
                        "base.py needs a docstring")

    def test_class_docstring(self):
        """Test for the BaseModel class docstring"""
        self.assertIsNot(BaseModel.__doc__, None,
                         "BaseModel class needs a docstring")
        self.assertTrue(len(BaseModel.__doc__) >= 1,
                        "BaseModel class needs a docstring")

    def test_func_docstrings(self):
        """Test for the presence of docstrings in BaseModel methods"""
        for func in self.base_funcs:
            with self.subTest(function=func):
                self.assertIsNot(
                    func[1].__doc__,
                    None,
                    "{:s} method needs a docstring".format(func[0])
                )
                self.assertTrue(
                    len(func[1].__doc__) > 1,
                    "{:s} method needs a docstring".format(func[0])
                )


class TestBaseModel(unittest.TestCase):
    """ Test the BaseModel class """
    def test_instantiation(self):
        """ Test that object is correctly created """
        instance = BaseModel()
        self.assertIs(type(instance), BaseModel)
        attrs_types = {
            "created_at": datetime,
            "updated_at": datetime,
        }
        for attr, typ in attrs_types.items():
            with self.subTest(attr=attr, typ=typ):
                self.assertIn(attr, instance.__dict__)
                self.assertIs(type(instance.__dict__[attr]), typ)

    def test_to_dict(self):
        """ Test conversion of object attributes to dictionary. """
        instance = BaseModel()
        instance.testname = "Guard&I"
        instance.number = 25
        dic = instance.to_dict()
        expected_attrs = ["created_at",
                          "updated_at",
                          "testname",
                          "number",
                          "__class__"]
        self.assertCountEqual(dic.keys(), expected_attrs)
        self.assertEqual(dic['__class__'], 'BaseModel')
        self.assertEqual(dic['testname'], "Axist")
        self.assertEqual(dic['number'], 25)

    def test_to_dict_values(self):
        """ Test that values in dict returned from to_dict are correct. """
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        bm = BaseModel()
        new_d = bm.to_dict()
        self.assertEqual(new_d["__class__"], "BaseModel")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], bm.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], bm.updated_at.strftime(t_format))

    def test_str(self):
        """ Test that the str method has the correct output. """
        instance = BaseModel()
        string = "[BaseModel] ({}) {}".format(instance.id, instance.__dict__)
        self.assertEqual(string, str(instance))

    def test_save(self):
        """
            Test to show updated_at changed after storage.save
            function is called.
        """
        inst = BaseModel()
        old_created_at = inst.created_at
        old_updated_at = inst.updated_at
        time.sleep(0.0001)
        inst.save()
        new_created_at = inst.created_at
        new_updated_at = inst.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertEqual(old_created_at, new_created_at)


if __name__ == '__main__':
    unittest.main()
