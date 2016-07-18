import time
import curses
import functools


try:
    import numpy as np
except ImportError:
    import np


try:
    from numba import jit, njit
    # raise ImportError()
except ImportError:
    def jit(f):
        return f
    njit = jit


@njit
def step(scene, counts):
    """
    >>> scene = np.array([[1, 1, 1], [0, 0, 0], [0, 0, 0]], dtype=np.uint8)
    >>> step(scene, np.zeros(3, dtype=np.uint8))
    >>> print(scene)
    [[1 1 1]
     [0 1 0]
     [0 0 0]]
    >>> scene = np.array([
    ...     [0, 0, 0, 0, 0, 0],
    ...     [0, 0, 1, 0, 0, 0],
    ...     [0, 0, 0, 1, 0, 0],
    ...     [0, 1, 1, 1, 0, 0],
    ...     [0, 0, 0, 0, 0, 0],
    ...     [0, 0, 0, 0, 0, 0],
    ... ], dtype=np.uint8)
    >>> np.sum(scene) == 5
    True
    >>> step(scene, np.zeros(6, dtype=np.uint8))
    >>> np.sum(scene) == 5
    True
    >>> step(scene, np.zeros(6, dtype=np.uint8))
    >>> np.sum(scene) == 5
    True
    >>> step(scene, np.zeros(6, dtype=np.uint8))
    >>> np.sum(scene) == 5
    True
    >>> step(scene, np.zeros(6, dtype=np.uint8))
    >>> np.sum(scene) == 5
    True
    """
    counts = 2 * scene[0]
    for i in range(1, len(scene)-1):
        # Count neighbors for scene[i] and use counts to update scene[i-1]
        a = scene[i-1][0] + scene[i][0] + scene[i+1][0]
        b = scene[i-1][1] + scene[i][1] + scene[i+1][1]
        for j in range(1, len(scene[0])-1):
            c = scene[i-1][j+1] + scene[i][j+1] + scene[i+1][j+1]
            if i > 1:
                if counts[j] >= 3 and counts[j] - scene[i-1][j] <= 3:
                    scene[i-1][j] = 1
                else:
                    scene[i-1][j] = 0
            counts[j] = a + b + c
            a = b
            b = c
    for j in range(1, len(scene[0])-1):
        if counts[j] >= 3 and counts[j] - scene[-2][j] <= 3:
            scene[-2][j] = 1
        else:
            scene[-2][j] = 0


def curses_wrapper(func):
    @functools.wraps(func)
    def f(*args, **kwargs):
        stdscr = curses.initscr()
        try:
            curses.noecho()
            curses.cbreak()
            stdscr.keypad(1)
            return func(stdscr, *args, **kwargs)
        finally:
            stdscr.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()

    return f


@curses_wrapper
def loop(stdscr, times):
    n, m = stdscr.getmaxyx()

    scene = np.random.randint(0, 2, (n-1, m-1), np.uint8)
    try:
        scene[0, :] = 0
        scene[-1, :] = 0
        scene[:, 0] = 0
        scene[:, -1] = 0
    except TypeError:
        for i in range(n-1):
            scene[i][0] = 0
            scene[i][-1] = 0
        for j in range(m-1):
            scene[0][j] = 0
            scene[-1][j] = 0

    # scene = np.zeros((n-1, m-1), np.uint8)
    # glider = [[2, 1], [3, 2], [1, 3], [2, 3], [3, 3]]
    # scene[tuple(np.transpose(glider) + 4)] = 1

    n = len(scene) * len(scene[0])

    @jit
    def draw():
        for i in range(len(scene)):
            stdscr.move(i, 0)
            for j in range(len(scene[0])):
                if scene[i][j]:
                    stdscr.addch('@')
                else:
                    stdscr.addch('.')
        stdscr.refresh()

    @jit
    def step_draw(scene, counts, n):
        for i in range(n):
            draw()
            step(scene, counts)

    counts = np.zeros(len(scene[0]), dtype=np.uint8)
    t1 = time.time()
    while True:
        step_draw(scene, counts, 20)
        t2 = time.time()
        times.append(t2 - t1)
        t1 = t2


if __name__ == "__main__":
    times = []
    try:
        loop(times)
    except KeyboardInterrupt:
        pass
    finally:
        print(times)
