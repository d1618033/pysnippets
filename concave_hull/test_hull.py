import unittest
from concave_hull import hull

import numpy as np


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


class TestPolygonArea(unittest.TestCase):
    def test_circle(self):
        x = np.arange(0, 1, 0.00001)
        y = np.sqrt(1-x**2)
        points = list(zip(x, y))
        edges = hull.pairs(points)
        expected_area = np.pi / 4
        actual_area = hull.polygon_area(edges)
        self.assertAlmostEqual(expected_area, actual_area, places=2)

    def test_rectangle(self):
        vertices = [(0, 0), (0, 5), (10, 5), (10, 0), (0, 0)]
        edges = hull.pairs(vertices)
        expected_area = 50
        actual_area = hull.polygon_area(edges)
        self.assertEqual(expected_area, actual_area)