#!/usr/bin/python3

"""
    Contains the TestSchoolDocs classes
"""

import inspect
import models
import pycodestyle
import unittest

BaseModel = models.base_model.BaseModel
School = models.school.School
school_doc = models.school.__doc__


class TestSchoolDocs(unittest.TestCase):
    """Tests to check the documentation and style of School class"""

    @classmethod
    def setUpClass(self):
        """Set up for docstring tests by extracting all the function
           object.
        """

        self.school_funcs = inspect.getmembers(School, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/school.py conforms to PEP8 (pycodestyle)."""
        for path in ['models/school.py',
                     'test_school.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_school_docstring(self):
        """Test for the existence of model docstring"""
        self.assertIsNot(school_doc, None,
                         "school.py needs a docstring")
        self.assertTrue(len(school_doc) > 1,
                        "school.py needs a docstring")

    def test_school_class_docstring(self):
        """Test for the School class docstring"""
        self.assertIsNot(School.__doc__, None,
                         "School class needs a docstring")
        self.assertTrue(len(School.__doc__) >= 1,
                        "School class needs a docstring")

    def test_school_func_docstrings(self):
        """Test for the presence of docstrings in school methods"""
        for func in self.school_funcs:
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


class TestSchool(unittest.TestCase):
    """Test the School class"""
    def test_is_subclass(self):
        """Test that School is a subclass of BaseModel"""
        sch = School()
        self.assertIsInstance(sch, BaseModel)
        self.assertTrue(hasattr(sch, "created_at"))
        self.assertTrue(hasattr(sch, "updated_at"))

    def test_id(self):
        """Test that Student has attr id, and it's None"""
        sch = School()
        self.assertTrue(hasattr(sch, "id"))
        self.assertEqual(sch.id, None)

    def test_email_attr(self):
        """Test School has attr email, and it's None"""
        sch = School()
        self.assertTrue(hasattr(sch, "email"))
        self.assertEqual(sch.email, None)

    def test_password_attr(self):
        """Test School has attr password, and it's encrypt"""
        sch = School()
        sch.password = 'Guardian123#'
        self.assertTrue(hasattr(sch, "password"))
        self.assertNotEqual(sch.password, 'Guardian123#')

    def test_name_attr(self):
        """Test School has attr name, and it's None"""
        sch = School()
        self.assertTrue(hasattr(sch, "name"))
        self.assertEqual(sch.name, None)

    def test_address_attr(self):
        """Test School has attr address, and it's None"""
        sch = School()
        self.assertTrue(hasattr(sch, "address"))
        self.assertEqual(sch.address, None)

    def test_city_attr(self):
        """Test School has attr city, and it's None"""
        sch = School()
        self.assertTrue(hasattr(sch, "city"))
        self.assertEqual(sch.city, None)

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        sch = School()
        new_dic = sch.to_dict()
        self.assertEqual(type(new_dic), dict)
        self.assertFalse("_sa_instance_state" in new_dic)
        for attr in sch.__dict__:
            if attr != "_sa_instance_state":
                self.assertTrue(attr in new_dic)
        self.assertTrue("__class__" in new_dic)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        sch = School()
        dic = sch.to_dict()
        self.assertEqual(dic["__class__"], "School")
        self.assertEqual(type(dic["created_at"]), str)
        self.assertEqual(type(dic["updated_at"]), str)
        self.assertEqual(dic["created_at"], sch.created_at.strftime(t_format))
        self.assertEqual(dic["updated_at"], sch.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        sch = School()
        d = sch.__dict__.copy()
        d.pop("_sa_instance_state", None)
        string = "[School] ({}) {}".format(sch.id, d)
        self.assertEqual(string, str(sch))


if __name__ == '__main__':
    unittest.main()
