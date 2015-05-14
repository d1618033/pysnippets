import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class BasePlot:
    def __init__(self, ax):
        self.ax = ax
        self.current_index = None
        self.points_to_indices = {}
        self.indices_to_points = []

    def plot(self):
        self.points_to_indices = {}
        self.indices_to_points = []
        for index in range(self.num_points()):
            point = self.plot_index(index)
            self.points_to_indices[point] = index
            self.indices_to_points.append(point)

    def plot_index(self, index):
        raise NotImplementedError

    def dehighlight_point(self, point):
        raise NotImplementedError

    def highlight_point(self, point):
        raise NotImplementedError

    def highlight_index(self, index):
        if self.current_index is not None:
            self.dehighlight_point(self.indices_to_points[self.current_index])
        self.current_index = index
        self.highlight_point(self.indices_to_points[self.current_index])

    def get_index(self, point):
        return self.points_to_indices[point]

    def get_axes(self):
        return self.ax

    def num_points(self):
        raise NotImplementedError


class PointPlot(BasePlot):
    def __init__(self, point_data, ax):
        self.point_data = point_data
        BasePlot.__init__(self, ax)

    def plot_index(self, index):
        return self.ax.plot([self.point_data[index, 0]],
                            [self.point_data[index, 1]],
                            [self.point_data[index, 2]], 'bo', picker=20)[0]

    def highlight_point(self, point):
        point.set_color('r')

    def dehighlight_point(self, point):
        point.set_color('b')

    def num_points(self):
        return self.point_data.shape[0]


class LinePlot(BasePlot):
    def __init__(self, t, line_data, ax):
        self.line_data = line_data
        self.t = t
        BasePlot.__init__(self, ax)

    def plot_index(self, index):
        return self.ax.plot(self.t, self.line_data[index, :], 'b-', picker=10)[0]

    def highlight_point(self, point):
        point.set_color('r')

    def dehighlight_point(self, point):
        point.set_color('b')

    def num_points(self):
        return self.line_data.shape[0]


class LinkedPlotsManager:
    def __init__(self, fig, plot_objs):
        self.axes_to_plot_objs = {plot_obj.get_axes(): plot_obj for plot_obj in plot_objs}
        self.fig = fig
        fig.canvas.mpl_connect('pick_event', self.onevent)

    def onevent(self, event):
        artist = event.artist
        ax = artist.get_axes()
        index = self.axes_to_plot_objs[ax].get_index(artist)
        self.highlight_index(index)
        self.fig.canvas.draw()

    def plot(self):
        for plot_obj in self.axes_to_plot_objs.values():
            plot_obj.plot()

    def highlight_index(self, index):
        for plot_obj in self.axes_to_plot_objs.values():
            plot_obj.highlight_index(index)


def demo():
    import numpy as np
    point_data = np.array([[i, i*2, i+5] for i in range(10)])
    t = np.arange(5)
    line_data = point_data[:, 0].reshape(-1, 1) + point_data[:, 1].reshape(-1, 1) * t.reshape(1, -1)

    fig = plt.figure()
    ax1 = plt.subplot(1, 2, 1, projection='3d')
    ax2 = plt.subplot(1, 2, 2)
    point_plot = PointPlot(point_data, ax1)
    line_plot = LinePlot(t, line_data, ax2)
    linked_plots = LinkedPlotsManager(fig, [point_plot, line_plot])
    linked_plots.plot()
    plt.show()


if __name__ == "__main__":
    demo()