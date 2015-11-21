# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit library

.. module:: lib.system.time
   :platform: Unix
   :synopsis: Module for time unit operations
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import time
import math

def microtime(get_as_float = False) :
    if get_as_float:
        return time.time()
    else:
        return '%f %d' % math.modf(time.time())
