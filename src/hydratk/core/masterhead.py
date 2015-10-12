# -*- coding: utf-8 -*-

"""This code is a part of Hydra framework

.. module:: masterhead
   :platform: Unix
   :synopsis: HydraTK master module.
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
import sys;
import os;
import errno;
import signal;
import threading;
import time;
import multiprocessing;
import pprint;

import inspect;
import imp;


import traceback;
import yaml;
import operator;
    
PYTHON_MAJOR_VERSION = sys.version_info[0];

if PYTHON_MAJOR_VERSION == 2:
    import ConfigParser as configparser;    
    
if PYTHON_MAJOR_VERSION == 3:    
    import configparser;      

from hydratk.core.propertyhead import PropertyHead;
from hydratk.core.corehead import CoreHead;

from hydratk.core import const, commands, event, events, message, messagerouter;
from hydratk.core.eventhandler import EventHandler; 
from hydratk.core.extension import Extension;
from hydratk.lib.compat import types;

from hydratk.lib.profiling.profiler import Profiler;
from hydratk.lib.array import multidict;
from hydratk.lib.console.commandlinetool import CommandlineTool;
from hydratk.lib.number import conversion;
from hydratk.lib.translation import translator;
from hydratk.translation import info;

HIGHLIGHT_START = chr(27) + chr(91) + "1m";
HIGHLIGHT_US = chr(27) + chr(91) + "4m";
HIGHLIGHT_END = chr(27) + chr(91) + "0m";
SHORT_DESC = HIGHLIGHT_START + const.APP_NAME + " v" + const.APP_VERSION + const.APP_REVISION + HIGHLIGHT_END + " load, performacne and stress testing tool";

class MasterHead(PropertyHead, CoreHead):
    """Class MasterHead extends from CoreHead decorated by EventHandler, Debugger and Profiler           
    """
    _instance = None;
    _instance_created = False;                 
        
    def __init__(self):
                  
        if MasterHead._instance_created == False:            
            raise ValueError("For creating class instance please use the get_head method instead!");
        if MasterHead._instance is not None:
            raise ValueError("A Class instantiation already exists, use get_head method instead!");
        
        '''Setting up global exception handler for uncaught exceptions''' 
        
        sys.excepthook = self.exception_handler;
          
        self._runlevel = const.RUNLEVEL_BASEINIT;
            
        current = threading.currentThread();
        current.status = const.CORE_THREAD_ALIVE;
                            
        self._trn = translator.Translator();
        """Checking for the --lang param presence"""
        if self.check_language() == False:          
            self._trn.set_language(self._language);
        
        self._import_global_messages();
                
        # self.dmsg('htk_on_warning', self._trn.msg('htk_cs', 'print_short_desc'), self.fromhere());        
        
        self._reg_self_fn_hooks();
        self._reg_self_command_hooks();
        self._reg_self_event_hooks();        
        if (len(sys.argv) > 1 and sys.argv[1] != 'help'):
            self.check_config();
                                          
    def exception_handler(self, extype, value, traceback):
        """Exception handler hook
           
           This method is registered as sys.excepthook callback and transforms unhandled exceptions to the HydraTK Event  
           
           Args:
              extype (str): Exception type           
              value (str): Exception message info
              traceback (obj) Exception traceback object        
        
        """
        try:
            ev = event.Event('htk_on_uncaught_exception', extype, value, traceback);                
            ev.set_data('type', extype);
            ev.set_data('value', value);
            ev.set_data('traceback', traceback);        
            self.fire_event(ev);
        
        except Exception as e:
            # import traceback
            print('Fatal error - Unhandled exception thrown in exception handler:')
            print('Type: %s' % extype)
            print('value: %s' % value)
            # print(repr(traceback.format_tb(traceback)))
        
    def get_translator(self):
        """Method returns current traslator object initialized from hydratrk.lib.translation.translator.Translator 
        
           Returns:            
              Translator (obj)
               
        """
        return self._trn;
    
    @staticmethod
    def get_head():                
        """Method is primary connector to HydraTK core
           
           This method returns current active MasterHead instance or creates a new one
           For preventing inner conflicts it's designed as singleton   
        
        Returns:            
           MasterHead (obj)
           
        Example:
        
        .. code-block:: python
        
            from hydratk.core.masterhead import MasterHead;        
                      
            mh = MasterHead.get_head();        
        
        """
        if MasterHead._instance is None:           
            MasterHead._instance_created = True;
            try:             
                MasterHead._instance = MasterHead();
            except Exception as e:
                print("Exception in user code:")
                print("-"*60)
                traceback.print_exc(file=sys.stdout)
                print("-"*60) 
                MasterHead._instance_created = False;
                raise e;                                            
        return MasterHead._instance;    
        
    def get_config(self):
        """Method return current loaded configuration  
        
        Returns:            
              self._config (dict)
           
        Example:
        
        .. code-block:: python
        
              from hydratk.core.masterhead import MasterHead;        
                      
              mh = MasterHead.get_head();
              config = mh.get_config();         
        """        
        return self._config;
                                
    def check_language(self):
        """Method checks for language change input parameters from command line and validates if it's supported 
        
        Returns:            
              language_changed (bool) - True in case if it's supported otherwise False 
        
        """        
        from hydratk.translation import info;
        language_changed = False;
        i = 0;
        for o in sys.argv:            
            if o == '-l' or o == '--language':                
                if sys.argv.index(o) < (len(sys.argv) - 1):                    
                    lang = sys.argv[i + 1];                    
                    if (lang in info.languages):                        
                        self._language = lang;
                        self._trn.set_language(self._language);                        
                        language_changed = True;
                        break;
                    else:
                        self.dmsg('htk_on_warning', self._trn.msg('htk_invalid_lang_set', lang), self.fromhere());
                else:
                    self.dmsg('htk_on_warning', self._trn.msg('htk_opt_ignore', 'Language', lang), self.fromhere());                    
            i = i + 1;
        return language_changed;
                
    def check_config(self):
        """Method checks for config file change input parameters from command line and validates its existence
           If the new config file exists, then current config file path will be replaced by new one 
        
        Returns:            
           config_changed (bool) - True in case if config file exists otherwise False 
        
        """        
        i = 0;
        config_changed = False;
        for o in sys.argv:
            if o == 'help': break;
            if o == '-c' or o == '--config':                
                if sys.argv.index(o) < (len(sys.argv) - 1):
                    config_file = sys.argv[i + 1];
                    if (os.path.exists(config_file)):
                        self._config_file = config_file;
                        config_changed = True;
                        break;
                    else:
                        self.dmsg('htk_on_warning', self._trn.msg('htk_conf_not_exists', config_file), self.fromhere());
                else:
                    self.dmsg('htk_on_warning', self._trn.msg('htk_opt_ignore', 'Config', ''), self.fromhere());
                    
            i = i + 1; 
        return config_changed;

    def match_short_option(self, opt, value_expected=False):
        """Method registers command line short option check       
    
        Args:
           opt (str): Short option string           
           value_expected (bool): Whether the option value is expected or not           
           
        Raises:            
           ValueError if the option is already registered for matching
           ValueError if the option is an empty string 
        
        """
        if opt != '': 
            if commands.short_opts.find(opt) < 0:
                commands.short_opts = commands.short_opts + opt;
                commands.getopt_short_opts = commands.getopt_short_opts + opt if value_expected == False else commands.getopt_short_opts + opt + ':';  
            else:                
                raise ValueError("Short option " + opt + " is already registered for matching");
        else:
            raise ValueError("Short option " + opt + " is not valid string");
        
    def match_long_option(self, opt, value_expected=False):
        """Method registers command line long option check       
    
        Args:
           opt (str): Short option string           
           value_expected (bool): Whether the option value is expected or not           
           
        Raises:            
           ValueError: if the option is already registered for matching or the option is an empty string            
        
        """
        if opt != '': 
            if opt not in commands.long_opts:                
                commands.long_opts.append(opt);
                add_opt = opt if value_expected == False else opt + '=';
                commands.getopt_long_opts.append(add_opt);  
            else:                
                raise ValueError("Long option " + opt + " is already registered for matching");
        else:
            raise ValueError("Long option " + opt + " is not valid option string");
            
    def match_command(self, cmd):
        """Method registers command line command check       
    
        Args:
           cmd (str): Command string                                 
           
        Raises:            
           ValueError: if the command is already registered for matching or the command is an empty string           
        """        
        if cmd != '': 
            if cmd not in commands.commands:
                commands.commands.append(cmd);
            else:                
                raise ValueError("Command " + cmd + " is already registered for matching");
        else:
            raise ValueError("Command " + cmd + " is not valid string");
                
    
    def register_fn_hook(self, fn_id, callback=''):
        """Method adds/replaces functionality hook
        
           Only one callback can be registered.
           This method is usable for functionality extending, replacement.
        
        Args:
           fn_id (mixed): string functionality id or list of dictionaries in format {'fn_id' : 'functionality_id', 'callback' : callable_fc }           
           callback (callable): User defined callback
               
        Returns:
           bool: register success in case that fn_id is non-empty string
           int: number of successfully registered fn hooks in case that fn_id is list of dictionaries with multiple defined hooks            
             
        Example:
         
        .. code-block:: python  
         
             from hydratk.core.MasterHead import MasterHead;                                                        
             
             mh = MasterHead.get_head();                                  
             mh.register_fn_hook('mh_bootstrap', my_bootstrapper);              
             
        """
        result = False;
        if (type(fn_id).__name__ == 'list'):            
            result = 0;
            for fnh in fn_id:                              
                if (fnh['fn_id'] != '' and hasattr(fnh['callback'], '__call__')): 
                    self._fn_hooks[fnh['fn_id']] = fnh['callback'];                   
                    result = result + 1;    
                    
        elif (fn_id != '' and hasattr(callback, '__call__')):
            self._fn_hooks[fn_id] = callback;                                                          
            result = True;            
        return result;
    
    def run_fn_hook(self, fn_id):
        """Method is processing registered callback for specified fn_id.
           
           This method is usable for functionality extending, replacement. 
        
        Args:
           fn_id (str): functionality id
                   
        Returns:            
           void
           
        Example:
        
        .. code-block:: python
        
           from hydratk.core.masterhead import MasterHead;
           from hydratk.core.event import Event;
                      
           mh = MasterHead.get_head();
           mh.run_fn_hook('mh_bootstrap');
        
        """
        if fn_id in self._fn_hooks:
            if self._fn_hooks[fn_id]() != True:            
                raise Exception('Functionality Hook error, have to return True') 
            
    def register_command_hook(self, cmd, callback=''):
        """Method adds command hook
        
           This method is usable for functionality extending, replacement, notification purposes etc.
        
        Args:
           cmd (mixed): string Command or list of dictionaries in format {'command' : 'defined_command', 'callback' : callable_fc }
           callback (callable): User defined callback
               
        Returns:
           bool: in case that cmd is defined by string 
           int: number of successfully added hooks in case that cmd is dictionary with multiple defined callbacks
             
        Example:
         
        .. code-block:: python  
         
             from hydratk.core.MasterHead import MasterHead;                                           
                          
             multi_hook = [
                           {'command' : 'mycommand1', 'callback' : obj1.fc_command_handler1 }, # you can specify multiple command hooks
                           {'command' : 'mycommand2', 'callback' : obj2.fc_command_handler2 },
                           {'command' : 'mycommand3', 'callback' : fc_command_handler3 }
                          ];
             
             mh = MasterHead.get_head();                                  
             mh.register_command_hook(multi_hook); # register all hooks at once
             mh.register_command_hook('mycommand4', fc_command_handler); # single registration  
             
        """
        result = False;
        if (type(cmd).__name__ == 'list'):            
            result = 0;
            for ch in cmd:                              
                if (ch['command'] != '' and hasattr(ch['callback'], '__call__')): 
                    record = {
                       'callback' : ch['callback']
                    };
                    if ch['command'] not in self._cmd_hooks:
                        self._cmd_hooks[ch['command']] = [];
                    self._cmd_hooks[ch['command']].append(record);                    
                    result = result + 1;                 
                                    
        elif (cmd != '' and hasattr(callback, '__call__')):
            record = {
              'callback' : callback
            };
            if cmd not in self._cmd_hooks:
                self._cmd_hooks[cmd] = [];                                                                                          
            self._cmd_hooks[cmd].append(record);                                               
            result = True;            
        return result;
    
    def register_command_option_hook(self, cmd_opt, callback=''):
        """Methods adds command option listener.
           
           This method is usable for functionality extending, replacement, notification purposes etc. 
        
           Args:
              cmd_opt (list or string): Command option
              callback (callable): Function callback 
        
           Returns:
              bool - in case that cmd_opt is defined by string 
              int  - number of successfully added hooks in case that cmd_opt is dictionary with multiple defined callbacks
           
           Example:
           
           .. code-block:: python
        
              from hydratk.core.MasterHead import MasterHead;
              
              multi_hook = [
                           {'command_option' : 'option', 'callback' : obj1.fc_command_handler1 }, # you can specify multiple command hooks
                           {'command_option' : 'mycommand2', 'callback' : obj2.fc_command_handler2 },
                           {'command_option' : 'mycommand3', 'callback' : fc_command_handler3 }
                          ];
                          
              mh = MasterHead.get_head();.  
           
        """
        result = False;
        if (type(cmd_opt).__name__ == 'list'):            
            result = 0;
            for ch in cmd_opt:                
                if (ch['command_option'] != '' and hasattr(ch['callback'], '__call__')): 
                    record = {
                       'callback' : ch['callback']
                    };
                    if cmd_opt not in self._cmd_opt_hooks:
                        self._cmd_opt_hooks[cmd_opt] = [];                                                                          
                    self._cmd_opt_hooks[cmd_opt].append(record);  
                    result = result + 1; 
                                
        elif (cmd_opt != '' and hasattr(callback, '__call__')):
            record = {
              'callback' : callback
            };
            if cmd_opt not in self._cmd_opt_hooks:
                self._cmd_opt_hooks[cmd_opt] = [];                                                                          
            self._cmd_opt_hooks[cmd_opt].append(record);                                                
            result = True;            
        return result;
        
        
    def register_event_hook(self, event, callback='', unpack_args=False, priority=const.EVENT_HOOK_PRIORITY):
        """Methods registers event listener.
           
           This method is useful for extending the system functionality
        
        Args:
           event (list or string): event 
           callback (callable): function callback
           unpack_args (bool): optional request that arguments from event object will be passed directly to listener, default false
           priority (int): optional priority number > 0, lower number means higher priority, default value is const.EVENT_HOOK_PRIORITY 
        
        Returns:
           bool - in case that cmd_opt is defined by string 
           int  - number of successfully registered hooks in case that event is dictionary with multiple defined callbacks
           
        Example:
        
        .. code-block:: python   
        
           from hydratk.core.masterhead import MasterHead;
           from hydratk.core import const;                      
           
           mh = MasterHead.get_head();
           
           hook = [
                   {'event' : 'htk_on_error', 'callback' : self.my_error_handler, 'unpack_args' : True, 'priority' : const.EVENT_HOOK_PRIORITY - 1}, # will be prioritized        
                   {'event' : 'htk_on_warning', 'callback' : self.my_warning_handler, 'unpack_args' : False}
                  ];            
                      
           mh.register_event_hook(hook);
           
        """
        result = False;
        if (type(event).__name__ == 'list'):                       
            result = 0;
            for eh in event:                
                if (eh['event'] != '' and hasattr(eh['callback'], '__call__')): 
                    record = {
                       'callback' : eh['callback'],
                       'unpack_args' : eh['unpack_args'] if 'unpack_args' in eh else False
                    };
                    
                    priority = eh['priority'] if 'priority' in eh and eh['priority'] >= 0 else const.EVENT_HOOK_PRIORITY;
                    
                    if eh['event'] not in self._event_hooks:
                        self._event_hooks[eh['event']] = {};
                    if priority not in self._event_hooks[eh['event']]:
                        self._event_hooks[eh['event']][priority] = [];
                                                                                   
                    self._event_hooks[eh['event']][priority].append(record);
                    result = result + 1; 
                # todo silently notify invalid hook
                                
        elif (event != '' and hasattr(callback, '__call__')):
            record = {
              'callback'    : callback,
              'unpack_args' : unpack_args
            };
            priority = priority if priority >= 0 else const.EVENT_HOOK_PRIORITY;
            if eh['event'] not in self._event_hooks:
                self._event_hooks[eh['event']] = {};    
            if priority not in self._event_hooks[event]:
                        self._event_hooks[event][priority] = [];                                                                                                 
            self._event_hooks[event][priority].append(record);                                                           
            result = True;
        # todo silently notify invalid hook                    
        return result;                 
                    
    def fire_event(self, oevent):
        """Method is processing specified event callbacks.
           
           This method is usable for functionality extending, replacement, notification purposes etc. 
        
        Args:
           oevent (obj): Event object type  hydratk.core.event.Event
        
        Returns:            
           int  - number of successfully processed event registered callbacks
           
        Example:
        
        .. code-block:: python
        
           from hydratk.core.masterhead import MasterHead;
           from hydratk.core.event import Event;
                      
           mh = MasterHead.get_head();
           event_id = 'myprefix_on_something_important';
           oevent = Event('event_id');
           oevent.set_data('alert','I just finished work');
           print('This event was processed %d times' % mh.fire_event(oevent));
           
        """
          
        fe_count = 0;
        event_id = oevent.id();                
        before_event_id = '^{0}'.format(event_id.replace('^', ''));         
        after_event_id = '${0}'.format(event_id.replace('$', ''));     
                   
        if event_id not in (before_event_id, after_event_id) and event_id in self._event_hooks and oevent.skip_before_hook is False:            
            hbh_ev = event.Event(before_event_id, oevent);                                     
            hbh_ev.set_data('target_event', oevent);                           
            self.fire_event(hbh_ev);
            if hbh_ev.will_run_default() == False:
                return fe_count;
        
        if event_id in self._event_hooks and oevent.propagate():                                             
            i = 0;
            for _, records in sorted(self._event_hooks[event_id].items(), key=operator.itemgetter(0)):  # _ unused priority
                for record in records:
                    if oevent.propagate() == False: return fe_count;
                    cb = record['callback']; 
                    if record['unpack_args']:
                        cb(oevent, *oevent.args());
                    else:
                        cb(oevent);
                    i += 1;
                fe_count = i;                                    
                                    
        if event_id not in (before_event_id, after_event_id) and event_id in self._event_hooks and oevent.propagate() and oevent.skip_after_hook is False:
            hah_ev = event.Event(after_event_id, oevent);                
            hah_ev.set_data('source_event', oevent);        
            self.fire_event(hah_ev);
        
        return fe_count;
                
    def apply_command_options(self):
        if ('--debug' in self._option_param):
            if (type(self._option_param['--debug'][0]).__name__ == 'str' and self._option_param['--debug'][0].isdigit()):                            
                self._debug = conversion.int2bool(self._option_param['--debug'][0]);
                self.dmsg('htk_on_debug_info', self._trn.msg('htk_opt_set', 'Debug', self._debug.__str__()), self.fromhere());            
            else:
                debug_value = self._option_param['--debug'][0].__str__() if self._option_param['--debug'][0] != {} else ''; 
                self.dmsg('htk_on_warning', self._trn.msg('htk_opt_ignore', 'Debug', debug_value), self.fromhere());
                
        if ('--debug-level' in self._option_param):    
            if (type(self._option_param['--debug-level'][0]).__name__ == 'str' and self._option_param['--debug-level'][0].isdigit() and int(self._option_param['--debug-level'][0]) > 0):            
                self._debug_level = int(self._option_param['--debug-level'][0]);
                self.dmsg('htk_on_debug_info', self._trn.msg('htk_opt_set', 'Debug level', self._debug_level.__str__()), self.fromhere());                            
            else:
                debug_level_value = self._option_param['--debug-level'][0].__str__() if self._option_param['--debug-level'][0] != {} else '';                 
                self.dmsg('htk_on_warning', self._trn.msg('htk_opt_ignore', 'Debug level', debug_level_value), self.fromhere());
                    
        if ('--language' in self._option_param):               
            if (type(self._option_param['--language'][0]).__name__ == 'str' and self._option_param['--language'][0] != {} and self._option_param['--language'][0] in info.languages):            
                self._language = self._option_param['--language'][0];
                self.dmsg('htk_on_debug_info', self._trn.msg('htk_opt_set', 'Language', self._language), self.fromhere());                            
            else:
                lang_value = self._option_param['--language'][0].__str__() if self._option_param['--language'][0] != {} else '';                 
                self.dmsg('htk_on_warning', self._trn.msg('htk_opt_ignore', 'Debug level', lang_value), self.fromhere());
                
                       
              
    def get_language(self):
        return self._language;
    
    def have_command_action(self):        
        return True if self._command != None else False
    
    def get_command_action(self):
        return self._command;
    '''
    def get_opt_alias_str(self, opt):             
        result = '';
        for a, o in commands.command_opt_alias.items():            
            if (opt == o):
                result = result + a + ',';
        return result;
    '''    
    
    def service_registered(self, service_name):        
        for service in self._app_service:
            if service_name == service.name: return True;
        return False;    
        
    def register_service(self, service_name, description, cb):
        if not isinstance(service_name, types.basestring) or service_name == '':
            raise TypeError('Service name must be a valid string, your input was: ' + service_name);
        if self.service_registered(service_name):
            raise SystemError('Service with name: "' + service_name + '" already registered');
        if (description == ''): 
            raise ValueError('Service description has to be specified');
        if not callable(cb):
            raise ValueError('Callback parameter must be a callable object');
        service_status = multiprocessing.Value('i', const.SERVICE_STATUS_STOPPED);                                
        parent_conn, child_conn = multiprocessing.Pipe(); 
        service_starter = self._service_starter;              
        service = multiprocessing.Process(target=service_starter, name=service_name, args=(cb, service_status, child_conn));
        service.pipe_conn = parent_conn;
        service.service_name = service_name;
        service.service_desc = description;
        service.service_status = service_status;
        self._app_service.append(service);
        self.dmsg('htk_on_debug_info', self._trn.msg('htk_app_service_reg_ok', service_name, description), self.fromhere());
        return True;
    
    def unregister_service(self, service_name):
        pass
    
    def start_service(self, service_name):
        for service in self._app_service:
            if service_name == service.name and not service.is_alive():
                service.start();                
                if service.is_alive():
                    self.dmsg('htk_on_debug_info', self._trn.msg('htk_app_service_start_ok', service_name), self.fromhere());
                    return True;
                else:
                    # raise Exception("Failed to start application service "+service_name);    
                    self.dmsg('htk_on_debug_info', "Failed to start service", self.fromhere());
            else:
                self.dmsg('htk_on_debug_info', self._trn.msg('htk_app_service_start_ok', service_name), self.fromhere());
                    
        return False;
    
    def stop_service(self, service_name):        
        pass
    
    def send_service_msg(self, service_name):
        pass
    
    def stop_services(self):
        for service in self._app_service:
            if service.pid != None:
                service_name = service.service_name;                          
                service.service_status.value = const.SERVICE_STATUS_STOPPED;                
                os.kill(int(service.pid), signal.SIGINT);
                self.dmsg('htk_on_debug_info', self._trn.msg('htk_app_service_stop', service_name), self.fromhere());
                service.join(const.PROCESS_JOIN_TIMEOUT);
                if service.is_alive():
                    self.dmsg('htk_on_debug_info', self._trn.msg('htk_app_service_stop_failed', service_name), self.fromhere());
                    self.dmsg('htk_on_debug_info', self._trn.msg('htk_app_service_stop_hard', service_name), self.fromhere()); 
                    os.kill(int(service.pid), signal.SIGKILL);
            else: self.dmsg('htk_on_debug_info', self._trn.msg('htk_app_service_inactive_skip', service.service_name), self.fromhere());
                
                    
    def init_core_threads(self): 
        i = 1;       
        while i <= self._num_threads:
            self.add_core_thread(i);
            i = i + 1;        
    
    def destroy_core_threads(self):
        for thread in self._thr:
            name = thread.name;
            thread.status.value = const.CORE_THREAD_EXIT;
            self.dmsg('htk_on_debug_info', self._trn.msg('htk_cthread_destroy', name), self.fromhere());
            thread.join();
                
    def add_core_thread(self, i=None):        
        nexti = len(self._thr) + 1 if i == None else i;
        status = multiprocessing.Value('i', const.CORE_THREAD_WORK);
        action_status = multiprocessing.Value('i', const.CORE_THREAD_ACTION_NONE);  
        is_alive_check = multiprocessing.Value('d', time.time());             
        parent_conn, child_conn = multiprocessing.Pipe();               
        current = multiprocessing.Process(target=self.c_worker, name=nexti, args=(nexti, status, action_status, child_conn, is_alive_check));
        
        current.last_ping_response = 0;
        current.next_check_time = time.time() + const.CORE_THREAD_PING_TIME;
        current.response_alert_level = 0;
        current.status = status;  
        current.action_status = action_status;      
        current.pipe_conn = parent_conn;
        current.is_alive_check = is_alive_check;
        current.num = nexti;                        
        self._thr.append(current); 
        self.dmsg('htk_on_debug_info', self._trn.msg('htk_cthread_init', nexti), self.fromhere());
        current.start();
    

        
            
