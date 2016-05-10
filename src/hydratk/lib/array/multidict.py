# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit library

.. module:: lib.array.multidict
   :platform: Unix
   :synopsis: Multi-level dictionary
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

from collections import defaultdict

class MultiDict(defaultdict):
    
    def __init__(self):
        """Class constructor
        
        Called when object is initialized
        
        Args:            
                
        """  
                
        defaultdict.__init__(self, MultiDict)
        
    def __repr__(self):
        """Method overrides __repr__
        
        Args:            
           
        Returns:
           str
                
        """  
                
        return dict.__repr__(self)