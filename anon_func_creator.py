import re
import inspect


def create_func(string):
    """
    Creates an 'annonymous' function
    Input:
        string - A string to eval. Use _1, _2, etc... for variables names.
    Output:
        A function. The number of arguments of the function depends on the variables you used in the string.
    Example:
        >>> f = create_func('_1 + _2*_3')
        >>> f(7, 5, 2)
        17
    """
    matches = re.findall('_\d*', string)
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    caller_locals = calframe[1][0].f_locals
    caller_globals = calframe[1][0].f_globals
    compiled_string = compile(string, '', 'eval')
    if len(matches) == 0:
        def func():
            return eval(compiled_string, caller_globals, caller_locals)
    else:
        num_args = max(map(lambda x: int(x) if x else 1, map(lambda x: x.replace('_', ''), matches)))

        def func(*args):
            if len(args) != num_args:
                raise TypeError("func() takes {0} positional arguments but {1} was given".format(num_args, len(args)))
            new_locals = caller_locals
            new_locals['_'] = args[0]
            for i, arg in enumerate(args):
                new_locals['_{0}'.format(i+1)] = arg
            return eval(compiled_string, caller_globals, new_locals)

    class Func:
        def __str__(self):
            return string

        def __repr__(self):
            return string

        def __call__(self, *args):
            return func(*args)

    return Func()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
