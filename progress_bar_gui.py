"""
A simple example of a tkinter app with a progress bar
"""

import tkinter
from tkinter import ttk
import time
import multiprocessing


def command(progress_func):
    """
    :param progress_func: a function that updates the progress bar
     it expects to get as input a number between 0 and 100
    """
    for i in range(100):
        progress_func(i+1)
        time.sleep(0.01)


class Progressbar(ttk.Progressbar):
    def __init__(self, *args, **kwargs):
        self.progress_bar_value = tkinter.IntVar(value=0)
        kwargs['variable'] = self.progress_bar_value
        ttk.Progressbar.__init__(self, *args, **kwargs)

    def set(self, value):
        self.progress_bar_value.set(value)

    def get(self):
        return self.progress_bar_value.get()


class Button(ttk.Button):
    def disable(self):
        self.config(state=tkinter.DISABLED)

    def enable(self):
        self.config(state=tkinter.NORMAL)


class App(ttk.Frame):
    def __init__(self, master, root):
        ttk.Frame.__init__(self, master=master)
        self.add_widgets()
        self.root = root

    def add_widgets(self):
        self.button = Button(
            self,
            text="Execute",
            command=self.on_click
        )
        self.button.pack()
        self.progress_bar = Progressbar(self)
        self.progress_bar.pack()

    def on_click(self):
        self.button.disable()
        queue = multiprocessing.Queue()
        process = multiprocessing.Process(target=command, args=(queue.put,))
        process.start()
        self.poll_progress(queue, process)

    def poll_progress(self, queue, process):
        if not process.is_alive():
            self.button.enable()
        else:
            while not queue.empty():
                p = queue.get()
                self.progress_bar.set(p)
            self.root.after(10, self.poll_progress, queue, process)


def _example():
    root = tkinter.Tk()
    App(master=root, root=root).pack()
    root.mainloop()


if __name__ == "__main__":
    _example()