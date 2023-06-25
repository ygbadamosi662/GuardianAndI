#!/usr/bin/python3

"""
    Contains the TestPickAndDropDocs classes
"""

import inspect
import models
import pycodestyle
import unittest

BaseModel = models.base_model.BaseModel
PickAndDrop = models.pick_and_drop.PickAndDrop
pick_and_drop_doc = models.pick_and_drop.__doc__


class TestPickAndDropDocs(unittest.TestCase):
    """Tests to check the documentation and style of PickAndDrop class"""

    @classmethod
    def setUpClass(self):
        """Set up for docstring tests by extrpding all the function
           object.
        """
        self.pd_funcs = inspect.getmembers(PickAndDrop, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/pick_and_drop.py conforms to PEP8 (pycodestyle)"""
        for path in ['models/pick_and_drop.py',
                     'test_pick_and_drop.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_pick_and_drop_docstring(self):
        """Test for the existence of model docstring"""
        self.assertIsNot(pick_and_drop_doc, None,
                         "pick_and_drop.py needs a docstring")
        self.assertTrue(len(pick_and_drop_doc) > 1,
                        "pick_and_drop.py needs a docstring")

    def test_pick_and_drop_class_docstring(self):
        """Test for the PickAndDrop class docstring"""
        self.assertIsNot(PickAndDrop.__doc__, None,
                         "PickAndDrop class needs a docstring")
        self.assertTrue(len(PickAndDrop.__doc__) >= 1,
                        "PickAndDrop class needs a docstring")

    def test_pick_and_drop_func_docstrings(self):
        """Test for the presence of docstrings in PickAndDrop methods"""
        for func in self.pd_funcs:
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


class TestPickAndDrop(unittest.TestCase):
    """Test the PickAndDrop class"""
    def test_is_subclass(self):
        """Test that PickAndDrop is a subclass of BaseModel"""
        pd = PickAndDrop()
        self.assertIsInstance(pd, BaseModel)
        self.assertTrue(hasattr(pd, "id"))
        self.assertTrue(hasattr(pd, "created_at"))
        self.assertTrue(hasattr(pd, "updated_at"))

    def test_school_id_attr(self):
        """Test PickAndDrop has attr school_id, and it's None"""
        pd = PickAndDrop()
        self.assertTrue(hasattr(pd, "school_id"))
        self.assertEqual(pd.school_id, None)

    def test_student_id_attr(self):
        """Test PickAndDrop has attr student_id, and it's None"""
        pd = PickAndDrop()
        self.assertTrue(hasattr(pd, "student_id"))
        self.assertEqual(pd.student_id, None)

    def test_guardian_id_attr(self):
        """Test PickAndDrop has attr guardian_id, and it's None"""
        pd = PickAndDrop()
        self.assertTrue(hasattr(pd, "guardian_id"))
        self.assertEqual(pd.guardian_id, None)

    def test_action_attr(self):
        """Test PickAndDrop has attr pdion, and it's None"""
        pd = PickAndDrop()
        self.assertTrue(hasattr(pd, "action"))
        self.assertEqual(pd.action, None)

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        pd = PickAndDrop()
        new_dic = pd.to_dict()
        self.assertEqual(type(new_dic), dict)
        self.assertFalse("_sa_instance_state" in new_dic)
        for attr in pd.__dict__:
            if attr != "_sa_instance_state":
                self.assertTrue(attr in new_dic)
        self.assertTrue("__class__" in new_dic)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        pd = PickAndDrop()
        dic = pd.to_dict()
        self.assertEqual(dic["__class__"], "PickAndDrop")
        self.assertEqual(type(dic["created_at"]), str)
        self.assertEqual(type(dic["updated_at"]), str)
        self.assertEqual(dic["created_at"], pd.created_at.strftime(t_format))
        self.assertEqual(dic["updated_at"], pd.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        pd = PickAndDrop()
        d = pd.__dict__.copy()
        d.pop("_sa_instance_state", None)
        string = "[PickAndDrop] ({}) {}".format(pd.id, d)
        self.assertEqual(string, str(pd))


if __name__ == '__main__':
    unittest.main()
