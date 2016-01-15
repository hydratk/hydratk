# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit

.. module:: core.debugger
   :platform: Unix
   :synopsis: HydraTK core integrated debugger
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import sys, os, multiprocessing, inspect,traceback
import pprint
import time
from datetime import datetime
from hydratk.core import const, event
from xtermcolor import colorize

"""
Debug levels:
-------------
0  - off
1  - application output variables, output data content and status confirmation
2  - application logic object variables, inter-operational data content, partial construction statuses
3  - shared libraries data, lower interface statuses, drivers, database connection objects, statuses
4  - configuration loading, apply changes
5  - event states, fn_hooks, ipc triggers, signals, shared memory, queue dumps
10 - core application
11 - core core application layer init
12 - core commandline input triggers
13 - core extensions init
14 - core config, config apply
15 - core baseinit
16 - core shutdown

Default channel filters:
------------------------
debug level  - channel
10             1,2 
11             1,3 
12             1,4
13             1,5 
14             1,6 
15             1,7 
16             1,8

1              10,11 
2              10,12
3              10,13
4              10,14
5              10,15
"""

class Debugger(object):
    _debug = False
    _debug_level = 1
    #_stdio_lock = multiprocessing.Lock()
    
    def fromhere(self, trace_level = 1):
        fname = sys._getframe(trace_level).f_code.co_filename
        modname = os.path.basename(fname)
        modarg = modname.split('.')                   
        frm = inspect.stack()[trace_level]
        mod = inspect.getmodule(frm[0])
        call_path = mod.__name__ if hasattr(mod,'__name__') else '__main__'        
        return {'file': sys._getframe(trace_level).f_code.co_filename,
                'line' : sys._getframe(trace_level).f_lineno,
                'module' : modarg[0],
                'func': sys._getframe(trace_level).f_code.co_name,
                'call_path' : call_path  
                }
                
    def function(self):
        return sys._getframe(1).f_code.co_name        
    
    def file(self):        
        return sys._getframe(1).f_code.co_filename

    def line(self):        
        return sys._getframe(1).f_lineno
    
    def module(self):
        fp = sys._getframe(1).f_code.co_filename
        modname = os.path.basename(fp)
        modarg = modname.split('.')
        return modarg[0]
        
    def errmsg(self,*args):
        print(args)
    
    def dmsg(self,event_id,*args):
        if (self._debug):        
            self.fire_event(event.Event(event_id,*args))
        
            
    ''' msg, location, level, channel'''
    def dout(self, msg, location = {'file' : '', 'line' : '', 'module': '', 'func' : '', 'call_path' : ''}, level = 1, channel  = const.DEBUG_CHANNEL):                
        if (self._debug and self._debug_level >= level and channel == const.DEBUG_CHANNEL):
            thrid = '0' if multiprocessing.current_process().name == 'MainProcess' else multiprocessing.current_process().name            
            msg_format = '[{timestamp}] Debug({level}): {callpath}:{func}:{thrid}: {msg}'
            if 'msg_format' in self.cfg['System']['Debug'] and self.cfg['System']['Debug']['msg_format'] != '':
                msg_format = self.cfg['System']['Debug']['msg_format']
            
            now = datetime.now()
            now_ms = "{:.3f}".format(round(int(now.strftime("%f")).__float__() / 1000000,3))
            now_ms = now_ms.split('.')[1]                          
            msg_text = msg_format.format(
                                    timestamp=now.strftime("%d/%m/%Y %H:%M:%S.{0}".format(now_ms)),
                                    shorttime=now.strftime("%H:%M:%S.{0}".format(now_ms)),
                                    level=level,
                                    file=location['file'],
                                    line=location['line'],
                                    module=location['module'],
                                    callpath=location['call_path'],
                                    func=location['func'],
                                    thrid = thrid,
                                    msg=msg,
                                    channel = channel
                                   )
                        
            if 'term_color' in self.cfg['System']['Debug'] and self.cfg['System']['Debug']['term_color'] is not None and '#' == self.cfg['System']['Debug']['term_color'][0]:
                rgb_color = self.cfg['System']['Debug']['term_color'].replace('#','')
                msg_text = colorize(msg_text, int(rgb_color,16)) 
                
            print(msg_text)
            sys.stdout.flush()
            
    ''' msg, location'''
    def wout(self,msg,location = {'file' : '', 'line' : '', 'module': '', 'func' : '', 'call_path' : ''}):
        thrid = '0' if multiprocessing.current_process().name == 'MainProcess' else multiprocessing.current_process().name
        #self._stdio_lock.acquire()
        print("Warning: %s:%s:%s: %s " % (location['call_path'],location['func'],thrid,msg))
        sys.stdout.flush()
        #self._stdio_lock.release()
    
        
    ''' msg, location'''
    def errout(self,msg,location = {'file' : '', 'line' : '', 'module': '', 'func' : '', 'call_path' : ''}):
        thrname = '0' if multiprocessing.current_process().name == 'MainProcess' else multiprocessing.current_process().name
        #self._stdio_lock.acquire()
        print("Error: %s:%s:%s: %s " % (location['call_path'],location['func'],thrname,msg))        
        sys.stdout.flush()
        #self._stdio_lock.release()
        
    ''' msg, location'''
        
    def exout(self, exc_type, exc_msg, exc_traceback ):
        thrname = '0' if multiprocessing.current_process().name == 'MainProcess' else multiprocessing.current_process().name
        #self._stdio_lock.acquire()
        print("Unhandled exception:%s: %s:\nmsg: %s\ntraceback:" % (thrname, exc_type, exc_msg))                 
        traceback.print_tb(exc_traceback)      
        sys.stdout.flush()
        
    def _ec_parent_tell_signal(self, oevent):
        #current = multiprocessing.current_process()
        #print('somebody wants to kill me'+"\n")
        pass
    '''notify Observer about the received signal '''            
    