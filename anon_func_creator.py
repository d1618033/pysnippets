import re
import inspect


def create_func(string):
    matches = re.findall('%\d+', string)
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    caller_locals = calframe[1][0].f_locals
    if len(matches) == 0:
        def func():
            return eval(string, {}, caller_locals)
    return func