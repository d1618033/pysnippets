import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from abc import abstractmethod, ABCMeta, abstractproperty
from tkinter import TclError
import warnings


class Data(metaclass=ABCMeta):
    @abstractmethod
    def plot_index(self, ax):
        raise NotImplementedError

    @abstractproperty
    def indices(self):
        raise NotImplementedError


class PointData(Data):
    def __init__(self, point_data):
        self.point_data = point_data

    def plot_index(self, ax, index):
        return ax.plot(*[(p,) for p in self.point_data[index, :]], color='b', marker='o', picker=20)[0]

    @property
    def indices(self):
        return list(range(self.point_data.shape[0]))


class LineData(Data):
    def __init__(self, t, line_data):
        self.t = t
        self.line_data = line_data

    def plot_index(self, ax, index):
        return ax.plot(self.t, self.line_data[index, :], 'b-', picker=10)[0]

    @property
    def indices(self):
        return list(range(self.line_data.shape[0]))


class BaseLinkablePlot(metaclass=ABCMeta):
    """
    A plot object that can be linked to other plots.
    Every artist in the plot (e.g line, point, etc...) should have a unique index tied to it.
    This unique index is exactly what ties this plot to the other plots.
    """
    @abstractmethod
    def initialize_plot(self) -> None:
        """
        This is the method that's called when the plot is first shown.
        """
        raise NotImplementedError

    @abstractmethod
    def get_index(self, artist: plt.Artist) -> int:
        """
        This method is given an artist object that has been clicked
        and returns the unique index of ths object.
        """
        raise NotImplementedError

    @abstractmethod
    def on_index_change(self, index: int) -> None:
        """
        A callback function when an index changes in a different plot (or this plot)
        """
        raise NotImplementedError

    @abstractproperty
    def axes(self) -> plt.Axes:
        """
        Returns the axes of this plot
        """
        raise NotImplementedError


class BasePartialPlot(BaseLinkablePlot):
    def __init__(self, ax, other_indices_func):
        self.ax = ax
        self.other_indices_func = other_indices_func
        self.points_to_indices = {}
        self.indices_to_points = []

    def get_index(self, artist: plt.Artist):
        return self.points_to_indices[artist]

    def on_index_change(self, index: int):
        self.ax.clear()
        self.indices_to_points = {}
        self.points_to_indices = {}
        self.indices_to_points[index] = self.plot_index(index)
        for other_index in self.other_indices_func(index):
            point = self.plot_index(other_index)
            self.indices_to_points[other_index] = point
            self.points_to_indices[point] = other_index

    @abstractmethod
    def plot_index(self, index):
        raise NotImplementedError


class HighlightPlot(BaseLinkablePlot):
    """
    A linkable plot that highlights the artist when selected
    """
    def __init__(self, ax: plt.Axes, data: Data) -> None:
        self.ax = ax
        self.data = data
        # Keep track of the current selected index
        # so that when an index changes we can dehighlight the previous index
        self.current_index = None
        self.points_to_indices = {}
        self.indices_to_points = []

    def initialize_plot(self) -> None:
        self.points_to_indices = {}
        self.indices_to_points = []
        for index in self.data.indices:
            point = self.data.plot_index(self.ax, index)
            self.points_to_indices[point] = index
            self.indices_to_points.append(point)

    def dehighlight_artist(self, artist: plt.Artist) -> None:
        artist.set_color('b')

    def highlight_artist(self, artist: plt.Artist) -> None:
        artist.set_color('r')

    def on_index_change(self, index: int) -> None:
        if self.current_index is not None:
            self.dehighlight_artist(self.indices_to_points[self.current_index])
        self.current_index = index
        self.highlight_artist(self.indices_to_points[self.current_index])

    def get_index(self, artist: plt.Artist) -> int:
        return self.points_to_indices[artist]

    @property
    def axes(self) -> plt.Axes:
        return self.ax


class LinkedPlotsManager:
    def __init__(self, plot_objs: "Iterable[BaseLinkablePlot]") -> None:
        self.axes_to_plot_objs = {
            plot_obj.axes: plot_obj for plot_obj in plot_objs
        }  # type: Dict[plt.Axes, BasePlot]
        figs = set([axes.figure for axes in self.axes_to_plot_objs.keys()])
        for fig in figs:
            fig.canvas.mpl_connect('pick_event', self.onevent)

    def onevent(self, event) -> None:
        artist = event.artist
        ax = artist.axes
        index = self.axes_to_plot_objs[ax].get_index(artist)
        self.on_index_change(index)

    def plot(self) -> None:
        for plot_obj in self.axes_to_plot_objs.values():
            plot_obj.initialize_plot()

    def on_index_change(self, index: int) -> None:
        for ax, plot_obj in self.axes_to_plot_objs.items():
            plot_obj.on_index_change(index)
            try:
                ax.figure.canvas.draw()
            except TclError:
                warnings.warn("Figure of plot_obj {0} is closed".format(plot_obj))


def demo():
    import numpy as np
    point_data = np.array([[i, i*2, i+5] for i in range(10)])
    t = np.arange(5)
    line_data = point_data[:, 0].reshape(-1, 1) + point_data[:, 1].reshape(-1, 1) * t.reshape(1, -1)

    _, ax1 = plt.subplots(subplot_kw=dict(projection='3d'))
    _, ax2 = plt.subplots()
    point_plot = HighlightPlot(ax1, PointData(point_data))
    line_plot = HighlightPlot(ax2, LineData(t, line_data))
    linked_plots = LinkedPlotsManager([point_plot, line_plot])
    linked_plots.plot()
    plt.show()


if __name__ == "__main__":
    demo()