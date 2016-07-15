# -*- coding: utf-8 -*-
"""Function callback management 

.. module:: lib.dynamic.callback
   :platform: Unix
   :synopsis: Function callback management 
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
import sys
try:
    import cPickle as pickle
except ImportError:
    import pickle  

class CallBackProcessor(object):
    """Class CallBackProcessor
    """
    
    _cbm           = None #CallBackManager instance
    _cb_dict       = {}
    _cb_dproxy     = None
    _current_cb    = None

    def __init__(self, cbm, cb_dict, cb_dproxy):
        self._cbm         = cbm
        self._cb_dict     = cb_dict
        self._cb_dproxy   = cb_dproxy       
    
    def _wrap_fn(self, *args, **kwargs):
        if self._current_cb is not None:
            cbh = self._cbm.async_handler if self._current_cb.async == True else self._cbm.sync_handler
                
            if cbh is not None:
                self._current_cb.args   = args
                self._current_cb.kwargs = kwargs
                result = cbh.cb_run(self._current_cb)
            else:
                if self._current_cb.async == True:
                    raise Exception("Asynchrounous callback handler not set, callback will be not processed")
                else:
                    raise Exception("Synchrounous callback handler not set, callback will be not processed")                
          
            self._current_cb = None
            return result
        else:
            raise Exception("There's nothing to process")
        
    def _wrap_fn_dproxy(self, *args, **kwargs):
        if self._current_cb is not None:
            ah = self._cbm.async_handler
            if ah is not None:
                self._current_cb.args   = args
                self._current_cb.kwargs = kwargs
                ah.cb_run(self._current_cb)
            else:
                raise Exception("Asynchrounous callback handler not set, callback will be not processed")
        self._current_cb = None
        
    def __getattr__(self, fn_id):             
        if fn_id in self._cb_dict:
            self._current_cb = self._cb_dict[fn_id]
            return self._wrap_fn
        
        if type(self._cb_dproxy).__name__ == 'DictProxy' and fn_id in self._cb_dproxy:
            self._current_cb = self._cb_dproxy[fn_id]
            return self._wrap_fn
        
        raise NameError("{0} is not defined".format(fn_id))

class CallBackTree(object):
    pass
        
class CallBack(object):
    """Class CallBack
    """
    
    _shared = False
    _async  = False
    _fn_id  = None
    _fn     = None
    _obj    = None    
    _args   = []
    _kwargs = {}  
    
    def __init__(self, fn_id, callback, options = None):
        if fn_id is None or fn_id == '':
            raise TypeError("fn_id: expected nonempty string")
        self._fn_id = fn_id
        
        if type(callback).__name__ == 'tuple':
            obj, fn_name = callback
            self.set_obj(obj)
            self.set_fn(fn_name)
        elif type(callback).__name__ in ('str', 'function'):
            self.set_fn(callback)            
        else:
            raise TypeError("callback: expected types: tuple,str,function, got {0}".format(type(callback).__name__))
    
          
    @property
    def args(self):
        return self._args
    
    @args.setter
    def args(self, nargs):
        self._args = nargs
    
    @property
    def kwargs(self):
        return self._kwargs

    @kwargs.setter
    def kwargs(self, nkwargs):
        self._kwargs = nkwargs
        
    @property
    def fn_id(self):
        return self._fn_id

    @property
    def fn(self):
        return self._fn

    @property
    def obj(self):
        return self._obj    
                  
    @property
    def shared(self):
        return self._shared
    
    @shared.setter
    def shared(self, state):
        if state in (True, False):
            self._shared = state
        else:
            raise TypeError("shared state: expected boolean")
            
    @property
    def async(self):
        return self._async
    
    @async.setter
    def async(self, state):        
        if state in (True, False):            
            self._async = state            
        else:
            raise TypeError("async state: expected boolean")
                
    def set_fn(self, fn_name):
        if type(fn_name).__name__ not in ('str','function'):
            raise TypeError("fn_name: str expected")
        self._fn = fn_name if type(fn_name).__name__ == 'str' else pickle.dumps(fn_name)
        
    def set_obj(self, obj):
        if type(obj).__name__ != 'instance':
            raise TypeError("obj: class instance expected")
        self._obj = pickle.dumps(obj)

class CallBackManager(object):
    """Class CallBackManager
    """
    
    _cb_dict       = {}
    _cb_dproxy     = None
    _cbm_proc      = None
    _async_handler = None
    _sync_handler  = None
    
    def __init__(self, cb_dict = None, cb_dproxy = None):
        if cb_dict is not None:
            self.set_cb_dict(cb_dict)
            
        if cb_dproxy is not None:
            self.set_cb_dproxy(cb_dproxy)
            
        self._sync_handler = SyncCallBackHandler()    
        self._cbm_proc     = CallBackProcessor(self, self._cb_dict, self._cb_dproxy)
    
    @property
    def sync_handler(self):
        return self._sync_handler
    
    def set_sync_handler(self, sh_obj):
        self._sync_handler = sh_obj
        
    @property
    def async_handler(self):
        return self._async_handler
    
    def set_async_handler(self, ah_obj):
        self._async_handler = ah_obj
    
    def set_cb_dict(self, cb_dict):
        if type(cb_dict).__name__ != 'dict':
            raise TypeError("cb_dict: dict expected")
        self._cb_dict    = cb_dict
        
    def set_cb_dproxy(self, cb_dproxy):
        if type(cb_dproxy).__name__ == 'DictProxy':
            self._cb_dproxy = cb_dproxy
        else:
            raise TypeError("cb_dproxy: DictProxy object expected")
    
    def create_cb_dproxy(self):
        from multiprocessing import Manager
        self._cb_dproxy = Manager().dict()
        
    @property
    def ns(self):
        return self._cbm_ns  
       
    @property
    def run(self):
        return self._cbm_proc
    
    def get_cb(self, fn_id):
        if type(fn_id).__name__ == 'str' and fn_id != '':
            if fn_id in self._cb_dict:
                return self._cb_dict[fn_id]           
            
            if fn_id in self._cb_dproxy:
                return self._cb_dproxy[fn_id]            
            
            raise KeyError("Undefined callback id: {0}".format(fn_id))
        else:
            raise TypeError("fn_id: expected nonempty string")    
        
    def reg_cb(self, fn_id, callback, options = None):
        if fn_id is None or fn_id == '':
            raise TypeError("fn_id: expected nonempty string")
        rcb = CallBack(fn_id, callback)
        shared = False
        async  = False
        
        if type(options).__name__ == 'dict':
            if 'shared' in options:
                if options['shared'] in (True, False):
                    shared = options['shared']
                else: 
                    raise ValueError("options['shared'] expected boolean, got {0}". format(type(options['shared']).__name__))
            if 'async' in options:
                if options['async'] in (True, False):
                    async = options['async']
                else: 
                    raise ValueError("options['async'] expected boolean, got {0}". format(type(options['async']).__name__))
        rcb.shared = shared
        rcb.async  = async
        if shared == False:    
            self._cb_dict[fn_id] = rcb           
        else:                     
            self._cb_dproxy[fn_id] = rcb             
    def add_cb(self):
        pass

    def update_cb(self, cb_obj):
        fn_id = cb_obj.fn_id
        if cb_obj.shared == True:            
            self._cb_dproxy[fn_id] = cb_obj
            if fn_id in self._cb_dict:
                del self._cb_dict[fn_id]
        else:
            self._cb_dict[fn_id] = cb_obj
            if fn_id in self._cb_dproxy:
                del self._cb_dproxy[fn_id]
        
class SyncCallBackHandler(object):
    def cb_run(self, cb_obj):
        print("sync: running request {0}".format(cb_obj.fn_id), cb_obj.args, cb_obj.kwargs)
        if type(cb_obj.fn).__name__ == 'function':
            return cb_obj.fn(*cb_obj.args, **cb_obj.kwargs)
    
    def cb_completed(self, req_id):
        pass
             
class AsyncCallBackHandler(object):
     
    def cb_run(self, cb_obj):
        print("async: running request {0}".format(cb_obj.fn_id), cb_obj.args, cb_obj.kwargs)
    
    def cb_completed(self, req_id):
        pass
    
    
        