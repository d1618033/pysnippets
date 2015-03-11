python_pow = pow


def slow_iter_pow(x, n):
    res = 1
    for _ in range(n):
        res *= x
    return res


def fast_iter_pow(x, n):
    res = 1
    element = x
    while n > 0:
        n, m = divmod(n, 2)
        if m:
            res *= element
        element *= element
    return res


def slow_recursive_pow(x, n):
    if n:
        return x * slow_recursive_pow(x, n-1)
    else:
        return 1