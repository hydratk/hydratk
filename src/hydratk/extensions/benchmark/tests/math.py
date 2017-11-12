# -*- coding: utf-8 -*-
"""Benchmark tests focused on Math

.. module:: benchmark.tests.math
   :platform: Unix
   :synopsis: Benchmark tests focused on Math.
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from datetime import datetime
from time import mktime

tests = [
  'factorial',
  'fibonacci',
  'floating_point'
]

def factorial(n=10000):
    """Method tests factorial calculation

    Args:
        n (int): n!

    Returns:
        void

    """

    fact = 1
    for i in range(n, 0, -1):
        fact *= i

def fibonacci(n=10000):
    """Method tests Fibonacci number calculation

    Args:
        n (int): n-th number

    Returns:
        void

    """

    a, b = 1, 1
    for i in range(n):
        a, b = b, a + b

def floating_point(n=1000000):
    """Method tests floating point arithmetics

    Args:
        n (int): count of operations

    Returns:
        void

    """

    float_inc = 0.0000000000019346
    float_num = float(mktime(datetime.now().timetuple()))
    for i in range(n):
        float_num += float_inc
