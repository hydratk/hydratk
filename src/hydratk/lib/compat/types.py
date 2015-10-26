"""This code is a part of Pyx application framework

.. module:: types
   :platform: Unix
   :synopsis: A useful module for solving Python 2 and 3 compatibility problems
.. moduleauthor:: Petr Czaderna <pc@headz.cz>

"""
import sys

PYTHON_MAJOR_VERSION = sys.version_info[0]

if PYTHON_MAJOR_VERSION == 2:
    str = str
    unicode = unicode
    bytes = str
    basestring = basestring    
    
if PYTHON_MAJOR_VERSION == 3:    
    str = str
    unicode = str
    bytes = bytes
    basestring = (str,bytes)   