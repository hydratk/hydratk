"""This code is a part of Pyx application framework

.. module:: firelogger
   :platform: Unix
   :synopsis: An implementation of firelogger protocol
.. moduleauthor:: Petr Czaderna <pc@headz.cz>

"""

import time
import math

def microtime(get_as_float = False) :
    if get_as_float:
        return time.time()
    else:
        return '%f %d' % math.modf(time.time())
