from unittest import TestCase
from fast_pow import python_pow, slow_iter_pow, fast_iter_pow, slow_recursive_pow, fast_recursive_pow


class PowTester:
    func = None  # replace this

    @classmethod
    def get_actual(cls, x, n):
        return cls.func(x, n)

    def assert_pow_is_correct(self, x, n, expected):
        actual = self.get_actual(x, n)
        self.assertEqual(actual, expected)

    def test_zero_pow_zero(self):
        self.assert_pow_is_correct(0, 0, 1)

    def test_anything_pow_zero(self):
        self.assert_pow_is_correct(10, 0, 1)

    def test_zero_pow_one(self):
        self.assert_pow_is_correct(0, 1, 0)

    def test_anything_pow_one(self):
        self.assert_pow_is_correct(10, 1, 10)

    def test_pow_two(self):
        self.assert_pow_is_correct(10, 2, 100)

    def test_pow_five(self):
        self.assert_pow_is_correct(3, 5, 243)

    def test_pow_large_number_pow_two(self):
        self.assert_pow_is_correct(3, 32, 1853020188851841)

    def test_pow_large_number_not_pow_two(self):
        self.assert_pow_is_correct(3, 18, 387420489)


class TestPythonPow(TestCase, PowTester):
    func = python_pow


class TestSlowIterPow(TestCase, PowTester):
    func = slow_iter_pow


class TestFastIterPow(TestCase, PowTester):
    func = fast_iter_pow


class TestSlowRecursivePow(TestCase, PowTester):
    func = slow_recursive_pow


class TestFastRecursivePow(TestCase, PowTester):
    func = fast_recursive_pow