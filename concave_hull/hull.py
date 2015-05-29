#!/usr/bin/python3

import os
from subprocess import Popen, PIPE, STDOUT
import io
import itertools

import matplotlib.pyplot as plt


DIR = os.path.dirname(__file__)
hull_path = os.path.join(DIR, "hull", "hull.exe")
output_file = 'hout-alf'


def get_alpha_shape(points: "list[(float, float)]") -> "list[(float, float)]":
    """
    Returns the concave hull around a given set of points.
    (Calculates the "best" alpha automatically)
    :param points: A list of 2d points
    :return: The vertices of the alpha shape.
    """
    bio = io.BytesIO()
    for point in points:
        bio.write("{0} {1}\n".format(*point).encode())

    p = Popen([hull_path, '-A', '-oN', '-m1000000'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    stdoutput, stderr = p.communicate(input=bio.getvalue())
    if stderr is not None:
        raise RuntimeError("Got errors when running hull: {0}".format(stderr))
    with open(output_file) as output:
        next(output)
        results_indices = [map(int, line.strip().split()) for line in output]
    os.remove(output_file)
    edges = [(points[i], points[j]) for i, j in results_indices]
    return edges_to_vertices(order_edges(edges))


def plot_hull(ax: plt.Axes, points: "list[(float, float)]", vertices: "list[(float, float)]") -> None:
    """
    Plots the points and the hull.
    :param ax: matplotlib axes, where the hull will be be plotted
    :param points: A list of 2d points
    :param vertices: A list of vertices of the hull to plot
    """
    for data, color in [(points, 'b'), (vertices, 'r')]:
        ax.plot(*zip(*data), color=color, marker='o', linestyle='')
    poly = plt.Polygon(vertices, linewidth=2, facecolor='r', edgecolor='r', linestyle='solid', alpha=0.5)
    ax.add_patch(poly)


def pairs(items: "list[T]") -> "list[(T, T)]":
    """
    Returns pairs of items in items.
    e.g:
    >>> pairs([1, 2, 3])
    [(1, 2), (2, 3)]

    :param items: a list
    :return: a list of pairs
    """
    return [(items[i], items[i+1]) for i in range(len(items)-1)]


def get_vertices_set(edges: "list[((float, float), (float, float))") -> "list[(float, float)]":
    """
    Returns a set of vertices from a given list of edges
    :param edges: a list of edges
    :return: a list of vertices
    """
    return set(itertools.chain(*edges))


def order_edges(edges: "list[((float, float), (float, float))") -> "list[(float, float)]":
    """
    Orders edges so that one edge always leads to the next
    :param edges: A list of edges
    :return: A list of sorted edges
    """
    edge_set = set(edges)
    current_edge = edge_set.pop()
    edges = [current_edge]
    while len(edge_set):
        for other_edge in edge_set:
            if current_edge[1] == other_edge[0]:
                current_edge = other_edge
                edge_to_remove = other_edge
                edges.append(current_edge)
                break
            elif current_edge[1] == other_edge[1]:
                current_edge = (other_edge[1], other_edge[0])
                edge_to_remove = other_edge
                edges.append(current_edge)
                break
        else:
            raise AssertionError("No edge starting from {0}".format(current_edge[1]))
        edge_set.remove(edge_to_remove)
    return edges


def edges_to_vertices(edges: "list[((float, float), (float, float))") -> "list[(float, float)]":
    """
    Converts *sorted* edges to vertices
    :param edges: a list of edges
    :return: a list of vertices
    """
    vertices = []
    for v1, v2 in edges:
        vertices.append(v1)
    return vertices


def polygon_area(vertices: "list[(float, float)]") -> float:
    """
    Returns the area of a simple polygon enclosed by the given vertices
    :param vertices: a list of vertices
    :return: The area of the polygon.
    """
    n = len(vertices)
    a = 0.0
    for i in range(n):
        j = (i + 1) % n
        a += abs(vertices[i][0] * vertices[j][1]-vertices[j][0] * vertices[i][1])
    result = a / 2.0
    return result


def read_points(stream: "collections.Iterable[str]") -> "list[(float, float)]":
    """
    Reads 2d points from a string stream and converts them to a list of (float, float)
    :param stream: an iterable of strings of the format ["x y"]
    :return: a list of points
    >>> read_points(["1 1.5", "10 3"])
    [(1.0, 1.5), (10.0, 3.0)]
    """
    points = [tuple([float(i) for i in line.rstrip().split()]) for line in stream]
    return points


def main(stream: "collections.Iterable[str]") -> None:
    """
    Given a stream of points calculates the hull and plots it
    :param stream: a list of strings of the format ["x y"]
    """
    points = read_points(stream)
    fig, ax = plt.subplots()
    plot_hull(ax, points, get_alpha_shape(points))
    plt.show()


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2:
        with open(sys.argv[1]) as f:
            main(f)
    else:
        main(sys.stdin)
