# coding=utf8

from __future__ import unicode_literals

"""
Challenge:  the Pythonic card deck class

The class CardDeck below represents a pack
of cards.

Find out how to use magic methods so that the
following three standard functions work:

    >>> import random
    >>> deck = CardDeck()
    >>> len(deck)
    52
    >>> print(deck[0])
    2♠
    >>> print(deck[-1])
    A♣
    >>> random.choice(deck) in list(deck)
    True
    >>> random.shuffle(deck)

Tip:
If you have lines in the docstring (this string) that look like interactive
Python sessions, you can use the doctest module to run and test this code.

Try: python3 -m doctest -v magic_methods.py

See: https://docs.python.org/3/library/doctest.html


Credit to Luciano Ramalho and his excellent book Fluent Python, from which
I stole this example.
"""

from numbers import Number
import math


class CardDeck:
    ranks = [str(n) for n in range(2, 11)] + ['J', 'Q', 'K', 'A']
    suits = '♠♡♢♣'

    def __init__(self):
        self._cards = [
            rank + suit
            for suit in self.suits
            for rank in self.ranks
        ]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, i):
        return self._cards[i]

    def __setitem__(self, i, v):
        self._cards[i] = v



"""
Bonus exercise: Polynomial class

Create a class that represents polynomials.  You may need to stretch your memory back to high school maths!

A polynomial loks like

    2(xx) - x + 7

And its essential features are the coefficients of each power of x

in this example, power-2=2, power-1=-1, power-0=7

Credit to Moshe Goldstein
"""

class Polynomial:
    """
    The constructor accepts a list of coefficients:
    >>> print(Polynomial([3, 2, 1]))
    x^2 + 2x + 3

    >>> I = Polynomial([1])
    >>> X = Polynomial([0, 1])
    >>> X2 = Polynomial([0, 0, 1])

    Addition:
    >>> print(I + X)
    x + 1
    >>> print(X + X)
    2x

    Negation:
    >>> print(-X)
    -x

    Multiplication:
    >>> print(X * X)
    x^2
    >>> print(I * I)
    1
    >>> print(X * X * X)
    x^3

    Exponentiation:
    >>> print(X ** 3)
    x^3
    >>> X ** 3 == X2 * X
    True
    >>> print((X + 1) ** 2)
    x^2 + 2x + 1

    Equality:
    >>> I + X == X + I
    True
    >>> X * X == X2
    True

    Derivatives:
    >>> print((X * X + I).derivative())
    2x

    Division:
    >>> print(*divmod(X2, X))
    x 0
    >>> print(*divmod((X + 1) * X + 1, X + 1))
    x 1
    >>> print(*divmod((X + 1) * X2, X + 1))
    x^2 0
    """

    def __init__(self, coefficients=()):
        self._coeff = list(coefficients)

    @classmethod
    def coerce(cls, value):
        if isinstance(value, cls):
            return value
        elif isinstance(value, Number):
            return cls([value])
        else:
            raise TypeError(type(value))

    @classmethod
    def monomial(cls, exponent):
        fixed = ['', 'x']
        try:
            return fixed[exponent]
        except IndexError:
            return 'x^%d' % exponent

    @classmethod
    def term(cls, exponent, coefficient):
        mon = cls.monomial(exponent)
        if coefficient == 1 and mon:
            return mon
        elif coefficient == -1 and mon:
            return '-%s' % mon
        else:
            return '%s%s' % (coefficient, mon)

    def __str__(self):
        terms = [self.term(i, c) for i, c in enumerate(self._coeff) if c]
        return " + ".join(reversed(terms)) or "0"

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self._coeff)

    @property
    def degree(self):
        return len(self._coeff)

    def __getitem__(self, i):
        if i < 0:
            raise IndexError("negative indexing not allowed")
        try:
            return self._coeff[i]
        except IndexError:
            return 0

    def __setitem__(self, i, v):
        if i < 0:
            raise IndexError("negative indexing not allowed")
        if i >= len(self._coeff):
            self._coeff.extend([0] * (i - len(self._coeff) + 1))
        self._coeff[i] = v

    def __eq__(self, poly):
        d = max(self.degree, poly.degree)
        return all(self[i] == poly[i] for i in range(d))

    def __add__(self, poly):
        '''returns the result of adding poly from self'''
        poly = self.coerce(poly)
        degree = max(self.degree, poly.degree)
        coefficients = [self[i] + poly[i] for i in range(degree)]
        while coefficients and coefficients[-1] == 0:
            coefficients.pop()
        return type(self)(coefficients)

    def __neg__(self):
        return type(self)([-c for c in self._coeff])

    def __sub__(self, poly):
        '''returns the result of subtracting poly from self'''
        return self + (-poly)

    def __mul__(self, poly):
        '''multiply two polynomials'''
        poly = self.coerce(poly)
        degree = self.degree + poly.degree - 1
        coefficients = [0 for i in range(degree)]
        for exponent in range(degree):
            for i in range(exponent + 1):
                j = exponent - i
                coefficients[exponent] += self[i] * poly[j]
        return type(self)(coefficients)

    def __pow__(self, exp):
        squares = [self]
        # squares[i] == self ** (2 ** i)
        lg = math.floor(math.log2(exp + 1))
        for _ in range(1, lg + 1):
            squares.append(squares[-1] * squares[-1])
        result = type(self)([1])
        remainder = exp
        for i in range(0, lg + 1):
            remainder, parity = divmod(remainder, 2)
            if parity == 1:
                result *= squares[i]
        return result

    def __rmul__(self, poly):
        return self * poly

    def value(self, x):
        '''returns the value of the polynomial at point x'''
        return sum(c * x ** i for i, c in enumerate(self._coeff))

    def derivative(self):
        '''returns the derivate of the polynomial'''
        return type(self)([(i + 1) * c for i, c in enumerate(self._coeff[1:])])

    def shift(self, exponent):
        return type(self)([0] * exponent + self._coeff)

    def __divmod__(self, divisor):
        quotient = type(self)()
        remainder = self

        shifts = range(self.degree - divisor.degree, -1, -1)
        for shift in shifts:
            assert quotient * divisor + remainder == self
            assert remainder.degree <= divisor.degree + shift
            q, d = divmod(remainder[divisor.degree - 1 + shift],
                          divisor[divisor.degree - 1])
            if d != 0:
                raise ArithmeticError(
                    "Leading term of divisor is not a monomial")
            quotient[shift] = q
            remainder -= q * divisor.shift(shift)
        assert quotient * divisor + remainder == self
        return quotient, remainder
