import unittest
from django_template_renderer import render_template
from datetime import datetime


class TestRenderTemplate(unittest.TestCase):
    def test_numbers(self):
        expected = '5000.6'
        actual = render_template('{{a}}', {'a': '5000.6'})
        self.assertEqual(actual, expected)

    def test_date(self):
        expected = '1/5/2015'
        actual = render_template('{{a|date:"j/n/Y"}}', {'a': datetime(day=1, month=5, year=2015)})
        self.assertEqual(actual, expected)
        
