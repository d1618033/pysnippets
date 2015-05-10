import infinite_fib
import unittest


def take(elems, n):
    for i, elem in enumerate(elems):
        if i >= n:
            return
        yield elem
    if i < n - 1:
        raise ValueError("n({n}) is out of bounds for iterable of size {size}".format(n=n, size=i))


class TestTake(unittest.TestCase):
    def test_zero(self):
        elems = [1, 2, 3]
        actual = list(take(elems, 0))
        expected = []
        self.assertEqual(actual, expected)

    def test_one(self):
        elems = [5, 2, 3]
        actual = list(take(elems, 1))
        expected = [5]
        self.assertEqual(actual, expected)

    def test_two(self):
        elems = [5, 2, 3]
        actual = list(take(elems, 2))
        expected = [5, 2]
        self.assertEqual(actual, expected)

    def test_all(self):
        elems = [5, 2, 3]
        actual = list(take(elems, 3))
        expected = elems
        self.assertEqual(actual, expected)

    def test_iterator(self):
        elems = range(10)
        actual = list(take(elems, 3))
        expected = [0, 1, 2]
        self.assertEqual(actual, expected)

    def test_out_of_bounds(self):
        elems = range(10)
        self.assertRaises(ValueError, lambda: list(take(elems, 11)))


class TestInfiniteFib:
    def get_result(self):
        raise NotImplementedError

    def assert_is_fib_sequence(self, n):
        prev1 = None
        prev2 = None
        for i, elem in enumerate(take(self.get_result(), n)):
            with self.subTest(i=i):
                if prev1 is None:
                    prev1 = elem
                    self.assertEqual(elem, 0)
                elif prev2 is None:
                    prev2 = elem
                    self.assertEqual(elem, 1)
                else:
                    self.assertEqual(elem, prev1 + prev2)
                    prev1, prev2 = prev2, elem

    def test_10_items(self):
        self.assert_is_fib_sequence(10)

    def test_100_items(self):
        self.assert_is_fib_sequence(100)


class TestIterativeInfiniteFib(unittest.TestCase, TestInfiniteFib):
    def get_result(self):
        return infinite_fib.itertive_infinite_fib()


class TestRecursiveInfiniteFib(unittest.TestCase, TestInfiniteFib):
    def get_result(self):
        return infinite_fib.recursive_infinite_fib()