# -*- coding: utf-8 -*-
"""Benchmark tests focused on disk operations

.. module:: benchmark.tests.disk
   :platform: Unix
   :synopsis: Benchmark tests focused on disk operations.
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from os import remove, makedirs, path, system
from shutil import rmtree

tests = [
    'file_single',
    'file_mult',
    'dir_mult',
    'dir_tree'
]

def file_single(size=10 * 1024 ** 2):
    """Method creates single file

    Args:
        size (int): size

    Returns:
        void

    """

    fname = 'test.txt'
    f = open(fname, 'w')
    f.write('0' * size)

    f.close()
    remove(fname)

def file_mult(n=1000, size=1024):
    """Method creates multiple files

    Args:
        n (int): count of files
        size (int): size

    Returns:
        void

    """

    fname = 'test{0}.txt'
    for i in range(n):
        f = open(fname.format(i), 'w')
        f.write('0' * size)
        f.close()

    for i in range(n):
        remove(fname.format(i))

def dir_mult(n=1000):
    """Method creates multiple directories

    Args:
        n (int): count of directories

    Returns:
        void

    """

    dname = 'test{0}'
    for i in range(n):
        makedirs(dname.format(i))

    for i in range(n):
        rmtree(dname.format(i))

def dir_tree(n=500):
    """Method creates directory tree

    Args:
        n (int): tree level

    Returns:
        void

    """

    dname = 'test{0}'
    dpath = dname.format('0')
    for i in range(n):
        makedirs(dpath)
        dpath = path.join(dpath, dname.format(i + 1))

    system('rm -fR {0}'.format(dname.format('0')))
