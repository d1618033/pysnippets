#!/usr/bin/python3

import os
from subprocess import Popen, PIPE, STDOUT
import io
import itertools

import numpy as np
import matplotlib.pyplot as plt


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
    edges = [(points[i], points[j]) for i, j in results_indices]
    return  edges_to_vertices(order_edges(edges))


def plot_hull(ax, points, vertices):
    for data, color in [(points, 'b'), (vertices, 'r')]:
        ax.plot(*zip(*data), color=color, marker='o', linestyle='')
    ax.set_title("Area: {0}".format(polygon_area(vertices)))
    poly = plt.Polygon(vertices, linewidth=2, facecolor='r', edgecolor='r', linestyle='solid', alpha=0.5)
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


def polygon_area(vertices):
    n = len(vertices) # of corners
    a = 0.0
    for i in range(n):
        j = (i + 1) % n
        a += abs(vertices[i][0] * vertices[j][1]-vertices[j][0] * vertices[i][1])
    result = a / 2.0
    return result


def read_points(stream):
    points = [tuple([float(i) for i in line.rstrip().split()]) for line in stream]
    return points

def main(stream):
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
