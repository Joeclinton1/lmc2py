"""
Checker function takes a list of integers as input and outputs a list of integers
"""


def checker(inputs):
    n = inputs[0]
    f = 1
    factors = []
    if n in [0, 1]:
        return [n]
    while f * f <= n:
        if n % f == 0:
            factors.append(f)
            n_div_f = n // f
            if n_div_f != f:
                factors.append(n_div_f)
        f += 1

    return sorted(factors)
