# -*- coding: utf-8 -*-
"""Benchmark tests focused on network operations

.. module:: benchmark.tests.network
   :platform: Unix
   :synopsis: Benchmark tests focused on network operations.
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from socket import socket, error

tests = [
    'request_single',
    'request_mult'
]

def request_single(size=1024 ** 2):
    """Method sends single TCP request

    Args:
        size (int): size

    Returns:
        void

    """

    c = socket()
    try:
        c.connect(('127.0.0.1', 22))
        c.sendall(('0' * size).encode('utf-8'))
    except error:
        pass
    finally:
        c.close()

def request_mult(n=100, size=1024):
    """Method sends multiple TCP requests

    Args:
        n (int): count of requests
        size (int): size

    Returns:
        void

    """

    for i in range(n):
        c = socket()
        try:
            c.connect(('127.0.0.1', 22))
            c.sendall(('0' * size).encode('utf-8'))
        except error:
            pass
        finally:
            c.close()
