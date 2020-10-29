def checker(inputs):
    n = inputs[0]
    f = 1
    factors = []
    if n in [0,1]:
        return [n]
    while 1:
        if n % f == 0:
            factors.append(f)
            ndivf = n // f
            if ndivf != f:
                factors.append(ndivf)
        f += 1
        if f * f > n:
            break
    return sorted(factors)