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

    def test_one_arg(self):
        string = "2*#"
        func = create_func(string)
        self.assertEqual(func(1), 2)
        self.assertEqual(func(5), 10)
        self.assertEqual(func(-5), -10)