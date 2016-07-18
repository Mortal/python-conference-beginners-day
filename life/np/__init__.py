from . import random
from builtins import sum


uint8 = None


def zeros(shape, dtype):
    if shape == ():
        return 0
    elif isinstance(shape, int):
        return zeros((shape,), dtype)
    else:
        return [zeros(shape[1:], dtype) for _ in range(shape[0])]


def array(x, dtype):
    return x
