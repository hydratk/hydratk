# -*- coding: utf-8 -*-
"""Useful module for solving Python 2 and 3 compatibility problems

.. module:: lib.compat.utils
   :platform: Unix
   :synopsis: Useful module for solving Python 2 and 3 compatibility problems
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import sys

PYTHON_MAJOR_VERSION = sys.version_info[0]

if PYTHON_MAJOR_VERSION == 2:
    range = xrange 
    
if PYTHON_MAJOR_VERSION == 3:    
    range = range
    