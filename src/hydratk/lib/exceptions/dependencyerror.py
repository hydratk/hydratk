# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit library

.. module:: lib.exceptions.dependencyerror
   :platform: Unix
   :synopsis: Class for dependency error exception
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

class DependencyError(Exception):
    '''
    classdocs
    '''

    def __init__(self, error_num, args, msg):
        """Class constructor
        
        Called when object is initialized
        
        Args:   
           error_num (int): number
           args (list): arguments
           msg (str): message
                
        """ 
        
        self.error_num = error_num
        self.args      = args        
        self.message   = msg