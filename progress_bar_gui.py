"""
A simple example of a tkinter app with a progress bar
"""

import tkinter
from tkinter import ttk
import time
import multiprocessing


def example_command(progress_func):
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


class NonBlockingTkinterCommand:
    def __init__(self, root, command, before, after, on_new_element_in_queue, poll_time=10):
        self.root = root
        self.command = command
        self.before = before
        self.after = after
        self.on_new_element_in_queue = on_new_element_in_queue
        self.poll_time = poll_time

    def run(self):
        self.before()
        queue = multiprocessing.Queue()
        process = multiprocessing.Process(target=self.command, args=(queue.put,))
        process.start()
        self.poll(queue, process)

    def poll(self, queue, process):
        if not process.is_alive():
            self.after()
        else:
            while not queue.empty():
                elem = queue.get()
                self.on_new_element_in_queue(elem)
            self.root.after(self.poll_time, self.poll, queue, process)


class App(ttk.Frame):
    def __init__(self, master, root):
        ttk.Frame.__init__(self, master=master)
        self.root = root
        self.add_widgets()

    def add_widgets(self):
        self.cmd = NonBlockingTkinterCommand(
            root=self.root,
            command=example_command,
            before=lambda: self.button.disable(),
            after=lambda: self.button.enable(),
            on_new_element_in_queue=lambda value: self.progress_bar.set(value),
        )
        self.button = Button(
            self,
            text="Execute",
            command=self.cmd.run
        )
        self.button.pack()
        self.progress_bar = Progressbar(self)
        self.progress_bar.pack()


def _example():
    root = tkinter.Tk()
    App(master=root, root=root).pack()
    root.mainloop()


if __name__ == "__main__":
    _example()