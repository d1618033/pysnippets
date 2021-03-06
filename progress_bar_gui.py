"""
A simple example of a tkinter app with a progress bar
"""

import tkinter
from tkinter import ttk
import time
import multiprocessing
import datetime


def example_command(progress):
    """
    :param progress: progress function
    """
    progress(dict(max=50))
    for i in range(50):
        progress(dict(progress=i+1, log="[{0}] got to: {1}".format(datetime.datetime.now(), i)))
        time.sleep(0.05)


class Dispatcher:
    """
    Creates a callable object that runs functions on kw values.
    e.g:
    create some test functions:
    >>> called = {}
    >>> def f1(x): called['f1'] = x
    >>> def f2(x): called['f2'] = x

    create the dispatcher object:
    >>> d = Dispatcher(f1=f1, f2=f2)

    call it:
    >>> d(f1=5, f2=7)
    >>> called['f1']
    5
    >>> called['f2']
    7
    """
    def __init__(self, **name_to_func_dict):
        self.name_to_func_dict = name_to_func_dict

    def __call__(self, **dictionary):
        for key, value in dictionary.items():
            if key in self.name_to_func_dict:
                self.name_to_func_dict[key](value)


class Progressbar(ttk.Progressbar):
    def __init__(self, *args, **kwargs):
        self.progress_bar_value = tkinter.IntVar(value=0)
        kwargs['variable'] = self.progress_bar_value
        ttk.Progressbar.__init__(self, *args, **kwargs)

    def set_max(self, value):
        self.config(maximum=value)

    def set(self, value):
        self.progress_bar_value.set(value)

    def get(self):
        return self.progress_bar_value.get()


class Text(tkinter.Text):
    def append(self, text):
        self.insert(tkinter.END, text+'\n')
        self.move_to_end()

    def clear(self):
        self.delete(1.0, tkinter.END)

    def move_to_end(self):
        self.yview(tkinter.END)


class TextWithScrollbars(ttk.Frame):
    def __init__(self, master, text_options={}):
        ttk.Frame.__init__(self, master)
        self.text_options = text_options
        self.add_widgets()

    def add_widgets(self):
        scrollbar = ttk.Scrollbar(self)
        text = Text(self, **self.text_options)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        text.pack(side=tkinter.LEFT, fill=tkinter.Y)
        scrollbar.config(command=text.yview)
        text.config(yscrollcommand=scrollbar.set)
        self.text = text

    def append(self, text):
        self.text.append(text)

    def clear(self):
        self.text.clear()


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

    def __call__(self):
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
        def before():
            self.button.disable()
            self.log.clear()

        self.button = Button(
            self,
            text="Execute",
        )
        self.button.pack()
        self.progress_bar = Progressbar(self, length=375)
        self.progress_bar.pack()
        self.log = TextWithScrollbars(self, text_options={'width': 50})
        self.log.pack()
        dispatcher = Dispatcher(
            max=self.progress_bar.set_max,
            progress=self.progress_bar.set,
            log=self.log.append,
        )
        self.cmd = NonBlockingTkinterCommand(
            self,
            command=example_command,
            before=before,
            after=lambda: self.button.enable(),
            on_new_element_in_queue=lambda elem: dispatcher(**elem),
        )
        self.button.config(command=self.cmd)


def _example():
    root = tkinter.Tk()
    frame = tkinter.Frame(root)
    frame.pack()
    App(master=frame).pack()
    root.mainloop()


if __name__ == "__main__":
    _example()