"""
Imagine you wanted to reimplement "head" and "grep" in python.  Here's a first cut:
"""

def head(max_lines, filenames):
    for fn in filenames:
        with open(fn) as f:
            for ix, line in enumerate(f):
                if ix >= max_lines:
                    return
                print(line, end='')


def grep(needle, filenames):
    for fn in filenames:
        with open(fn) as f:
            for line in f:
                if needle in line:
                    print(line, end='')

"""
There's a lot of duplicated code there!  Now we could build a helper function like this:
"""

def getlines(filenames):
    for fn in filenames:
        with open(fn) as f:
            return f.readlines()

"""
but then head would be inefficient, because getlines always reads every single line in the file.

Find out how to use a generator to make a version of getlines that is "lazy"

More info here: http://anandology.com/python-practice-book/iterators.html
"""


import operator


def enumlines(filenames):
    for fn in filenames:
        with open(fn) as f:
            yield from enumerate(f)


def getlines(filenames):
    return map(operator.itemgetter(1), enumlines(filenames))


def head(max_lines, filenames):
    for ix, line in enumlines(filenames):
        if ix >= max_lines:
            continue
        print(line, end='')


def grep(needle, filenames):
    for line in getlines(filenames):
        if needle in line:
            print(line, end='')
