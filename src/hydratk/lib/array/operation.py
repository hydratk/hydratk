# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit library

.. module:: lib.array.operation
   :platform: Unix
   :synopsis: Module for collection operations
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

def subdict(o_dict, subset):
    
    return dict((key, value) for key, value in o_dict.items() if key in subset); 
