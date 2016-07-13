# -*- coding: utf-8 -*-
"""Module for time unit operations

.. module:: lib.system.mtime
   :platform: Unix
   :synopsis: Module for time unit operations
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import time
import math

def microtime(get_as_float=False) :
    """Methods returns current time including microseconds

    Args:
       get_as_float (bool): return time as float

    Returns:
       float: if get_as_flost
       str: if not get_as_float
    
    """
        
    if get_as_float:
        return time.time()
    else:
        micro = math.modf(time.time())
        return '%d %f' % (micro[1], micro[0])
