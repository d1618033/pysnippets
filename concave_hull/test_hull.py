import unittest
from concave_hull import hull


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