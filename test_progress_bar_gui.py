import unittest
from unittest import mock
import progress_bar_gui


class TestDispatcher(unittest.TestCase):
    def test_called(self):
        f1 = mock.MagicMock()
        f2 = mock.MagicMock()
        dispatcher = progress_bar_gui.Dispatcher({
            'f1': f1,
            'f2': f2,
        })
        dispatcher({'f1': 10, 'f2': 3})
        f1.assert_called_once_with(10)
        f2.assert_called_once_with(3)

    def test_not_called(self):
        f1 = mock.MagicMock()
        f2 = mock.MagicMock()
        dispatcher = progress_bar_gui.Dispatcher({
            'f1': f1,
            'f2': f2,
        })
        dispatcher({'f1': 10})
        f1.assert_called_once_with(10)
        f2.assert_has_calls([])