# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit

.. module:: core.message
   :platform: Unix
   :synopsis: HydraTK core commmunication messages definition
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

'''request'''
REQUEST          = 1   
'''info'''
RESPONSE         = 2 
'''info'''  
INFO             = 3
'''info'''   
SERVICE_STATUS   = 4
'''request'''   
MONITOR          = 5
'''info'''   
SERVICE_IDENT    = 6
'''info'''   
SERVICES_MAP     = 7
'''info'''   
SERVICE_SHUTDOWN = 8
'''info, new ident alternative'''   
SERVICE_HELLO    = 9
'''request'''   
PING             = 10
'''response'''  
PONG             = 11
'''msg copy for the monitor request'''  
COPY             = 12
'''info'''  
SERVICE_ALERT    = 13
'''info'''  
SERVICE_ERROR    = 99
'''info'''  
SERVICE_DROPPED  = 100
'''info''' 
SERVICE_KILLED   = 101
'''dummy 1st test message''' 
DUMMY_FIRST      = 300
'''dummy test message''' 
DUMMY            = 301
'''dummy test message''' 
DUMMY_LAST       = 302 
''' messages with number < 500 are core reserved numbers''' 

types = { 
        'FN_CALLBACK' : 1
       } 
        
            
class Message(object):
    _type = None

class FnCallBackMsg(Message):
    _type     = types['FN_CALLBACK']
    _callback = None
    _args     = None
    _kwargs   = None
    
    def __init__(self, callback, *args, **kwargs):
        """Class constructor
        
        Called when object is initialized
        
        Args:
           callback (callable): callback
           args (args): arguments
           kwargs (kwargs): key value arguments        
           
        """
                
        self.set_callback(callback)
        self.set_args(args, kwargs)
    
    def set_callback(self, callback):
        """Method sets callback
        
        Args:
           callback (callable): callback
        
        Returns:            
           void
           
        Raises:
           error: TypeError
           
        """
                
        if callable(callback):
            self._callback = callback
        else:
            raise TypeError('Callable object required')
        
    def set_args(self, *args, **kwargs):
        """Method sets arguments
        
        Args:
           args (args): arguments
           kwargs (kwargs): key value arguments
        
        Returns:            
           void
           
        """
                
        self._args   = args
        self._kwargs = kwargs
        
    def run(self):
        """Method executes callback
        
        Args:
        
        Returns:            
           obj: callback output
           
        """
                
        return self._callback(self, *self._args, **self._kwargs)