# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit

.. module:: core.logger
   :platform: Unix
   :synopsis: HydraTK core integrated logging features
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import sys

class Logger(object):
    _emulate_print = True
    
    def spout(self, data):        
        lf = "\n" if self._emulate_print == True else ""
        sys.stdout.write(data+lf)
        sys.stdout.flush()        
    