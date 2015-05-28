import unittest
from concave_hull import hull


class TestPairs(unittest.TestCase):
    def test_two(self):
        items = [1, 5]
        expected = [(1, 5)]
        actual = hull.pairs(items)
        self.assertEqual(actual, expected)

    def test_five(self):
        items = [1, 2, 3, 6, 7]
        expected = [(1, 2), (2, 3), (3, 6), (6, 7)]
        actual = hull.pairs(items)
        self.assertEqual(actual, expected)


class TestEdgesToVertices(unittest.TestCase):
    def test_ordered(self):
        edges = [
            [(1, 5), (2, 3)],
            [(2, 3), (5, 7)],
            [(5, 7), (7, 9)]
        ]
        expected = [(1, 5), (2, 3), (5, 7), (7, 9)]
        actual = hull.edges_to_vertices(edges)
        self.assertEqual(expected, actual)

    def test_ordered_between_but_not_within(self):
        edges = [
            [(2, 3), (1, 5)],
            [(2, 3), (5, 7)],
            [(7, 9), (5, 7)]
        ]
        expected = [(1, 5), (2, 3), (5, 7), (7, 9)]
        actual = hull.edges_to_vertices(edges)
        self.assertEqual(expected, actual)