# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit library

.. module:: lib.data.gen
   :platform: Unix
   :synopsis: Module for random data generation
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from time import time, strftime
from random import randint

def gen_systimestamp():
    """Method generates system timestamp
        
    Args:
        
    Returns:
        str: timestamp in format YYYY-MM-DDTHH24:MI:SS    
                
    """    
    
    return strftime('%Y-%m-%dT%H:%M:%S')

def gen_sysdate():
    """Method generates system data
        
    Args:
        
    Returns:
        str: date in format YYYY-MM-DD   
                
    """       
    
    return strftime('%Y-%m-%d')

def gen_message_id():
    """Method generates random message id
        
    Args:
        
    Returns:
        str: message id in format hydratk-time-random 3-digit number  
                
    """       
    
    return 'hydratk-{0}-{1}'.format(time(), gen_id(3))

def gen_id(n=10):
    """Method generates random number
        
    Args:
        n (int): number of digits
        
    Returns:
        str: random n-digit number
        
    Raises:
        error: ValueError
                
    """  
    
    if (n > 0):     
        return str(randint(10**(n-1), 10**n-1))
    else:
        raise ValueError('n must be positive integer')