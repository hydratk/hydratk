# -*- coding: utf-8 -*-
"""Module for number conversions

.. module:: lib.number.conversion
   :platform: Unix
   :synopsis: Module for number conversions
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

def int2bool(intvar):
    """Method converts number to bool
        
    Args:   
       intvar (int): number

    Returns: 
       bool: result
                
    """ 
            
    result = False
    intvar = int(intvar)    
    if intvar > 0:
        result = True
    return result    