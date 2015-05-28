#!/usr/bin/python3

import os
from subprocess import Popen, PIPE, STDOUT
import io
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
    return [(points[i], points[j]) for i, j in results_indices]


def plot_hull(ax, points, edges):
    ax.plot([point[0] for point in points], [point[1] for point in points], 'bo')
    for edge_i, edge_j in edges:
        ax.plot([edge_i[0], edge_j[0]], [edge_i[1], edge_j[1]], 'ro-')


def pairs(items):
    return [(items[i], items[i+1]) for i in range(len(items)-1)]


def edges_to_vertices(edges):
    vertices = []
    for v1, v2 in edges:
        vertices.append(v1)
    vertices.append(edges[-1][-1])
    return vertices


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