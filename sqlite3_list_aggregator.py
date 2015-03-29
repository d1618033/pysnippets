"""
This module solves the following problem:

Say you have a table with two or more columns.
Just for the sake of the example, say you have two column. x and y.
Let's say your data is:
x,y
1,2
1,3
2,4
2,5
1,6
Say you want to get a list of ys for each value of x, e.g:
x,list
1,[2,3,6]
2,[4,5]
This would not normally be possible in sqlite3 for two reasons:
1. Lists are not valid types.
2. There's no function in sqlite3 that aggregates a group into a list.

So, first of all add the list type to sqlite3:
>>> import sqlite3
>>> register_list_adapter_and_converter()

Next, we want to register the function ListAggregator to our database:

>>> con = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
>>> con.create_aggregate("list_aggregator", 1, ListAggregator)

Now, lets set up a demo table:
>>> con.execute("CREATE TABLE test (x INTEGER, y INTEGER)") # doctest: +ELLIPSIS
<...>
>>> data = [
...     {"x": 1, "y": 2},
...     {"x": 1, "y": 3},
...     {"x": 2, "y": 4},
...     {"x": 2, "y": 5},
...     {"x": 1, "y": 6},
... ]
>>> con.executemany("INSERT INTO test (x, y) VALUES (:x, :y)", data) # doctest: +ELLIPSIS
<...>
>>> [(x, convert_list(ly)) for x, ly in con.execute("SELECT x, list_aggregator(y) FROM test GROUP BY x").fetchall()]
[(1, [2, 3, 6]), (2, [4, 5])]
"""
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


if __name__ == "__main__":
    import doctest
    doctest.testmod()
