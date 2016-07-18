import random


def randint(a, b, shape, dtype):
    n, m = shape
    return [[random.randint(a, b-1) for j in range(m)] for i in range(n)]
