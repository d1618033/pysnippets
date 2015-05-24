import re
import inspect
from copy import deepcopy


def create_func(string):
    matches = re.findall('_\d*', string)
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    caller_locals = calframe[1][0].f_locals
    caller_globals = calframe[1][0].f_globals
    if len(matches) == 0:
        def func():
            return eval(string, caller_globals, caller_locals)
    else:
        num_args = max(map(lambda x: int(x) if x else 1, map(lambda x: x.replace('_', ''), matches)))

        def func(*args):
            if len(args) != num_args:
                raise TypeError("func() takes {0} positional arguments but {1} was given".format(num_args, len(args)))
            new_locals = caller_locals
            new_locals['_'] = args[0]
            for i, arg in enumerate(args):
                new_locals['_{0}'.format(i+1)] = arg
            return eval(string, caller_globals, new_locals)

    return func