import tkinter
from tkinter import ttk
import time
import multiprocessing


def command(progress_func):
    for i in range(100):
        progress_func(i+1)
        time.sleep(0.01)


class App(ttk.Frame):
    def __init__(self, master, root):
        ttk.Frame.__init__(self, master=master)
        self.add_widgets()
        self.root = root

    def add_widgets(self):
        self.button = ttk.Button(
            self,
            text="Execute",
            command=self.on_click
        )
        self.button.pack()
        self.progress_bar_value = tkinter.IntVar(value=0)
        self.progress_bar = ttk.Progressbar(self, variable=self.progress_bar_value)
        self.progress_bar.pack()

    def disable_button(self):
        self.button.config(state=tkinter.DISABLED)

    def enable_button(self):
        self.button.config(state=tkinter.NORMAL)

    def on_click(self):
        self.disable_button()
        queue = multiprocessing.Queue()
        process = multiprocessing.Process(target=command, args=(queue.put,))
        process.start()
        self.poll_progress(queue, process)

    def poll_progress(self, queue, process):
        if not process.is_alive():
            self.enable_button()
        else:
            while not queue.empty():
                p = queue.get()
                self.progress_bar_value.set(p)
            root.after(10, self.poll_progress, queue, process)


if __name__ == "__main__":
    root = tkinter.Tk()
    App(master=root, root=root).pack()
    root.mainloop()