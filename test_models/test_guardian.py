#!/usr/bin/python3

"""
    Contains the TestGuardianDocs classes
"""

import inspect
import models
import pycodestyle
import unittest

BaseModel = models.base_model.BaseModel
Guardian = models.guardian.Guardian
guardian_doc = models.guardian.__doc__


class TestGuardianDocs(unittest.TestCase):
    """Tests to check the documentation and style of Guardian class"""

    @classmethod
    def setUpClass(self):
        """Set up for docstring tests by extracting all the function
           object.
        """
        self.guardian_funcs = inspect.getmembers(Guardian, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/guardian.py conforms to PEP8 (pycodestyle)."""
        for path in ['models/guardian.py',
                     'test_guardian.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_guardian_docstring(self):
        """Test for the existence of model docstring"""
        self.assertIsNot(guardian_doc, None,
                         "guardian.py needs a docstring")
        self.assertTrue(len(guardian_doc) > 1,
                        "guardian.py needs a docstring")

    def test_guardian_class_docstring(self):
        """Test for the Guardian class docstring"""
        self.assertIsNot(Guardian.__doc__, None,
                         "Guardian class needs a docstring")
        self.assertTrue(len(Guardian.__doc__) >= 1,
                        "Guardian class needs a docstring")

    def test_guardian_func_docstrings(self):
        """Test for the presence of docstrings in guardian methods"""
        for func in self.guardian_funcs:
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


class TestGuardian(unittest.TestCase):
    """Test the Guardian class"""
    def test_is_subclass(self):
        """Test that Guardian is a subclass of BaseModel"""
        gua = Guardian()
        self.assertIsInstance(gua, BaseModel)
        self.assertTrue(hasattr(gua, "id"))
        self.assertTrue(hasattr(gua, "created_at"))
        self.assertTrue(hasattr(gua, "updated_at"))

    def test_id(self):
        """Test that Student has attr id, and it's None"""
        gua = Guardian()
        self.assertTrue(hasattr(gua, "id"))
        self.assertEqual(gua.id, None)

    # def test_student_id_attr(self):
    #     """Test Student has attr school_id, and it's None"""
    #     gua = Guardian()
    #     self.assertTrue(hasattr(gua, "student_id"))
    #     self.assertEqual(gua.student_id, None)

    def test_email_attr(self):
        """Test Guardian has attr email, and it's None"""
        gua = Guardian()
        self.assertTrue(hasattr(gua, "email"))
        self.assertEqual(gua.email, None)

    def test_password_attr(self):
        """Test Guardian has attr password, and it's encrypted"""
        gua = Guardian()
        gua.password = "Wardproof123#"
        self.assertTrue(hasattr(gua, "password"))
        self.assertNotEqual(gua.password, "Wardproof123#")

    def test_first_name_attr(self):
        """Test Guardian has attr first_name, and it's None"""
        gua = Guardian()
        self.assertTrue(hasattr(gua, "first_name"))
        self.assertEqual(gua.first_name, None)
        
    def test_last_name_attr(self):
        """Test Guardian has attr last_name, and it's None"""
        gua = Guardian()
        self.assertTrue(hasattr(gua, "last_name"))
        self.assertEqual(gua.last_name, None)

    def test_gender_attr(self):
        """Test Guardian has attr gender, and it's None"""
        gua = Guardian()
        self.assertTrue(hasattr(gua, "gender"))
        self.assertEqual(gua.gender, None)

    def test_tag_attr(self):
        """Test Guardian has attr tag, and it's None"""
        gua = Guardian()
        self.assertTrue(hasattr(gua, "tag"))
        self.assertEqual(gua.tag, None)

    def test_dob_attr(self):
        """Test Guardian has attr dob, and it's None"""
        gua = Guardian()
        self.assertTrue(hasattr(gua, "dob"))
        self.assertEqual(gua.dob, None)

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        gua = Guardian()
        new_dic = gua.to_dict()
        self.assertEqual(type(new_dic), dict)
        self.assertFalse("_sa_instance_state" in new_dic)
        for attr in gua.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_dic)
        self.assertTrue("__class__" in new_dic)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        gua = Guardian()
        dic = gua.to_dict()
        self.assertEqual(dic["__class__"], "Guardian")
        self.assertEqual(type(dic["created_at"]), str)
        self.assertEqual(type(dic["updated_at"]), str)
        self.assertEqual(dic["created_at"], gua.created_at.strftime(t_format))
        self.assertEqual(dic["updated_at"], gua.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        gua = Guardian()
        string = "[Guardian] ({}) {}".format(gua.id, gua.__dict__)
        self.assertEqual(string, str(gua))

if __name__ == '__main__':
    unittest.main()
