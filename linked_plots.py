import matplotlib.pyplot as plt


class PointPlot:
    def __init__(self, point_data, ax):
        self.point_data = point_data
        self.ax = ax
        self.current_index = None
        self.points_to_indices = {}
        self.indices_to_points = []

    def plot(self):
        self.points_to_indices = {}
        self.indices_to_points = []
        for index in range(len(self.point_data)):
            point = self.ax.plot(self.point_data[index, 0], self.point_data[index, 1], 'bo', picker=5)[0]
            self.points_to_indices[point] = index
            self.indices_to_points.append(point)

    def plot_index(self, index):
        if self.current_index is not None:
            self.indices_to_points[self.current_index].set_color('b')
        self.current_index = index
        self.indices_to_points[self.current_index].set_color('r')

    def get_index(self, point):
        return self.points_to_indices[point]

    def get_axes(self):
        return self.ax


class LinePlot:
    def __init__(self, t, line_data, ax):
        self.line_data = line_data
        self.t = t
        self.ax = ax
        self.current_index = None
        self.points_to_indices = {}
        self.indices_to_points = []

    def plot(self):
        self.points_to_indices = {}
        self.indices_to_points = []
        for index in range(len(self.line_data)):
            point = self.ax.plot(self.t, self.line_data[index, :], 'b-', picker=5)[0]
            self.points_to_indices[point] = index
            self.indices_to_points.append(point)

    def plot_index(self, index):
        if self.current_index is not None:
            self.indices_to_points[self.current_index].set_color('b')
        self.current_index = index
        self.indices_to_points[self.current_index].set_color('r')

    def get_index(self, point):
        return self.points_to_indices[point]

    def get_axes(self):
        return self.ax


class LinkedPlotsManager:
    def __init__(self, fig, plot_objs):
        self.axes_to_plot_objs = {plot_obj.get_axes(): plot_obj for plot_obj in plot_objs}
        self.fig = fig

    def onevent(self, event):
        artist = event.artist
        ax = artist.get_axes()
        index = self.axes_to_plot_objs[ax].get_index(artist)
        self.plot_index(index)
        self.fig.canvas.draw()

    def plot(self):
        for plot_obj in self.axes_to_plot_objs.values():
            plot_obj.plot()

    def plot_index(self, index):
        for plot_obj in self.axes_to_plot_objs.values():
            plot_obj.plot_index(index)


def demo():
    import numpy as np
    point_data = np.array([[i, i] for i in range(10)])
    t = np.arange(5)
    line_data = point_data[:, 0].reshape(-1, 1) + point_data[:, 1].reshape(-1, 1) * t.reshape(1, -1)

    fig, (ax1, ax2) = plt.subplots(ncols=2)
    point_plot = PointPlot(point_data, ax1)
    line_plot = LinePlot(t, line_data, ax2)
    linked_plots = LinkedPlotsManager(fig, [point_plot, line_plot])
    fig.canvas.mpl_connect('pick_event', linked_plots.onevent)
    linked_plots.plot()
    plt.show()


if __name__ == "__main__":
    demo()