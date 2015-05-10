from operator import add
import itertools


def itertive_infinite_fib():
    a, b = 0, 1
    yield a
    yield b
    while True:
        a, b = b, a + b
        yield b


def tail(gen):
    next(gen)
    return gen


def zip_with(func, elems1, elems2):
    for elem1, elem2 in zip(elems1, elems2):
        yield func(elem1, elem2)


def recursive_infinite_fib():
    yield 0
    yield 1
    f1, f2 = itertools.tee(recursive_infinite_fib(), 2)
    yield from zip_with(add, f1, tail(f2))
