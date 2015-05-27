#!/usr/bin/python3

import sys, os
from subprocess import Popen, PIPE, STDOUT
import io


DIR = os.path.dirname(__file__)
hull_path = os.path.join(DIR, "hull", "hull.exe")
output_file = os.path.join(DIR, 'hout-alf')


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


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    points = [tuple([float(i) for i in line.rstrip().split()]) for line in sys.stdin]
    fig, ax = plt.subplots()
    ax.plot([point[0] for point in points], [point[1] for point in points], 'bo')
    for point_i, point_j in get_alpha_shape(points):
        ax.plot([point_i[0], point_j[0]], [point_i[1], point_j[1]], 'ro-')
    plt.show()
