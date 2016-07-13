# -*- coding: utf-8 -*-
"""HydraTK default event class

.. module:: core.event
   :platform: Unix
   :synopsis: HydraTK default event class
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import pprint

class Event(object):
    """ Class Event
    """
    
    _id                 = None
    _args               = ()
    _data               = {}
    _propagate          = True
    _run_default        = True
    _skip_before_hook   = False
    _skip_after_hook    = False


    def __init__(self, event_id, *args, **kwargs):
        """Class constructor
        
        Called when the object is initialized

        Args:
           event_id (str): event
           args (args): arguments
           kwargs (kwargs): key value arguments
           
        Raises:
           error: ValueError   
           
        """
                
        self._args               = ()
        self._data               = {}
        self._propagate          = True
        self._run_default        = True
        self._skip_before_hook   = False
        self._skip_after_hook    = False
        if isinstance(event_id, str) and event_id != '':
            self._id = event_id
            self._data['target_event'] = None
            self._data['source_event'] = None
        else: raise ValueError("Invalid event id specified, nonempty string is required")
                            
        if isinstance(args, tuple):
            self._args = ()
        self._args = args        
        if len(kwargs) > 0:
            for k,v in kwargs.items():
                self._data[k] = v                         
        
    def id(self):
        """Method gets id attribute

        Args:
           none
           
        Returns:
           str 
           
        """  
        
        return self._id
    
    def argc(self):
        """Method gets count of arguments

        Args:
           none
           
        Returns:
           int: count of arguments
           
        """
                
        return len(self._args)
         
    def args(self):
        """Method gets args attribute

        Args:
           none
           
        Returns:
           tuple 
           
        """  
        
        return self._args
    
    def get_all_data(self):
        """Method gets event data

        Args:
           none
           
        Returns:
           dict: data
           
        """
                
        return self._data
    
    def get_data(self, key):
        """Method gets requested event data

        Args:
           key (str): data key
           
        Returns:
           obj: data value
           
        """
        
        return self._data[key] if (key in self._data) else None
    
    def set_data(self, key, value):
        """Method sets requested event data

        Args:
           key (str): data key
           value (obj): data value
           
        Returns:
           void
           
        Raises:
           error: ValueError
           
        """
                
        if isinstance(key, str) and key != '':
            self._data[key] = value
        else: raise ValueError("Invalid key specified, nonempty string is required")
        
    def argv(self, num): 
        """Method gets request event argument

        Args:
           num (int): argument index
           
        Returns:
           obj: argument value
           
        """
                       
        return self._args[num] if (num < len(self._args)) else None        
    
    def set_argv(self, num, val=None):
        """Method sets requested event argument

        Args:
           num (int): argument index
           val (obj): argument value
           
        Returns:
           void
           
        """
                
        if isinstance(num, int) and num < len(self._args):
            args = list(self._args)
            args[num] = val
            self._args = tuple(args)
    
    def stop_propagation(self):
        """Method stops event propagation

        Args:
           none
           
        Returns:
           void
           
        """
                
        self._propagate = False
    
    @property
    def skip_before_hook(self):
        """ skip_before_hook property getter """
        
        return self._skip_before_hook
    
    @property
    def skip_after_hook(self):
        """ skip_after_hook property getter """
        
        return self._skip_after_hook
    
    def prevent_default(self):
        """Method prevents default event processing

        Args:
           none
           
        Returns:
           void
           
        """
                
        self._run_default = False
    
    def run_default(self):
        """Method enables default event processing

        Args:
           none
           
        Returns:
           void
           
        """
                
        self._run_default = True
    
    
    def will_run_default(self):
        """Method gets default event processing

        Args:
           none
           
        Returns:
           bool: run_default
           
        """        
        
        return self._run_default
           
    def propagate(self):
        """Method gets propagate attribute

        Args:
           none
           
        Returns:
           bool 
           
        """  
        
        return self._propagate