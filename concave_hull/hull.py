#!/usr/bin/python3

import os
from subprocess import Popen, PIPE, STDOUT
import io
import matplotlib.pyplot as plt
import itertools


DIR = os.path.dirname(__file__)
hull_path = os.path.join(DIR, "hull", "hull.exe")
output_file = 'hout-alf'


def get_alpha_shape(points):
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
    return [(points[i], points[j]) for i, j in results_indices]


def plot_hull(ax, points, edges):
    ax.plot([point[0] for point in points], [point[1] for point in points], 'bo', picker=10)
    for edge_i, edge_j in edges:
        ax.plot([edge_i[0], edge_j[0]], [edge_i[1], edge_j[1]], 'ro-')
    ax.set_title("Area: {0}".format(polygon_area(edges)))
    vertices = edges_to_vertices(order_edges(edges))
    poly = plt.Polygon(vertices, facecolor='r', edgecolor='none', alpha=0.5)
    ax.add_patch(poly)


def pairs(items):
    return [(items[i], items[i+1]) for i in range(len(items)-1)]


def get_vertices_set(edges):
    return set(itertools.chain(*edges))


def order_edges(edges):
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


def edges_to_vertices(edges):
    vertices = []
    for v1, v2 in edges:
        vertices.append(v1)
    return vertices


def polygon_area(edges):
    a = 0.0
    for (x1, y1), (x2, y2) in edges:
        a += abs(x1 * y2 - x2 * y1)
    result = a / 2.0
    return result


def main(stream):
    points = [tuple([float(i) for i in line.rstrip().split()]) for line in stream]
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