# -*- coding: utf-8 -*-
"""Benchmark tests focused on memory allocation

.. module:: benchmark.tests.memory
   :platform: Unix
   :synopsis: Benchmark tests focused on memory allocation.
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

tests = [
    'allocate_single',
    'allocate_mult'
]

def allocate_single(size=1024 ** 3):
    """Method allocates memory for single variable

    Args:
        size (int): size

    Returns:
        void

    """

    data = '0' * size
    del data

def allocate_mult(n=1000, size=1024 ** 2):
    """Method allocates memory for multiple variables

    Args:
        n (int): count of variables
        size (int): size

    Returns:
        void

    """

    data = []
    for i in range(n):
        data.append('0' * size)

    del data
