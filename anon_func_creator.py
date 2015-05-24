import re


def create_func(string):
    matches = re.findall('%\d+', string)
    if len(matches) == 0:
        def func():
            return eval(string)
    return func