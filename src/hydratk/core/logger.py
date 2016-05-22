# -*- coding: utf-8 -*-
"""HydraTK core integrated logging features

.. module:: core.logger
   :platform: Unix
   :synopsis: HydraTK core integrated logging features
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import sys

class Logger(object):
    """Class Logger
    """
    
    _emulate_print = True
    
    def spout(self, data):   
        """Method prints data
        
        Args:     
           data (str): data
           
        Returns:
                
        """  
                     
        lf = "\n" if self._emulate_print == True else ""
        sys.stdout.write(data+lf)
        sys.stdout.flush()        
    