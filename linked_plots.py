import matplotlib.pyplot as plt
import numpy as np


def distance(p1, p2):
    return ((p1 - p2) ** 2).sum()


def closest_point_to_point(points, point):
    return np.argmin(((points - point) ** 2).sum(axis=1))


def min_by(on, by):
    return on[min(range(len(by)), key=by.__getitem__)]


def closest_line_to_point(t, lines, point):
    distances = []
    indices = []
    for index, line in enumerate(lines):
        for ti, linei in zip(t, line):
            distances.append(distance(point, np.array([ti, linei])))
            indices.append(index)
    return min_by(indices, distances)


class PointPlot:
    def __init__(self, point_data, ax):
        self.point_data = point_data
        self.ax = ax
        self.current_index = None
        self.matplotlib_points = None

    def plot(self):
        self.matplotlib_points = [self.ax.plot(self.point_data[index, 0], self.point_data[index, 1], 'bo')[0] for index in range(len(self.point_data))]

    def plot_index(self, index):
        assert self.matplotlib_points is not None
        assert 0 <= index <= len(self.matplotlib_points), "Index ({0}) out of bounds ({1})".format(index, len(self.matplotlib_points))
        if self.current_index is not None:
            self.matplotlib_points[self.current_index].set_color('b')
        self.current_index = index
        self.matplotlib_points[self.current_index].set_color('r')

    def get_index(self, point):
        return closest_point_to_point(self.point_data, point)

    def get_axes(self):
        return self.ax


class LinePlot:
    def __init__(self, t, line_data, ax):
        self.line_data = line_data
        self.t = t
        self.ax = ax
        self.current_index = None
        self.matplotlib_lines = None

    def plot(self):
        self.matplotlib_lines = [self.ax.plot(self.t, self.line_data[index, :], 'b-')[0] for index in range(len(self.line_data))]

    def plot_index(self, index):
        assert self.matplotlib_lines is not None
        assert 0 <= index <= len(self.matplotlib_lines), "Index ({0}) out of bounds ({1})".format(index, len(self.matplotlib_lines))
        if self.current_index is not None:
            self.matplotlib_lines[self.current_index].set_color('b')
        self.current_index = index
        self.matplotlib_lines[self.current_index].set_color('r')

    def get_index(self, point):
        return closest_line_to_point(self.t, self.line_data, point)

    def get_axes(self):
        return self.ax


class LinkedPlotsManager:
    def __init__(self, fig, plot_objs):
        self.axes_to_plot_objs = {plot_obj.get_axes(): plot_obj for plot_obj in plot_objs}
        self.fig = fig

    def onevent(self, event):
        if event.inaxes is not None:
            point = np.array([event.xdata, event.ydata])
            index = self.axes_to_plot_objs[event.inaxes].get_index(point)
            self.plot_index(index)
            self.fig.canvas.draw()

    def plot(self):
        for plot_obj in self.axes_to_plot_objs.values():
            plot_obj.plot()

    def plot_index(self, index):
        for plot_obj in self.axes_to_plot_objs.values():
            plot_obj.plot_index(index)


def demo():
    point_data = np.random.randn(10, 2)
    t = np.arange(5)
    line_data = point_data[:, 0].reshape(-1, 1) + point_data[:, 1].reshape(-1, 1) * t.reshape(1, -1)


    fig, (ax1, ax2) = plt.subplots(ncols=2)
    point_plot = PointPlot(point_data, ax1)
    line_plot = LinePlot(t, line_data, ax2)
    linked_plots = LinkedPlotsManager(fig, [point_plot, line_plot])
    fig.canvas.mpl_connect('motion_notify_event', linked_plots.onevent)
    linked_plots.plot()
    plt.show()


if __name__ == "__main__":
    demo()