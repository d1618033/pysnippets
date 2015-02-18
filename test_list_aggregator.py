import unittest
import sqlite3_list_aggregator
import sqlite3


def setup_db():
    sqlite3_list_aggregator.register_list_adapter_and_converter()
    con = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
    return con


class TestListAdapter(unittest.TestCase):
    def test_adapt_convert(self):
        x = [1, 5, 7.9, "a"]
        actual = sqlite3_list_aggregator.convert_list(sqlite3_list_aggregator.adapt_list(x))
        expected = x
        self.assertEqual(actual, expected)

    def test_register(self):
        con = setup_db()
        con.execute("create table temp(x list)")
        x = [1, 2, "a"]
        con.execute("insert into temp (x) values (:x)", {"x": x})
        actual = con.execute("select x from temp").fetchone()[0]
        expected = x
        self.assertEqual(actual, expected)


class TestListAggregator(unittest.TestCase):
    def setUp(self):
        self.con = setup_db()
        self.con.create_aggregate("list_aggregator", 1, sqlite3_list_aggregator.ListAggregator)
        self.con.execute("create table test (x integer, y integer)")

    def _get_result(self):
        results = self.con.execute("select list_aggregator(x) from test group by y order by y").fetchall()
        return [sqlite3_list_aggregator.convert_list(result[0]) for result in results]

    def insert_data(self, data):
        query = "insert into test (x, y) values (:x, :y)"
        if isinstance(data, list):
            self.con.executemany(query, data)
        else:
            self.con.execute(query, data)

    def test_groupby_one_group_one_row(self):
        self.insert_data([{'x': 1, 'y': 10}])
        actual = self._get_result()
        expected = [[1]]
        self.assertEqual(actual, expected)

    def test_groupby_one_group_two_rows(self):
        self.insert_data([{"x": 1, "y": 10}, {"x": 2, "y": 10}])
        actual = self._get_result()
        expected = [[1, 2]]
        self.assertEqual(actual, expected)

    def test_groupby_two_groups_one_row(self):
        self.insert_data([{"x": 1, "y": 10}, {"x": 2, "y": 11}])
        actual = self._get_result()
        expected = [[1], [2]]
        self.assertEqual(actual, expected)

    def test_groupby_two_groups_two_rows_each(self):
        self.insert_data([
            {"x": 1, "y": 10},
            {"x": 2, "y": 10},
            {"x": 3, "y": 11},
            {"x": 4, "y": 11},
        ])
        actual = self._get_result()
        expected = [[1, 2], [3, 4]]
        self.assertEqual(actual, expected)
