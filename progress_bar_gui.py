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
    for i in range(1000):
        progress_func((i+1)/10)
        time.sleep(0.001)


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
    def __init__(self, master, command, before, after, on_new_element_in_queue, poll_time=10):
        """
        :param master: The container of this command (e.g a frame object or a root object)
        :param command: The command to run. The command must take a single argument
                        which will be a function to use to add to the queue.
        :param before: A function with no arguments that will be executed before running the command.
        :param after: A function with no arguments that will be executed after running the command.
        :param on_new_element_in_queue: A function with one argument, that will be given the value
                                        that was added in the queue.
        :param poll_time: The time to wait between checks of the queue.
        """
        self.master = master
        self.command = command
        self.before = before
        self.after = after
        self.on_new_element_in_queue = on_new_element_in_queue
        self.poll_time = poll_time

    def run(self):
        """
        Run the command
        """
        self.before()
        queue = multiprocessing.Queue()
        process = multiprocessing.Process(target=self.command, args=(queue.put,))
        process.start()
        self._poll(queue, process)

    def _poll(self, queue, process):
        if not process.is_alive():
            self.after()
        else:
            while not queue.empty():
                elem = queue.get()
                self.on_new_element_in_queue(elem)
            self.master.after(self.poll_time, self._poll, queue, process)


class App(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master=master)
        self.add_widgets()

    def add_widgets(self):
        self.cmd = NonBlockingTkinterCommand(
            self,
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
    frame = tkinter.Frame(root)
    frame.pack()
    App(master=frame).pack()
    root.mainloop()


if __name__ == "__main__":
    _example()