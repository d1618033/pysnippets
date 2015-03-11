python_pow = pow


def slow_iter_pow(x, n):
    res = 1
    for _ in range(n):
        res *= x
    return res


def fast_iter_pow(x, n):
    """
    we can write:
    n = a0*1 + a1*2 + a2*4 + ...
    (n's binary form)
    so:
    x^n = x^(a0*1 + a1*2 + a2*4 + ...)
    = (x^1)^(a0) * (x^2)^(a1) * (x^4)^(a2) * ...
    now, notice that
    n % 2 is equal to a0
    and n // 2 = a1 + a2 * 2 + ... (i.e the same form, with one less digit)
    """
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


def fast_recursive_pow(x, n):
    if n:
        if n % 2:
            return fast_recursive_pow(x, n - 1) * x
        else:
            return fast_recursive_pow(x * x, n / 2)
    else:
        return 1