import re
import inspect


def create_func(string):
    matches = re.findall('_\d*', string)
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    caller_locals = calframe[1][0].f_locals
    if len(matches) == 0:
        def func():
            return eval(string, {}, caller_locals)
    else:
        num_args = max(map(lambda x: int(x) if x else 1, map(lambda x: x.replace('_', ''), matches)))

        def func(*args):
            if len(args) != num_args:
                raise TypeError("func() takes {0} positional arguments but {1} was given".format(num_args, len(args)))

    return func