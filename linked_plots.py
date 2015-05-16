import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from abc import abstractmethod, ABCMeta


class BaseLinkablePlot(metaclass=ABCMeta):
    @abstractmethod
    def plot(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_index(self, artist: plt.Artist) -> int:
        raise NotImplementedError

    @abstractmethod
    def on_index_change(self, index: int) -> None:
        raise NotImplementedError


class BaseHighlightPlot(BaseLinkablePlot, metaclass=ABCMeta):
    def __init__(self, ax: plt.Axes) -> None:
        self.ax = ax
        self.current_index = None
        self.points_to_indices = {}
        self.indices_to_points = []

    def plot(self) -> None:
        self.points_to_indices = {}
        self.indices_to_points = []
        for index in self.indices_to_plot():
            point = self.plot_index(index)
            self.points_to_indices[point] = index
            self.indices_to_points.append(point)

    @abstractmethod
    def plot_index(self, index: int) -> plt.Artist:
        raise NotImplementedError

    @abstractmethod
    def dehighlight_point(self, point: plt.Artist) -> None:
        raise NotImplementedError

    @abstractmethod
    def highlight_point(self, point: plt.Artist) -> None:
        raise NotImplementedError

    def on_index_change(self, index: int) -> None:
        if self.current_index is not None:
            self.dehighlight_point(self.indices_to_points[self.current_index])
        self.current_index = index
        self.highlight_point(self.indices_to_points[self.current_index])

    def get_index(self, point: plt.Artist) -> int:
        return self.points_to_indices[point]

    @property
    def axes(self) -> plt.Axes:
        return self.ax

    @abstractmethod
    def indices_to_plot(self) -> "Iterable[int]":
        raise NotImplementedError


class PointHighlightPlot(BaseHighlightPlot):
    def __init__(self, point_data: "numpy.ndarray", ax: plt.Axes) -> None:
        BaseHighlightPlot.__init__(self, ax)
        self.point_data = point_data

    def plot_index(self, index: int) -> None:
        return self.ax.plot([self.point_data[index, 0]],
                            [self.point_data[index, 1]],
                            [self.point_data[index, 2]], 'bo', picker=20)[0]

    def highlight_point(self, point: plt.Artist) -> None:
        point.set_color('r')

    def dehighlight_point(self, point: plt.Artist) -> None:
        point.set_color('b')

    def indices_to_plot(self) -> int:
        return range(self.point_data.shape[0])


class LineHighlightPlot(BaseHighlightPlot):
    def __init__(self, t: "numpy.ndarray", line_data: "numpy.ndarray", ax: plt.Axes):
        BaseHighlightPlot.__init__(self, ax)
        self.line_data = line_data
        self.t = t

    def plot_index(self, index: int) -> plt.Artist:
        return self.ax.plot(self.t, self.line_data[index, :], 'b-', picker=10)[0]

    def highlight_point(self, point: plt.Artist) -> None:
        point.set_color('r')

    def dehighlight_point(self, point: plt.Artist) -> None:
        point.set_color('b')

    def indices_to_plot(self) -> "Iterable[int]":
        return range(self.line_data.shape[0])


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
            plot_obj.plot()

    def on_index_change(self, index: int) -> None:
        for ax, plot_obj in self.axes_to_plot_objs.items():
            plot_obj.on_index_change(index)
            ax.figure.canvas.draw()


def demo():
    import numpy as np
    point_data = np.array([[i, i*2, i+5] for i in range(10)])
    t = np.arange(5)
    line_data = point_data[:, 0].reshape(-1, 1) + point_data[:, 1].reshape(-1, 1) * t.reshape(1, -1)

    _, ax1 = plt.subplots(subplot_kw=dict(projection='3d'))
    _, ax2 = plt.subplots()
    point_plot = PointHighlightPlot(point_data, ax1)
    line_plot = LineHighlightPlot(t, line_data, ax2)
    linked_plots = LinkedPlotsManager([point_plot, line_plot])
    linked_plots.plot()
    plt.show()


if __name__ == "__main__":
    demo()