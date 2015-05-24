import unittest

from anon_func_creator import create_func


class TestCreateFunc(unittest.TestCase):
    def test_no_args_function(self):
        string = "1+1"
        func = create_func(string)
        self.assertEqual(func(), 2)

    def test_no_args_with_scope(self):
        x = 10
        string = "x+1"
        func = create_func(string)
        self.assertEqual(func(), 11)