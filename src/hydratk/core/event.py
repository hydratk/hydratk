"""This code is a part of Hydra Toolkit

.. module:: hydratk.core.event
   :platform: Unix
   :synopsis: Default event class.
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
import pprint

class Event(object):
    _id                 = None
    _args               = ()
    _data               = {}
    _propagate          = True
    _run_default        = True
    _skip_before_hook   = False
    _skip_after_hook    = False


    def __init__(self, event_id, *args, **kwargs):
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
        return self._id
    
    def argc(self):
        return len(self._args)
            
    def args(self):
        return self._args
    
    def get_all_data(self):
        return self._data
    
    def get_data(self, key):
        return self._data[key]
    
    def set_data(self, key, value):
        if isinstance(key, str) and key != '':
            self._data[key] = value
        else: raise ValueError("Invalid key specified, nonempty string is required")
        
    def argv(self,num):        
        return self._args[num]        
    
    def set_argv(self,num, val = None):
        if isinstance(num, int):
            self._args[num] = val
    
    def stop_propagation(self):
        self._propagate = False
    
    @property
    def skip_before_hook(self):
        return self._skip_before_hook
    
    @property
    def skip_after_hook(self):
        return self._skip_after_hook
    
    def prevent_default(self):
        self._run_default = False
    
    def run_default(self):
        self._run_default = True
    
    def will_run_default(self):
        return self._run_default
                
    def propagate(self):
        return self._propagate