#!/usr/bin/python3

"""
    Contains the TestStudentDocs classes
"""

import inspect
import models
import pycodestyle
import unittest

BaseModel = models.base_model.BaseModel
Student = models.student.Student
student_doc = models.student.__doc__


class TestStudentDocs(unittest.TestCase):
    """Tests to check the documentation and style of Student class"""

    @classmethod
    def setUpClass(self):
        """Set up for docstring tests by extracting all the function
           object.
        """
        self.student_funcs = inspect.getmembers(Student, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/student.py conforms to PEP8 (pycodestyle)."""
        for path in ['models/student.py',
                     'test_student.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_student_docstring(self):
        """Test for the existence of model docstring"""
        self.assertIsNot(student_doc, None,
                         "student.py needs a docstring")
        self.assertTrue(len(student_doc) > 1,
                        "student.py needs a docstring")

    def test_student_class_docstring(self):
        """Test for the Student class docstring"""
        self.assertIsNot(Student.__doc__, None,
                         "Student class needs a docstring")
        self.assertTrue(len(Student.__doc__) >= 1,
                        "Student class needs a docstring")

    def test_student_func_docstrings(self):
        """Test for the presence of docstrings in student methods"""
        for func in self.student_funcs:
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


class TestStudent(unittest.TestCase):
    """Test the Student class"""
    def test_is_subclass(self):
        """Test that Student is a subclass of BaseModel"""
        std = Student()
        self.assertIsInstance(std, BaseModel)
        self.assertTrue(hasattr(std, "id"))
        self.assertTrue(hasattr(std, "created_at"))
        self.assertTrue(hasattr(std, "updated_at"))

    def test_id(self):
        """Test that Student has attr id, and it's None"""
        std = Student()
        self.assertTrue(hasattr(std, "id"))
        self.assertEqual(std.id, None)

    def test_school_id_attr(self):
        """Test Student has attr school_id, and it's None"""
        std = Student()
        self.assertTrue(hasattr(std, "school_id"))
        self.assertEqual(std.school_id, None)

    def test_first_name_attr(self):
        """Test Student has attr first_name, and it's None"""
        std = Student()
        self.assertTrue(hasattr(std, "first_name"))
        self.assertEqual(std.first_name, None)

    def test_last_name_attr(self):
        """Test Student has attr last_name, and it's None"""
        std = Student()
        self.assertTrue(hasattr(std, "last_name"))
        self.assertEqual(std.last_name, None)

    def test_gender_attr(self):
        """Test Student has attr gender, and it's None"""
        std = Student()
        self.assertTrue(hasattr(std, "gender"))
        self.assertEqual(std.gender, None)

    def test_dob_attr(self):
        """Test Student has attr dob, and it's None"""
        std = Student()
        self.assertTrue(hasattr(std, "dob"))
        self.assertEqual(std.dob, None)

    def test_grade_attr(self):
        """Test Student has attr class_grade, and it's None"""
        std = Student()
        self.assertTrue(hasattr(std, "grade"))
        self.assertEqual(std.grade, None)

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        std = Student()
        new_dic = std.to_dict()
        self.assertEqual(type(new_dic), dict)
        self.assertFalse("_sa_instance_state" in new_dic)
        for attr in std.__dict__:
            if attr != "_sa_instance_state":
                self.assertTrue(attr in new_dic)
        self.assertTrue("__class__" in new_dic)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        std = Student()
        dic = std.to_dict()
        self.assertEqual(dic["__class__"], "Student")
        self.assertEqual(type(dic["created_at"]), str)
        self.assertEqual(type(dic["updated_at"]), str)
        self.assertEqual(dic["created_at"], std.created_at.strftime(t_format))
        self.assertEqual(dic["updated_at"], std.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        std = Student()
        d = std.__dict__.copy()
        d.pop("_sa_instance_state", None)
        string = "[Student] ({}) {}".format(std.id, d)
        self.assertEqual(string, str(std))


if __name__ == '__main__':
    unittest.main()
