# -*- coding: utf-8 -*-
"""HydraTK core integrated debugger

.. module:: core.debugger
   :platform: Unix
   :synopsis: HydraTK core integrated debugger
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import sys
import os
import multiprocessing
import inspect
import traceback
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

    _debug = False
    _debug_level = None
    _debug_channel = []
    _debug_channel_map = {
        1: [10, 11],
        2: [10, 12],
        3: [10, 13],
        4: [10, 14],
        5: [10, 15],
        10: [1, 2],
        11: [1, 3],
        12: [1, 4],
        13: [1, 5],
        14: [1, 6],
        15: [1, 7],
        16: [1, 8]
    }
    
    _dbg_msg_format_vars = {       
       'lrb' : '(',
       'rrb' : ')'         
    }
     
    @property
    def dbg_msg_format_vars(self):
        return self._dbg_msg_format_vars
             
    def dbg_class_has_method(self, class_type, method_name):
        """Method returns class type if class has implemented selected method_name 

        Dictionary {file, module, func, line, call_path}

        Args:     
           class_type (mixed): class type definition or tuple of class types
           method_name (str): method name     

        Returns:
           type: class type - if class has implemented selected method_name        
           bool: False
        """        
        result = False
        if type(class_type).__name__ not in('type', 'tuple'): 
            raise TypeError("Invalid input type for class_type")
        if type(method_name).__name__ not in ('str') or method_name == '':
            raise TypeError("Invalid input type for method_name")
         
        if type(class_type).__name__ == 'tuple':            
            for cl in class_type:                               
                if hasattr(cl, method_name) and inspect.ismethod(getattr(cl, method_name)):
                    result = cl
                    break
        else:                     
            if hasattr(class_type, method_name) and inspect.ismethod(getattr(class_type, method_name)):
                result = class_type
        
        return result            
        
    def fromhere(self, trace_level=1):
        """Method returns location of executed code 

        Dictionary {file, module, class, func, line, call_path}

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
        class_name = None        
        call_path = mod.__name__ if hasattr(mod, '__name__') else '__main__'
        
        if 'self' in sys._getframe(trace_level).f_locals:
            classes = list(sys._getframe(trace_level).f_locals["self"].__class__.__bases__)
            classes.append(sys._getframe(trace_level).f_locals["self"].__class__)
            
            class_type = self.dbg_class_has_method(tuple(classes), sys._getframe(trace_level).f_code.co_name)
            if class_type != False:
                class_name = class_type.__name__                         
        result = {
                   'file': sys._getframe(trace_level).f_code.co_filename,
                   'line': sys._getframe(trace_level).f_lineno,
                   'module': modarg[0],
                   'class' : class_name,
                   'func': sys._getframe(trace_level).f_code.co_name,
                   'call_path': call_path
                }
        return result

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

    def errmsg(self, msg):
        """Method sends error message

        Args:
           msg (str): error message
               

        Returns:
           void   
     
        """
        if self._error_info:
            if type(msg).__name__ == 'tuple' and len(msg) > 0:
                msg_key = msg[0]
                msg_params = ()
                if len(msg) > 1:
                    msg_params = msg[1:]
                    msg = self._trn.msg(msg_key, *msg_params)
                else:
                    msg = self._trn.msg(msg_key)
            
            self.fire_event(event.Event('htk_on_error', msg, self.fromhere(2)))
     
            
    def warnmsg(self, msg):
        """Method sends warning message

        Args:
           msg (str): warning message
               

        Returns:
           void   
     
        """
        if self._warning_info:
            if type(msg).__name__ == 'tuple' and len(msg) > 0:
                msg_key = msg[0]
                msg_params = ()
                if len(msg) > 1:
                    msg_params = msg[1:]
                    msg = self._trn.msg(msg_key, *msg_params)
                else:
                    msg = self._trn.msg(msg_key)
            
            self.fire_event(event.Event('htk_on_warning', msg, self.fromhere(2))) 
                  

    def demsg(self, event_id, *args):
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
            self.fire_event(event.Event(event_id, *args))

    
    def dmsg(self, msg, level=1, channel=const.DEBUG_CHANNEL):
        """Method sends debug message

        Args:
           msg (str): message
           level (int): debug level
           channel (list): debug channel        

        Returns:
           bool: True if message was send to processing otherwise False


        """
           
        if self.debug is True:
            if self.debug_level is not None and level > self.debug_level:                 
                return False
            if len(self._debug_channel) > 0 and self.match_channel(channel) == False:        
                return False
            
            if type(msg).__name__ == 'tuple' and len(msg) > 0:
                msg_key = msg[0]
                msg_params = ()
                if len(msg) > 1:
                    msg_params = msg[1:]
                    msg = self._trn.msg(msg_key, *msg_params)
                else:
                    msg = self._trn.msg(msg_key)                               
            self.fire_event(event.Event('htk_on_debug_info', msg, self.fromhere(2), level, channel))
            return True

    def match_channel(self, channel, profile_channel = None):
        """Method checks if required channels are tracked by debugger

        Args:
           channel (obj): required channel as int (channel id), list (channel ids)
           profile_channel (list): logger profile channels   

        Returns:
           bool: result   

        """
        debug_channel = profile_channel if type(profile_channel).__name__ == 'list' else self._debug_channel
        if len(debug_channel) == 0:  # channel filters off
            return True
        else:
            if type(channel).__name__ == 'list':
                return len(list(set(debug_channel).intersection(channel))) > 0

            if type(channel).__name__ == 'int':
                return channel in debug_channel

            return False  # unknown type


    def dbg_format_exception_msg(self, profile, extype, msg, tb):
        
        # override message format if configured
        if 'format' in profile:
            msg_format = profile['format']
        else:
            msg_format = "[{timestamp}] EXCEPTION:[{thrid}): {msg}\n{trace}"
                
        thrid = '0' if multiprocessing.current_process().name == 'MainProcess' else multiprocessing.current_process().name
        now = datetime.now()
        now_ms = "{:.3f}".format(round(int(now.strftime("%f")).__float__() / 1000000, 3))
        now_ms = now_ms.split('.')[1]
        tb_lines = traceback.format_list(traceback.extract_tb(tb))
        trace = ''
        for tb_line in tb_lines:
            trace += "\t{0}".format(tb_line)
            
        format_options = {
           'timestamp' : now.strftime("%d/%m/%Y %H:%M:%S,{0}".format(now_ms)),
           'shorttime' : now.strftime("%H:%M:%S.{0}".format(now_ms)),        
            'thrid'    : thrid,
            'msg'      : msg,
            'extype'   : extype.__name__,
            'trace'    : trace 
        }
        format_options.update(self._dbg_msg_format_vars)            
        msg_text = msg_format.format(**format_options)

        # override message color if configured
        if 'term_color' in profile and profile['term_color'] is not None and '#' == profile['term_color'][0]:
            rgb_color = profile['term_color'].replace('#', '')
            msg_text = colorize(msg_text, int(rgb_color, 16))
        
                
        return msg_text
        

    def dbg_format_msg(self, profile, msg, location={'file': None, 'line': None, 'module': None, 'func': None, 'call_path': None, 'class' : None }, level=1, channel=[]):
        """Method implements message formating

        Args:     
           profile (dict)  : logger dictionary profile
           msg (string)    : message
           location (dict) : message trace parameters
           level (int)     : debug level
           channel (list)  : channel filter list

        Returns:
           bool: result

        """                  
        msg_text = False
        process_msg = False 
        
        if profile['log_type'] == 'debug':
            debug_level = self._debug_level if self._debug_level is not None else profile['level']
            debug_channel = self._debug_channel if len(self._debug_channel) > 0 else profile['channel']
            if (debug_level >= level and self.match_channel(channel, debug_channel) == True):
                process_msg = True
        else:
            process_msg = True
        
        if process_msg == True:
            thrid = '0' if multiprocessing.current_process().name == 'MainProcess' else multiprocessing.current_process().name
            

            # override message format if configured
            if 'format' in profile:
                msg_format = profile['format']
            else:
                msg_format = '[{timestamp}] DEBUG({level}): {callpath}:{func}:{thrid}: {msg}{lf}'
           
            now = datetime.now()
            now_ms = "{:.3f}".format(round(int(now.strftime("%f")).__float__() / 1000000, 3))
            now_ms = now_ms.split('.')[1]
            format_options = {
               'timestamp' : now.strftime("%d/%m/%Y %H:%M:%S,{0}".format(now_ms)),
               'shorttime' : now.strftime("%H:%M:%S.{0}".format(now_ms)),
               'level'     : level,
                'file'     : location['file'],
                'line'     : location['line'],
                'module'   : location['module'],
                'callpath' : location['call_path'],
                'func'     : "{0}.{1}".format(location['class'],location['func']) if location['class'] != None else location['func'],
                'thrid'    : thrid,
                'msg'      : msg,
                'channel'  : channel,
            }
            format_options.update(self._dbg_msg_format_vars)            
            msg_text = msg_format.format(**format_options)

            # override message color if configured
            if 'term_color' in profile and profile['term_color'] is not None and '#' == profile['term_color'][0]:
                rgb_color = profile['term_color'].replace('#', '')
                msg_text = colorize(msg_text, int(rgb_color, 16))

        return msg_text            
            
    
    def _ec_parent_tell_signal(self, oevent):
        #current = multiprocessing.current_process()
        #print('somebody wants to kill me'+"\n")
        pass
    '''notify Observer about the received signal '''
