# -*- coding: utf-8 -*-
"""Multi-level dictionary

.. module:: lib.array.multidict
   :platform: Unix
   :synopsis: Multi-level dictionary
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

from collections import defaultdict

class MultiDict(defaultdict):
    """Class MultiDict
    
    Inherited from defaultdict
    """
    
    def __init__(self):
        """Class constructor
        
        Called when object is initialized
        
        Args: 
           none           
                
        """  
                
        defaultdict.__init__(self, MultiDict)
        
    def __repr__(self):
        """Method overrides __repr__
        
        Args:  
           none          
           
        Returns:
           str
                
        """  
                
        return dict.__repr__(self)