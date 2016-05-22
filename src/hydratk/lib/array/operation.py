# -*- coding: utf-8 -*-
"""Module for collection operations

.. module:: lib.array.operation
   :platform: Unix
   :synopsis: Module for collection operations
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

def subdict(o_dict, subset):
    """Method gets sub dictionary
        
    Args:
        o_dict (dict): original dictionary
        subset (list): requested subset key 
        
    Returns:
        dict: sub dictionary
                
    """     
    
    return dict((key, value) for key, value in o_dict.items() if key in subset); 
