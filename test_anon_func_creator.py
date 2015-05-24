import unittest
import math

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

    def test_one_arg_wrong_num_args(self):
        string = "2*_"
        func = create_func(string)
        self.assertRaises(TypeError, func, 1, 5)
        self.assertRaises(TypeError, func)

    def test_one_arg(self):
        string = "2*_"
        func = create_func(string)
        self.assertEqual(func(1), 2)
        self.assertEqual(func(5), 10)
        self.assertEqual(func(-5), -10)

    def test_two_args(self):
        string = "2*_1 + _2"
        func = create_func(string)
        self.assertEqual(func(1, 6), 8)
        self.assertEqual(func(5, 7), 17)
        self.assertEqual(func(-5, 3), -7)

    def test_scope_is_not_overwritten(self):
        _1 = 5
        string = "_1 + 10"
        func = create_func(string)
        self.assertEqual(func(20), 30)
        self.assertEqual(_1, 5)

    def test_two_scopes_up(self):
        string = "_1 + math.cos(0)"
        func = create_func(string)
        self.assertEqual(func(5), 6)