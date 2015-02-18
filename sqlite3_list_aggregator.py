import sqlite3
import pickle


class ListAggregator:
    def __init__(self):
        self._list = []

    def step(self, value):
        self._list.append(value)

    def finalize(self):
        return adapt_list(self._list)


def adapt_list(list_):
    return pickle.dumps(list_)


def convert_list(bytes_):
    return pickle.loads(bytes_)


def register_list_adapter_and_converter():
    sqlite3.register_adapter(list, adapt_list)
    sqlite3.register_converter("list", convert_list)

