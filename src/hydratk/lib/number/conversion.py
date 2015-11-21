# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit library

.. module:: lib.number.conversion
   :platform: Unix
   :synopsis: Module for number conversions
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

def int2bool(intvar):
    result = False
    intvar = int(intvar)    
    if intvar > 0:
        result = True
    return result    