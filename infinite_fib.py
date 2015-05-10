def itertive_infinite_fib():
    a, b = 0, 1
    yield a
    yield b
    while True:
        a, b = b, a + b
        yield b


def recursive_infinite_fib():
    yield 0
    yield 1
    prevs = recursive_infinite_fib()
    afters = recursive_infinite_fib()
    next(afters)
    for prev, after in zip(prevs, afters):
        yield prev + after

