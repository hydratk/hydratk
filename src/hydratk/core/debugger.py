# -*- coding: utf-8 -*-
"""HydraTK core integrated debugger

.. module:: core.debugger
   :platform: Unix
   :synopsis: HydraTK core integrated debugger
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import sys, os, multiprocessing, inspect, traceback
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
    """ Class Debugger
    """
    
    _debug             = False
    _debug_level       = 1
    _debug_channel     = []
    _debug_channel_map = {
                           1 : [10,11], 
                           2 : [10,12],
                           3 : [10,13],
                           4 : [10,14],
                           5 : [10,15],                          
                          10 : [1,2], 
                          11 : [1,3], 
                          12 : [1,4],
                          13 : [1,5], 
                          14 : [1,6], 
                          15 : [1,7], 
                          16 : [1,8]
                         }    
    
    def fromhere(self, trace_level=1):
        """Method returns location of executed code 
        
        Dictionary {file, module, func, line, call_path}
        
        Args:     
           trace_level (int): level in stacktrace     
           
        Returns:
           dict: code location       
                
        """ 
                 
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
        """Method returns executed function name
        
        Args:       
           none
           
        Returns:
           str: function      
                
        """ 
                
        return sys._getframe(1).f_code.co_name        
    
    def file(self):       
        """Method returns executed filename
        
        Args:       
           none
           
        Returns:
           str: filename      
                
        """ 
                 
        return sys._getframe(1).f_code.co_filename

    def line(self):   
        """Method returns executed line number
        
        Args:       
           none
           
        Returns:
           int: line number      
                
        """ 
                     
        return sys._getframe(1).f_lineno
    
    def module(self):
        """Method returns executed module name
        
        Args:       
           none
           
        Returns:
           str: module      
                
        """ 
                
        fp = sys._getframe(1).f_code.co_filename
        modname = os.path.basename(fp)
        modarg = modname.split('.')
        return modarg[0]
        
    def errmsg(self, *args):
        """Method prints error message
        
        Args:
           args (list): list of arguments       
           
        Returns:
           void      
                
        """ 
                
        print(args)
    
    def dmsg(self, event_id, *args):
        """Method sends debug message via event
        
        Args:
           event_id (str): event
           args (args): arguments       
           
        Returns:
           void   
           
        Raises:
           event: event_id   
                
        """ 
                
        if (self._debug):        
            self.fire_event(event.Event(event_id,*args))
        
    def match_channel(self, channel):
        """Method checks if required channels are tracked by debugger
        
        Args:
           channel (obj): required channel as int (channel id), list (channel ids)   
           
        Returns:
           bool: result   
                
        """ 
                
        if len(self._debug_channel) == 0: # channel filters off
            return True
        else:        
            if type(channel).__name__ == 'list':
                return len(list(set(self._debug_channel).intersection(channel))) > 0
                 
            if type(channel).__name__ == 'int':
                return channel in self._debug_channel
            
            return False #unknown type
                                    
    def dout(self, msg, location={'file' : '', 'line' : '', 'module': '', 'func' : '', 'call_path' : ''}, level=1, channel=[]):  
        """Method prints debug message
        
        Configuration options:
        System/Debug/msg_format
        System/Debug/term_color
        
        Args:
           msg (str): message
           location (dict): location of executed code as dictionary {file, line, module, func, call_path}
                            format returned by method fromhere
           level (int): required debug level, default 1
           channel (obj): required channel as int, channels as list of int, default all    
           
        Returns:
           void   
                
        """ 
                              
        if (self._debug and self._debug_level >= level and self.match_channel(channel) == True):
            thrid = '0' if multiprocessing.current_process().name == 'MainProcess' else multiprocessing.current_process().name            
            msg_format = '[{timestamp}] Debug({level}): {callpath}:{func}:{thrid}: {msg}'
            
            # override message format if configured
            if 'msg_format' in self.cfg['System']['Debug'] and self.cfg['System']['Debug']['msg_format'] != '':
                msg_format = self.cfg['System']['Debug']['msg_format']
            
            now = datetime.now()
            now_ms = "{0}".format(round(int(now.strftime("%f")).__float__() / 1000000,3))
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
            
            # override message color if configured            
            if 'term_color' in self.cfg['System']['Debug'] and self.cfg['System']['Debug']['term_color'] is not None and '#' == self.cfg['System']['Debug']['term_color'][0]:
                rgb_color = self.cfg['System']['Debug']['term_color'].replace('#','')
                msg_text = colorize(msg_text, int(rgb_color,16)) 
                
            print(msg_text)
            sys.stdout.flush()
            
    def wout(self, msg, location={'file' : '', 'line' : '', 'module': '', 'func' : '', 'call_path' : ''}):
        """Method prints warning message

        Args:
           msg (str): message
           location (dict): location of executed code as dictionary {file, line, module, func, call_path}
                            format returned by method fromhere
           
        Returns:
           void   
                
        """ 
                
        thrid = '0' if multiprocessing.current_process().name == 'MainProcess' else multiprocessing.current_process().name
        #self._stdio_lock.acquire()
        print("Warning: %s:%s:%s: %s " % (location['call_path'],location['func'],thrid,msg))
        sys.stdout.flush()
        #self._stdio_lock.release()
    
        
    def errout(self, msg, location={'file' : '', 'line' : '', 'module': '', 'func' : '', 'call_path' : ''}):
        """Method prints error message

        Args:
           msg (str): message
           location (dict): location of executed code as dictionary {file, line, module, func, call_path}
                            format returned by method fromhere
           
        Returns:
           void   
                
        """
                
        thrname = '0' if multiprocessing.current_process().name == 'MainProcess' else multiprocessing.current_process().name
        #self._stdio_lock.acquire()
        print("Error: %s:%s:%s: %s " % (location['call_path'],location['func'],thrname,msg))        
        sys.stdout.flush()
        #self._stdio_lock.release()

    def exout(self, exc_type, exc_msg, exc_traceback):
        """Method prints exception including traceback

        Args:
           exc_type (str): type of exception
           exc_msg (str): message
           exc_traceback (obj): traceback
           
        Returns:
           void   
                
        """
                
        thrname = '0' if multiprocessing.current_process().name == 'MainProcess' else multiprocessing.current_process().name
        #self._stdio_lock.acquire()
        print("Unhandled exception:%s: %s:\nmsg: %s\ntraceback:" % (thrname, exc_type, exc_msg))                         
        print("Traceback:")
        traceback.print_tb(exc_traceback)        
        
    def _ec_parent_tell_signal(self, oevent):
        #current = multiprocessing.current_process()
        #print('somebody wants to kill me'+"\n")
        pass
    '''notify Observer about the received signal '''            
    