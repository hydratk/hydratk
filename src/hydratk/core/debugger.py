# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: debugger
   :platform: Unix
   :synopsis: Hydra core integrated debugger.
.. moduleauthor:: Petr Czaderna <pc@headz.cz>

"""
import sys, os, multiprocessing, inspect,traceback;
import pprint;
from hydratk.core import const, event;
'''TODO remove const '''

class Debugger:
    _debug = False;
    _debug_level = 1;
    #_stdio_lock = multiprocessing.Lock();
    
    def fromhere(self):
        fname = sys._getframe(1).f_code.co_filename;
        modname = os.path.basename(fname);
        modarg = modname.split('.')                   
        frm = inspect.stack()[1];
        mod = inspect.getmodule(frm[0]);
        call_path = mod.__name__ if hasattr(mod,'__name__') else '__main__';        
        return {'file': sys._getframe(1).f_code.co_filename,
                'line' : sys._getframe(1).f_lineno,
                'module' : modarg[0],
                'func': sys._getframe(1).f_code.co_name,
                'call_path' : call_path  
                };
                
    def function(self):
        return sys._getframe(1).f_code.co_name;        
    
    def file(self):        
        return sys._getframe(1).f_code.co_filename;

    def line(self):        
        return sys._getframe(1).f_lineno;
    
    def module(self):
        fp = sys._getframe(1).f_code.co_filename;
        modname = os.path.basename(fp);
        modarg = modname.split('.')
        return modarg[0];
        
    def errmsg(self,*args):
        print(args);
    
    def dmsg(self,event_id,*args):        
        self.fire_event(event.Event(event_id,*args));
        
            
    ''' msg, location, level, channel'''
    def dout(self, msg, location = {'file' : '', 'line' : '', 'module': '', 'func' : '', 'call_path' : ''}, level = 1, channel  = const.DEBUG_CHANNEL):        
        
        if (self._debug and self._debug_level >= level and channel == const.DEBUG_CHANNEL):
            thrname = '0' if multiprocessing.current_process().name == 'MainProcess' else multiprocessing.current_process().name;
            #self._stdio_lock.acquire();
            print("Debug(%d): %s:%s:%s: %s " % (level,location['call_path'],location['func'],thrname,msg));
            sys.stdout.flush();
            #self._stdio_lock.release();
            
    ''' msg, location'''
    def wout(self,msg,location = {'file' : '', 'line' : '', 'module': '', 'func' : '', 'call_path' : ''}):
        thrname = '0' if multiprocessing.current_process().name == 'MainProcess' else multiprocessing.current_process().name;
        #self._stdio_lock.acquire();
        print("Warning: %s:%s:%s: %s " % (location['call_path'],location['func'],thrname,msg));
        sys.stdout.flush();
        #self._stdio_lock.release();
    
        
    ''' msg, location'''
    def errout(self,msg,location = {'file' : '', 'line' : '', 'module': '', 'func' : '', 'call_path' : ''}):
        thrname = '0' if multiprocessing.current_process().name == 'MainProcess' else multiprocessing.current_process().name;
        #self._stdio_lock.acquire();
        print("Error: %s:%s:%s: %s " % (location['call_path'],location['func'],thrname,msg));        
        sys.stdout.flush();
        #self._stdio_lock.release();
        
    ''' msg, location'''
        
    def exout(self, exc_type, exc_msg, exc_traceback ):
        thrname = '0' if multiprocessing.current_process().name == 'MainProcess' else multiprocessing.current_process().name;
        #self._stdio_lock.acquire();
        print("Unhandled exception:%s: %s:\nmsg: %s\ntraceback:" % (thrname, exc_type, exc_msg));                 
        traceback.print_tb(exc_traceback);      
        sys.stdout.flush();
        
    def _ec_parent_tell_signal(self, oevent):
        #current = multiprocessing.current_process();
        #print('somebody wants to kill me'+"\n");
        pass
    '''notify Observer about the received signal '''            
    