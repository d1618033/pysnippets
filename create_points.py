import matplotlib.pyplot as plt


class PointCollector:
    def __init__(self, ax, output_stream):
        self.output_stream = output_stream
        self.ax = ax

    def _set_limits(self):
        self.ax.set_xlim([0, 1])
        self.ax.set_ylim([0, 1])
        
    def on_click(self, event):
        x, y = event.xdata, event.ydata
        self.output_stream.write("{0} {1}\n".format(x, y))
        self.ax.plot(x, y, 'bo')
        self._set_limits()
        self.ax.figure.canvas.draw()     


def main(output_file):
    fig, ax = plt.subplots()
    with open(output_file, 'w') as f:
        pc = PointCollector(ax, f)
        fig.canvas.mpl_connect('button_press_event', pc.on_click)
        plt.show()
    

if __name__ == "__main__":
    main('points')
