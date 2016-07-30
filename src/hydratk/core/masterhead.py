# -*- coding: utf-8 -*-
"""HydraTK master module

.. module:: core.masterhead
   :platform: Unix
   :synopsis: HydraTK master module
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import sys
import os
import errno
import signal
import time
import multiprocessing
import pprint

import inspect
import imp


import traceback
import yaml
import operator
import threading

from hydratk.lib.exceptions.inputerror import InputError
    
PYTHON_MAJOR_VERSION = sys.version_info[0]

if PYTHON_MAJOR_VERSION == 2:
    import ConfigParser as configparser    
    
if PYTHON_MAJOR_VERSION == 3:    
    import configparser      

from hydratk.core.hookhead import ModuleLoader
from hydratk.core.propertyhead import PropertyHead
from hydratk.core.corehead import CoreHead
from hydratk.core.servicehead import ServiceHead

from hydratk.core import const 
from hydratk.core import commands
from hydratk.core import commandopt
from hydratk.core import event
from hydratk.core import events
from hydratk.core import message
from hydratk.core import messagerouter
from hydratk.core.eventhandler import EventHandler 
from hydratk.core.extension import Extension
from hydratk.lib.compat import types

from hydratk.lib.profiling.profiler import Profiler
from hydratk.lib.array import multidict
from hydratk.lib.console.commandlinetool import CommandlineTool
from hydratk.lib.number import conversion
from hydratk.translation.core import info
from hydratk.lib.translation import translator

HIGHLIGHT_START = chr(27) + chr(91) + "1m"
HIGHLIGHT_US = chr(27) + chr(91) + "4m"
HIGHLIGHT_END = chr(27) + chr(91) + "0m"
SHORT_DESC = HIGHLIGHT_START + const.APP_NAME + " v" + const.APP_VERSION + const.APP_REVISION + HIGHLIGHT_END + " load, performance and stress testing tool"

class MasterHead(PropertyHead, ServiceHead, CoreHead, ModuleLoader):
    """Class MasterHead extends from CoreHead decorated by EventHandler, Debugger and Profiler           
    """
    _instance = None
    _instance_created = False                 
        
    def __init__(self):
        """Class constructor
        
        MasterHead use singleton pattern, constructor should never be called directly
        
        Args:
           none
        
        Raises:
           error: ValueError       
                
        """         
                  
        if MasterHead._instance_created == False:            
            raise ValueError("For creating class instance please use the get_head method instead!")
        if MasterHead._instance is not None:
            raise ValueError("A Class instantiation already exists, use get_head method instead!")        
        
        '''Setting up global exception handler for uncaught exceptions''' 
        
        sys.excepthook = self.exception_handler
        
        '''Setting up basic functionality hooks'''
        self._reg_self_fn_hooks()
        
                                                  
    def exception_handler(self, extype, value, traceback):
        """Exception handler hook
           
           This method is registered as sys.excepthook callback and transforms unhandled exceptions to the HydraTK Event  
           
        Args:
           extype (str): Exception type           
           value (str): Exception message info
           traceback (obj) Exception traceback object   
              
        Returns:
           void
              
        Raises:
           event: htk_on_uncaught_exception     
        
        """
        try:
            ev = event.Event('htk_on_uncaught_exception', extype, value, traceback)                
            ev.set_data('type', extype)
            ev.set_data('value', value)
            ev.set_data('traceback', traceback)        
            self.fire_event(ev)
        
        except Exception as e:
            # import traceback
            print('Fatal error - Unhandled exception thrown in exception handler:')
            print('type: %s' % extype)
            print('value: %s' % value)
            # print(repr(traceback.format_tb(traceback)))
    
    def get_translator(self):
        """Method returns current traslator object initialized from hydratrk.lib.translation.translator.Translator 
        
        Args:
           none
        
        Returns:            
           obj: Translator
               
        """
        
        return self._trn
    
    @staticmethod
    def get_head():                
        """Method is primary connector to HydraTK core
           
           This method returns current active MasterHead instance or creates a new one
           For preventing inner conflicts it's designed as singleton   
        
        Args:
           none
        
        Returns:            
           obj: MasterHead
           
        Example:
        
        .. code-block:: python
        
            from hydratk.core.masterhead import MasterHead        
                      
            mh = MasterHead.get_head()        
        
        """
        
        if MasterHead._instance is None:           
            MasterHead._instance_created = True
            try:             
                MasterHead._instance = MasterHead()
            except Exception as e:
                print("Exception in user code:")
                print("-"*60)
                traceback.print_exc(file=sys.stdout)
                print("-"*60) 
                MasterHead._instance_created = False
                raise e                                            
        return MasterHead._instance    
        
    def get_config(self):
        """Method return current loaded configuration  
        
        Args:
           none
        
        Returns:            
           dict: self._config
           
        Example:
        
        .. code-block:: python
        
              from hydratk.core.masterhead import MasterHead        
                      
              mh = MasterHead.get_head()
              config = mh.get_config()         
        """  
              
        return self._config

    def check_run_mode(self):
        """Method checks for run_mode input parameter (-m, --run-mode) from command line and validates if it's supported 
        
        Args:
           none
        
        Returns:            
           bool: run_mode_changed, True in case if it's supported otherwise False 
        
        """             
           
        run_mode_changed = False
        i = 0
        for o in sys.argv:            
            if o == '-m' or o == '--run-mode':                
                if sys.argv.index(o) < (len(sys.argv) - 1):                    
                    mode = int(sys.argv[i + 1]) if (sys.argv[i + 1].isdigit()) else 0                   
                    if (mode in [
                                 const.CORE_RUN_MODE_SINGLE_APP,
                                 const.CORE_RUN_MODE_PP_APP,
                                 const.CORE_RUN_MODE_PP_DAEMON
                                ]):                        
                        self._run_mode = mode
                        self._trn.set_language(self._language)                        
                        run_mode_changed = True
                        break
                    else:
                        self.dmsg('htk_on_warning', self._trn.msg('htk_invalid_run_mode_set', mode), self.fromhere())
                else:
                    self.dmsg('htk_on_warning', self._trn.msg('htk_opt_ignore', 'run_mode', mode), self.fromhere())                    
            i = i + 1
        return run_mode_changed
                                    
    def check_language(self):
        """Method checks for language change input parameters (-l, --language) from command line and validates if it's supported 
        
        Args:
           none
        
        Returns:            
           bool: language_changed, True in case if it's supported otherwise False 
        
        """  
              
        from hydratk.translation.core import info
        language_changed = False
        i = 0
        for o in sys.argv:            
            if o == '-l' or o == '--language':                
                if sys.argv.index(o) < (len(sys.argv) - 1):                    
                    lang = sys.argv[i + 1]                    
                    if (lang in info.languages):                        
                        self._language = lang
                        self._trn.set_language(self._language)                        
                        language_changed = True
                        break
                    else:
                        self.dmsg('htk_on_warning', self._trn.msg('htk_invalid_lang_set', lang), self.fromhere())
                else:
                    self.dmsg('htk_on_warning', self._trn.msg('htk_opt_ignore', 'Language', lang), self.fromhere())                    
            i = i + 1
        return language_changed
                
    def check_config(self):
        """Method checks for config file change input parameters (-c, --config) from command line and validates its existence
           If the new config file exists, then current config file path will be replaced by new one 
        
        Args:
           none
        
        Returns:            
           bool: config_changed, True in case if config file exists otherwise False 
        
        """       
         
        i = 0
        config_changed = False
        for o in sys.argv:
            if o == 'help': break
            if o == '-c' or o == '--config':                
                if sys.argv.index(o) < (len(sys.argv) - 1):
                    config_file = sys.argv[i + 1]
                    if (os.path.exists(config_file)):
                        self._config_file = config_file
                        config_changed = True
                        break
                    else:
                        self.dmsg('htk_on_warning', self._trn.msg('htk_conf_not_exists', config_file), self.fromhere())
                else:
                    self.dmsg('htk_on_warning', self._trn.msg('htk_opt_ignore', 'Config', ''), self.fromhere())
                    
            i = i + 1 
        return config_changed

    def check_profile(self):
        """Method checks for profile option parameter (help, -p, --profile) with specified output statistics file           
        
        Args:
           none
        
        Returns:            
           tuple: result, bool enable_profiler, string statistics file 
        
        """        
        
        i = 0
        self.dmsg('htk_on_debug', "Checking profile option", self.fromhere())
        enable_profiler = False
        stats_file     = ''
        for o in sys.argv:
            if o == 'help': break
            if o == '-p' or o == '--profile':                                
                if sys.argv.index(o) < (len(sys.argv) - 2):
                    stats_file = sys.argv[i + 1]                    
                    if stats_file is not None and stats_file != '':
                        enable_profiler = True
                        self.dmsg('htk_on_debug', "Profiler enabled, stats will be written to the: {0}".format(stats_file), self.fromhere())                    
                else:
                    self.dmsg('htk_on_warning', self._trn.msg('htk_opt_ignore', 'Profile', ''), self.fromhere())
                    
            i = i + 1 
        return (enable_profiler, stats_file)

    def check_debug(self):
        """Method checks for debug option with specified level parameter (-d, --debug) from command line 
        
        Args:
           none
        
        Returns:            
           bool: debug_changed, True in case if it's set otherwise False 
        
        """        
                
        debug_changed = False
        i = 0
        for o in sys.argv:            
            if o == '-d' or o == '--debug':                
                if sys.argv.index(o) < (len(sys.argv) - 1):                    
                    debug_level = sys.argv[i + 1]  
                    if debug_level.encode().isdigit():
                        self._debug_level = int(debug_level) 
                        self._debug = True
                        self._trn.set_debug_level(debug_level)                
                        self.dmsg('htk_on_debug_info', self._trn.msg('htk_debug_level_set', self._debug_level), self.fromhere())                  
                        debug_changed = True
                    else:
                        self.dmsg('htk_on_warning', self._trn.msg('htk_invalid_debug_level_set', debug_level), self.fromhere())
                else:
                    self.dmsg('htk_on_warning', self._trn.msg('htk_opt_ignore', 'Debug', ''), self.fromhere())                    
            i = i + 1
        return debug_changed

    def check_debug_channel(self):
        """Method checks for debug channel option with specified channel filters from command line (-d, --debug-channel)
        
        Args:
           none
        
        Returns:            
           bool: debug_channel_changed, True in case if it's set otherwise False 
        
        """                
        debug_channel_changed = False
        i = 0
        for o in sys.argv:            
            if o == '-e' or o == '--debug-channel':                
                if sys.argv.index(o) < (len(sys.argv) - 1):                    
                    debug_channel = sys.argv[i + 1]  
                    if debug_channel.encode('utf-8').isdigit():
                        self._debug_channel = [int(debug_channel)]                                         
                        self.dmsg('htk_on_debug_info', self._trn.msg('htk_debug_channel_set', self._debug_channel[0]), self.fromhere())                  
                        debug_channel_changed = True
                    elif type(debug_channel).__name__ == 'str' and debug_channel != '' and ',' in debug_channel:
                        dch = debug_channel.split(',')
                        new_filter = []
                        for dchf in dch:
                            if dchf != '':
                                debug_channel_changed = True 
                                new_filter.append(int(dchf))
                        if debug_channel_changed:
                            self._debug_channel = new_filter
                    else:
                        self.dmsg('htk_on_warning', self._trn.msg('htk_invalid_debug_channel_set', debug_channel), self.fromhere())
                else:
                    self.dmsg('htk_on_warning', self._trn.msg('htk_opt_ignore', 'debug-channel', ''), self.fromhere())                    
            i = i + 1
        return debug_channel_changed
             
    def match_short_option(self, opt, value_expected=False, d_opt=None, allow_multiple=False, opt_group='htk'):
        """Method registers command line short option check       
    
        Args:
           opt (str): Short option string           
           value_expected (bool): Whether the option value is expected or not  
           d_opt (str): target option
           allow_multiple (bool): multiple option occurences allowed
           opt_group (obj): list or str, option group, default htk         
           
        Returns:
           void   
           
        Raises:            
           error: TypeError
        
        """
        
        if type(opt_group).__name__ == 'list':
            for optg in opt_group:
                if optg not in commandopt.short_opt:
                    commandopt.short_opt[optg] = []
                if opt not in commandopt.short_opt[optg]:
                    commandopt.short_opt[optg].append(opt)
                    opts = "-{0}".format(opt)
                    if optg not in commandopt.opt:
                        commandopt.opt[optg] = {}
                    commandopt.opt[optg][opts] = {
                                                    'd_opt'          : d_opt,
                                                    'has_value'      : value_expected,
                                                    'allow_multiple' : allow_multiple                           
                                                }
        elif type(opt_group).__name__ == 'str':
            if opt_group not in commandopt.short_opt:
                commandopt.short_opt[opt_group] = []
            if opt not in commandopt.short_opt[opt_group]:
                commandopt.short_opt[opt_group].append(opt)
                opts = "-{0}".format(opt)
                if opt_group not in commandopt.opt:
                    commandopt.opt[opt_group] = {}
                commandopt.opt[opt_group][opts] = {
                                                'd_opt'          : d_opt,
                                                'has_value'      : value_expected,
                                                'allow_multiple' : allow_multiple                           
                                            }
        
        else:
            raise TypeError('opt_group can be only of type list or str, got {0}'.format(type(opt_group).__name__))
        
    def match_long_option(self, opt, value_expected=False, d_opt=None, allow_multiple=False, opt_group='htk'):
        """Method registers command line long option check       
    
        Args:
           opt (str): long option string           
           value_expected (bool): Whether the option value is expected or not
           d_opt (str): target option
           allow_multiple (bool): multiple option occurences allowed
           opt_group (obj): list or str, option group, default htk                         
          
        Returns:
           void  
           
        Raises:            
           error: TypeError
        
        """
        
        if type(opt_group).__name__ == 'list':
            for optg in opt_group:
                if optg not in commandopt.long_opt:
                    commandopt.long_opt[optg] = []
                if opt not in commandopt.long_opt[optg]:
                    commandopt.long_opt[optg].append(opt)
                    optl = "--{0}".format(opt)
                    if optg not in commandopt.opt:
                        commandopt.opt[optg] = {}
                    commandopt.opt[optg][optl] = {
                                                    'd_opt'          : d_opt,
                                                    'has_value'      : value_expected,
                                                    'allow_multiple' : allow_multiple                           
                                                }
        elif type(opt_group).__name__ == 'str':
            if opt_group not in commandopt.long_opt:
                commandopt.long_opt[opt_group] = []
            if opt not in commandopt.long_opt[opt_group]:
                commandopt.long_opt[opt_group].append(opt)
                optl = "--{0}".format(opt)
                if opt_group not in commandopt.opt:
                    commandopt.opt[opt_group] = {}
                commandopt.opt[opt_group][optl] = {
                                                'd_opt'          : d_opt,
                                                'has_value'      : value_expected,
                                                'allow_multiple' : allow_multiple                           
                                            }
        
        else:
            raise TypeError('opt_group can be only of type list or str, got {0}'.format(type(opt_group).__name__))
    
    
    def match_cli_option(self, opt, value_expected=False, d_opt=None, allow_multiple=False, opt_group='htk'):
        """Method registers command option check       
    
        Args:
           opt (obj): tuple or list, short and long option strings        
           value_expected (bool): Whether the option value is expected or not   
           d_opt (str): target option
           allow_multiple (bool): multiple option occurences allowed
           opt_group (obj): list or str, option group, default htk                       
           
        Raises:            
           error: TypeError
        
        """
        
        if type(opt).__name__ not in ('tuple, list'):
            raise TypeError('option can be only of type tuple or list, got {0}'.format(type(opt).__name__))
        
        short_opt, long_opt = opt
        self.match_short_option(short_opt, value_expected, d_opt, allow_multiple, opt_group)
        self.match_long_option(long_opt, value_expected, d_opt, allow_multiple, opt_group) 

            
    def match_cli_command(self, cmd, opt_group='htk'):
        """Method registers command line command check       
    
        Args:
           cmd (str): Command string    
           opt_group (str): option group, default htk
           
        Returns:
           void                             
           
        Raises:            
           error: ValueError: if the command is already registered for matching or the command is an empty string           
        """
        
        if opt_group not in commandopt.cmd:
            commandopt.cmd[opt_group] = []
            
        if cmd != '': 
            if cmd not in commandopt.cmd[opt_group]:                
                commandopt.cmd[opt_group].append(cmd)                
                
            else:                
                raise ValueError(self._trn.msg('htk_cmd_registered', cmd))
        else:
            raise ValueError(self._trn.msg('htk_cmd_invalid', cmd))
                
    
    def set_cli_cmdopt_profile(self, profile):
        """Method sets new command option profile     
    
        Args:
           profile (str): option group
           
        Returns:
           void                             
           
        Raises:            
           error: InputError
                     
        """
                
        if type(profile).__name__ == 'str' and profile != '':
            self._opt_profile = profile
            if profile not in commandopt.opt: 
                commandopt.opt[profile] = {}
                
            if profile not in commandopt.long_opt:
                commandopt.long_opt[profile] = []
                
            if profile not in commandopt.short_opt:
                commandopt.short_opt[profile] = []
            
        else:
            raise InputError(0, [], "Option profile have to be non empty string type, got '{0}' '{1}'".format(profile, type(profile).__name__))
        
    def set_cli_appl_title(self, help_title, cp_string):
        """Method sets custom application title    
    
        Args:
           help_title (str): help
           cp_string (str): copyright
           
        Returns:
           void                             
           
        Raises:            
           error: InputError
                     
        """
                
        if type(help_title).__name__ == 'str' and type(cp_string).__name__ == 'str': 
            self._help_title = help_title
            self._cp_string = cp_string
        else:
            raise InputError(0, [], "help_title and cp_string have to be string type, got '{0}' '{1}'".format(type(help_title).__name__,type(cp_string).__name__))
            
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
         
             from hydratk.core.MasterHead import MasterHead                                                        
             
             mh = MasterHead.get_head()                                  
             mh.register_fn_hook('mh_bootstrap', my_bootstrapper)              
             
        """
        
        result = False
        if (type(fn_id).__name__ == 'list'):            
            result = 0
            for fnh in fn_id:                              
                if (fnh['fn_id'] != '' and hasattr(fnh['callback'], '__call__')): 
                    self._fn_hooks[fnh['fn_id']] = fnh['callback']                   
                    result = result + 1    
                    
        elif (fn_id != '' and hasattr(callback, '__call__')):
            self._fn_hooks[fn_id] = callback                                                          
            result = True            
        return result
    
    def run_fn_hook(self, fn_id, *args, **kwargs):
        """Method is processing registered callback for specified fn_id.
           
           This method is usable for functionality extending, replacement. 
        
        Args:
           fn_id (str): functionality id
           args (mixed): optional arguments
           kwargs (mixed): optional keyword arguments
                   
        Returns:            
           void
           
        Raises:
           exception: Exception
           
        Example:
        
        .. code-block:: python
        
           from hydratk.core.masterhead import MasterHead
           from hydratk.core.event import Event
                      
           mh = MasterHead.get_head()
           mh.run_fn_hook('mh_bootstrap')
        
        """
        
        if fn_id in self._fn_hooks:
            if self._fn_hooks[fn_id](*args,**kwargs) != True:            
                raise Exception(self._trn.msg('htk_fn_hook_invalid', fn_id)) 
    
    def dummy_fn_hook(self):
        """Method runs dummy hook
        
        Args:
           none
                   
        Returns:            
           bool: True
        
        """
                
        return True
     
    def start_pp_app(self):
        """Method starts application
        
        Args:
           none
                   
        Returns:            
           void
        
        """
                
        self._start_app()
    
    def stop_pp_app(self, force_exit=False):
        """Method stops application
        
        Args:
           force_exit (bool): force application termination
                   
        Returns:            
           void
        
        """
                
        self._stop_app(force_exit)
           
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
         
             from hydratk.core.MasterHead import MasterHead                                           
                          
             multi_hook = [
                           {'command' : 'mycommand1', 'callback' : obj1.fc_command_handler1 }, # you can specify multiple command hooks
                           {'command' : 'mycommand2', 'callback' : obj2.fc_command_handler2 },
                           {'command' : 'mycommand3', 'callback' : fc_command_handler3 }
                          ]
             
             mh = MasterHead.get_head()                                  
             mh.register_command_hook(multi_hook) # register all hooks at once
             mh.register_command_hook('mycommand4', fc_command_handler) # single registration  
             
        """
        
        result = False
        if (type(cmd).__name__ == 'list'):            
            result = 0
            for ch in cmd:                              
                if (ch['command'] != '' and hasattr(ch['callback'], '__call__')): 
                    record = {
                       'callback' : ch['callback']
                    }
                    if ch['command'] not in self._cmd_hooks:
                        self._cmd_hooks[ch['command']] = []
                    self._cmd_hooks[ch['command']].append(record)                    
                    result = result + 1                 
                                    
        elif (cmd != '' and hasattr(callback, '__call__')):
            record = {
              'callback' : callback
            }
            if cmd not in self._cmd_hooks:
                self._cmd_hooks[cmd] = []                                                                                          
            self._cmd_hooks[cmd].append(record)                                               
            result = True            
        return result
    
    def register_command_option_hook(self, cmd_opt, callback=''):
        """Methods adds command option listener.
           
           This method is usable for functionality extending, replacement, notification purposes etc. 
        
           Args:
              cmd_opt (list or string): Command option
              callback (callable): Function callback 
        
           Returns:
              bool: in case that cmd_opt is defined by string 
              int: number of successfully added hooks in case that cmd_opt is dictionary with multiple defined callbacks
           
           Example:
           
           .. code-block:: python
        
              from hydratk.core.MasterHead import MasterHead
              
              multi_hook = [
                           {'command_option' : 'option', 'callback' : obj1.fc_command_handler1 }, # you can specify multiple option hooks
                           {'command_option' : 'mycommand2', 'callback' : obj2.fc_command_handler2 },
                           {'command_option' : 'mycommand3', 'callback' : fc_command_handler3 }
                          ]
                          
              mh = MasterHead.get_head().  
           
        """
        
        result = False
        if (type(cmd_opt).__name__ == 'list'):            
            result = 0
            for ch in cmd_opt:                
                if (ch['command_option'] != '' and hasattr(ch['callback'], '__call__')): 
                    record = {
                       'callback' : ch['callback']
                    }
                    opt = ch['command_option']
                    if opt not in self._cmd_option_hooks:
                        self._cmd_option_hooks[opt] = []                                                                          
                    self._cmd_option_hooks[opt].append(record)  
                    result = result + 1 
                                
        elif (cmd_opt != '' and hasattr(callback, '__call__')):
            record = {
              'callback' : callback
            }
            if cmd_opt not in self._cmd_option_hooks:
                self._cmd_option_hooks[cmd_opt] = []                                                                          
            self._cmd_option_hooks[cmd_opt].append(record)                                                
            result = True            
        return result
        
        
    def register_event_hook(self, event, callback='', unpack_args=False, priority=const.EVENT_HOOK_PRIORITY):
        """Methods registers event listener.
           
           This method is useful for extending the system functionality
        
        Args:
           event (list or string): event 
           callback (callable): function callback
           unpack_args (bool): optional request that arguments from event object will be passed directly to the listener, default false
           priority (int): optional priority number > 0, lower number means higher priority, default value is const.EVENT_HOOK_PRIORITY 
        
        Returns:
           bool: in case that cmd_opt is defined by string 
           int: number of successfully registered hooks in case that event is dictionary with multiple defined callbacks
           
        Example:
        
        .. code-block:: python   
        
           from hydratk.core.masterhead import MasterHead
           from hydratk.core import const                      
           
           mh = MasterHead.get_head()
           
           hook = [
                   {'event' : 'htk_on_error', 'callback' : self.my_error_handler, 'unpack_args' : True, 'priority' : const.EVENT_HOOK_PRIORITY - 1}, # will be prioritized        
                   {'event' : 'htk_on_warning', 'callback' : self.my_warning_handler, 'unpack_args' : False}
                  ]            
                      
           mh.register_event_hook(hook)
           
        """
        
        result = False
        if (type(event).__name__ == 'list'):                       
            result = 0
            for eh in event:                
                if (eh['event'] != '' and hasattr(eh['callback'], '__call__')): 
                    record = {
                       'callback' : eh['callback'],
                       'unpack_args' : eh['unpack_args'] if 'unpack_args' in eh else False
                    }
                    
                    priority = eh['priority'] if 'priority' in eh and eh['priority'] >= 0 else const.EVENT_HOOK_PRIORITY
                    
                    if eh['event'] not in self._event_hooks:
                        self._event_hooks[eh['event']] = {}
                    if priority not in self._event_hooks[eh['event']]:
                        self._event_hooks[eh['event']][priority] = []
                                                                                   
                    self._event_hooks[eh['event']][priority].append(record)
                    result = result + 1 
                # todo silently notify invalid hook
                                
        elif (event != '' and hasattr(callback, '__call__')):
            record = {
              'callback'    : callback,
              'unpack_args' : unpack_args
            }
            priority = priority if priority >= 0 else const.EVENT_HOOK_PRIORITY
            if event not in self._event_hooks:
                self._event_hooks[event] = {}    
            if priority not in self._event_hooks[event]:
                        self._event_hooks[event][priority] = []                                                                                                 
            self._event_hooks[event][priority].append(record)                                                           
            result = True
        # todo silently notify invalid hook                    
        return result                 
    
    def unregister_event_hook(self, event, callback=None):
        """Methods unregisters event listener(s) for specified event.
           
           This method is useful for extending the system functionality
        
        Args:
           event (string): event 
           callback (callable): matching callback            
        
        Returns:
           bool: in case that callback is not specified
           int: number of successfully unregistered hooks for matching callback
           
        Example:
        
        .. code-block:: python   
        
           from hydratk.core.masterhead import MasterHead
                              
           
           mh = MasterHead.get_head()
           
           hook = [
                   {'event' : 'htk_on_error', 'callback' : self.my_error_handler, 'unpack_args' : True, 'priority' : const.EVENT_HOOK_PRIORITY - 1}, # will be prioritized        
                   {'event' : 'htk_on_warning', 'callback' : self.my_warning_handler, 'unpack_args' : False}
                  ]            
                      
           mh.register_event_hook(hook)
           mh.unregister_event_hook('htk_on_error') # unregisters all hooks, returns True
           mh.unregister_event_hook('htk_on_warning', self.my_warning_handler) # unregisers matching hook only, returns 1 
           
        """    
                    
        if callback == None:
            result = False
            if event in self._event_hooks:
                del self._event_hooks[event]
                result = True
        else:
            result = 0
            if event in self._event_hooks:
                for priority, hooks in self._event_hooks[event].items():
                    item = 0            
                    for record in hooks:
                        if callable(callback) and record['callback'].__name__ == callback.__name__:
                            del self._event_hooks[event][priority][item]
                            result += 1
                        item += 1
                    
        return result
                    
            
    def replace_event_hook(self, event, callback, record):
        """Methods replaces event listener(s) for specified event.
           
           This method is useful for extending the system functionality
        
        Args:
           event (string): event 
           callback (callable): matching callback
           record (dict) : new callback record            
        
        Returns:          
           int: number of successfully replaced hooks for matching callback
           
        Raises:
           exception: Exception
           
        Example:
        
        .. code-block:: python   
        
           from hydratk.core.masterhead import MasterHead
                              
           
           mh = MasterHead.get_head()
           
           hook = [
                   {'event' : 'htk_on_error', 'callback' : self.my_error_handler, 'unpack_args' : True, 'priority' : const.EVENT_HOOK_PRIORITY - 1}, # will be prioritized        
                   {'event' : 'htk_on_warning', 'callback' : self.my_warning_handler, 'unpack_args' : False}
                  ]            
              
           mh.register_event_hook(hook)
           
           new_record = {
              'callback' : another_warning_handler, 
              'unpack_args' : False
           }
           
           mh.replace_event_hook('htk_on_warning', self.my_warning_handler, new_record) # replaces matching hook only, returns 1 
           
        """  
                     
        if type(record).__name__ != 'dict':
            raise Exception("Invalid record type, dictionary expected")
        if not hasattr(record['callback'], '__call__'):
            raise Exception("Callback replacement is not callable")  
        result = 0
        if event in self._event_hooks:
            for priority, hooks in self._event_hooks[event].items():
                item = 0            
                for rec in hooks:
                    if callable(callback) and rec['callback'].__name__ == callback.__name__:
                        self._event_hooks[event][priority][item] = record
                        result += 1
                    item += 1
        
        return result
            
                    
    def fire_event(self, oevent):
        """Method is processing specified event callbacks.
           
           This method is usable for functionality extending, replacement, notification purposes etc. 
        
        Args:
           oevent (obj): Event object type  hydratk.core.event.Event
        
        Returns:            
           int: number of successfully processed event registered callbacks
           
        Example:
        
        .. code-block:: python
        
           from hydratk.core.masterhead import MasterHead
           from hydratk.core.event import Event
                      
           mh = MasterHead.get_head()
           event_id = 'myprefix_on_something_important'
           oevent = Event('event_id')
           oevent.set_data('alert','I just finished work')
           print('This event was processed %d times' % mh.fire_event(oevent))
           
        """
          
        fe_count = 0
        event_id = oevent.id()                
        before_event_id = '^{0}'.format(event_id.replace('^', ''))         
        after_event_id = '${0}'.format(event_id.replace('$', ''))     
              
        # fire event before requested event is processed if enabled          
        if event_id not in (before_event_id, after_event_id) and event_id in self._event_hooks and oevent.skip_before_hook is False:            
            hbh_ev = event.Event(before_event_id, oevent)                                     
            hbh_ev.set_data('target_event', oevent)                           
            self.fire_event(hbh_ev)
            if hbh_ev.will_run_default() == False:
                return fe_count
        
        # process event and execute registered callback
        if event_id in self._event_hooks and oevent.propagate():                                             
            i = 0
            for _, records in sorted(self._event_hooks[event_id].items(), key=operator.itemgetter(0)):  # _ unused priority
                for record in records:
                    if oevent.propagate() == False: return fe_count
                    cb = record['callback'] 
                    if record['unpack_args']:
                        cb(oevent, *oevent.args())
                    else:
                        cb(oevent)
                    i += 1
                fe_count = i                                    
            
        # fire event after requested event is processed if enabled                        
        if event_id not in (before_event_id, after_event_id) and event_id in self._event_hooks and oevent.propagate() and oevent.skip_after_hook is False:
            hah_ev = event.Event(after_event_id, oevent)                
            hah_ev.set_data('source_event', oevent)        
            self.fire_event(hah_ev)
        
        return fe_count
                
    def apply_command_options(self):
        """Method sets several command options 
        
        Debugging, language
        
        Args:
           none
        
        Returns:            
           void
           
        """
                
        if ('--debug' in self._option_param):
            if (type(self._option_param['--debug'][0]).__name__ == 'str' and self._option_param['--debug'][0].isdigit()):
                if int(self._option_param['--debug'][0]) > 0:
                    self._debug = True
                    self._debug_level = int(self._option_param['--debug'][0])                              
                else:
                    self._debug = False
                self.dmsg('htk_on_debug_info', self._trn.msg('htk_opt_set', 'Debug', self._debug.__str__()), self.fromhere())
                self.dmsg('htk_on_debug_info', self._trn.msg('htk_opt_set', 'Debug level', self._debug_level.__str__()), self.fromhere())            
            else:
                debug_value = self._option_param['--debug'][0].__str__() if self._option_param['--debug'][0] != {} else '' 
                self.dmsg('htk_on_warning', self._trn.msg('htk_opt_ignore', 'Debug', debug_value), self.fromhere())                        
                    
        if ('--language' in self._option_param):               
            if (type(self._option_param['--language'][0]).__name__ == 'str' and self._option_param['--language'][0] != {} and self._option_param['--language'][0] in info.languages):            
                self._language = self._option_param['--language'][0]
                self.dmsg('htk_on_debug_info', self._trn.msg('htk_opt_set', 'Language', self._language), self.fromhere())                            
            else:
                lang_value = self._option_param['--language'][0].__str__() if self._option_param['--language'][0] != {} else ''                 
                self.dmsg('htk_on_warning', self._trn.msg('htk_opt_ignore', 'Debug level', lang_value), self.fromhere())
                                                     
    def get_language(self):
        """Method gets language
        
        Args:
           none
        
        Returns:            
           str: language
           
        """
                
        return self._language
    
    def have_command_action(self): 
        """Method checks if command is set
        
        Args:
           none
        
        Returns:            
           bool: result
           
        """
                       
        return True if self._command != None else False
    
    def get_command_action(self):
        """Method gets command
        
        Args:
           none
        
        Returns:            
           str: command
           
        """
                
        return self._command
    
    '''
    def get_opt_alias_str(self, opt):             
        result = ''
        for a, o in commands.command_opt_alias.items():            
            if (opt == o):
                result = result + a + ','
        return result
    '''    
    
    def service_registered(self, service_name):  
        """Method checks if service is registered
        
        Args:
           service_name (str): service
        
        Returns:            
           bool: result
           
        """
                      
        for service in self._app_service:
            if service_name == service.name: return True
        return False    
        
    def register_service(self, service_name, description, cb):
        """Method registers given service and creates own process
        
        Args:
           service_name (str): service
           description (str): description
           cb (callable): callback
        
        Returns:            
           bool: True
           
        Raises:
           error: TypeError
           error: SystemError
           error: ValueError
           
        """
                
        if not isinstance(service_name, types.basestring) or service_name == '':
            raise TypeError(self._trn.msg('htk_app_service_invalid', service_name))
        if self.service_registered(service_name):
            raise SystemError(self._trn.msg('htk_app_service_registered', service_name))
        if (description == ''): 
            raise ValueError(self._trn.msg('htk_app_service_desc_missing'))
        if not callable(cb):
            raise ValueError(self._trn.msg('htk_cb_not_callable'))
        service_status = multiprocessing.Value('i', const.SERVICE_STATUS_STOPPED)                                
        parent_conn, child_conn = multiprocessing.Pipe() 
        service_starter = self._service_starter              
        service = multiprocessing.Process(target=service_starter, name=service_name, args=(cb, service_status, child_conn))
        service.pipe_conn = parent_conn
        service.service_name = service_name
        service.service_desc = description
        service.service_status = service_status
        self._app_service.append(service)
        self.dmsg('htk_on_debug_info', self._trn.msg('htk_app_service_reg_ok', service_name, description), self.fromhere())
        return True
    
    def unregister_service(self, service_name):
        pass
    
    def start_service(self, service_name):
        """Method starts service
        
        Args:
           service_name (str): service
        
        Returns:            
           bool: result
           
        """
                
        for service in self._app_service:
            if service_name == service.name and not service.is_alive():
                service.start()                
                if service.is_alive():
                    self.dmsg('htk_on_debug_info', self._trn.msg('htk_app_service_start_ok', service_name), self.fromhere())
                    return True
                else:
                    # raise Exception("Failed to start application service "+service_name)    
                    self.dmsg('htk_on_debug_info', self._trn('htk_app_service_start_failed', service_name), self.fromhere())
            else:
                self.dmsg('htk_on_debug_info', self._trn.msg('htk_app_service_start_ok', service_name), self.fromhere())
                    
        return False
    
    def stop_service(self, service_name):        
        pass
    
    def send_service_msg(self, service_name):
        pass
    
    def stop_services(self):
        """Method stops all running services
        
        Service is tried via signal SIGINT first
        If not successful it is stopped via signal SIGKILL
        
        Args:
        
        Returns:            
           void
           
        """
                
        for service in self._app_service:
            if service.pid != None:
                service_name = service.service_name                          
                service.service_status.value = const.SERVICE_STATUS_STOPPED                
                os.kill(int(service.pid), signal.SIGINT)
                self.dmsg('htk_on_debug_info', self._trn.msg('htk_app_service_stop', service_name), self.fromhere())
                service.join(const.PROCESS_JOIN_TIMEOUT)
                if service.is_alive():
                    self.dmsg('htk_on_debug_info', self._trn.msg('htk_app_service_stop_failed', service_name), self.fromhere())
                    self.dmsg('htk_on_debug_info', self._trn.msg('htk_app_service_stop_hard', service_name), self.fromhere()) 
                    os.kill(int(service.pid), signal.SIGKILL)
            else: self.dmsg('htk_on_debug_info', self._trn.msg('htk_app_service_inactive_skip', service.service_name), self.fromhere())
                
                    
    def init_core_threads(self): 
        """Method initializes threads according to configuration
        
        Args:
           none
        
        Returns:            
           void
           
        """
                
        i = 1       
        while i <= self._num_threads:
            self.add_core_thread(i)
            i = i + 1        
    
    def destroy_core_threads(self):
        """Method destroys threads
        
        Args:
           none
        
        Returns:            
           void
           
        """
                
        for thread in self._thr:
            name = thread.name
            thread.status.value = const.CORE_THREAD_EXIT
            self.dmsg('htk_on_debug_info', self._trn.msg('htk_cthread_destroy', name), self.fromhere())
            thread.join()
                
    def add_core_thread(self, i=None):  
        """Method adds new thread to the pool
        
        Args:
           i (int): thread id
        
        Returns:            
           void
           
        """        
              
        nexti = len(self._thr) + 1 if i == None else i
        status = multiprocessing.Value('i', const.CORE_THREAD_WORK)
        action_status = multiprocessing.Value('i', const.CORE_THREAD_ACTION_NONE)  
        is_alive_check = multiprocessing.Value('d', time.time())             
        parent_conn, child_conn = multiprocessing.Pipe()               
        current = multiprocessing.Process(target=self._c_worker, name=nexti, args=(nexti, status, action_status, child_conn, is_alive_check))
        
        current.last_ping_response = 0
        current.next_check_time = time.time() + const.CORE_THREAD_PING_TIME
        current.response_alert_level = 0
        current.status = status  
        current.action_status = action_status      
        current.pipe_conn = parent_conn
        current.is_alive_check = is_alive_check
        current.num = nexti                        
        self._thr.append(current) 
        self.dmsg('htk_on_debug_info', self._trn.msg('htk_cthread_init', nexti), self.fromhere())
        current.start()
    
    def get_thrid(self):
        """Method gets thread id (name)
        
        Args:
           none
        
        Returns:            
           str: id
           
        """
                
        return '0' if multiprocessing.current_process().name == 'MainProcess' else multiprocessing.current_process().name
        
    def create_ext_skel(self):
        """Method creates extension skeleton
        
        Skeleton contains extension module, configuration, langtexts, installation
        In default (non-interactive) mode the skeleton is created from template in ~/hydratk directory
        In interactive mode the skeleton wizard asks the user for several data (path, name, author, ...)
        
        Command line options - --force, --interactive, --ext-skel-path
        
        Args:
           none
        
        Returns:            
           bool: result
           
        """
                
        from hydratk.core import template;
        from os.path import expanduser
        default_install_path = "{0}/hydratk".format(expanduser("~"));
        result               = False
        force_cmd            = True if CommandlineTool.get_input_option('force') == True else False
        interactive          = True if CommandlineTool.get_input_option('interactive') == True else False
        ext_skel_path        = CommandlineTool.get_input_option('ext-skel-path')         
        ext_skel_path        = default_install_path if ext_skel_path in (False,'') else ext_skel_path
        '''Default data'''
        ext_name     = template.extension_default_user_data['ext_name']
        ext_ucname   = template.extension_default_user_data['ext_ucname'] 
        ext_desc     = template.extension_default_user_data['ext_desc']
        ext_year     = template.extension_default_user_data['ext_year']
        author_name  = template.extension_default_user_data['author_name']
        author_email = template.extension_default_user_data['author_email']
        ext_license  = template.extension_default_user_data['ext_license']
        
        if interactive:
            try:
                print('****************************************')
                print('*   Extension skeleton create wizard   *')
                print('****************************************')
                print('This wizard will create HydraTK extension development skeleton in following 6 steps')
                print('Hit ENTER for default value, CTRL + C to exit')
                
                print('1. Enter the directory, where the extension structure will be created');
                read_ext_skel_path = raw_input("[{0}]:".format(default_install_path))
                ext_skel_path = read_ext_skel_path if len(read_ext_skel_path) > 0 else ext_skel_path
                print("Extension skeleton directory set to: %s" % ext_skel_path)
                
                print('2. Enter the extension module name, must be one word short unique string');
                read_ext_name = raw_input("[{0}]:".format(template.extension_default_user_data['ext_name']))
                ext_name = read_ext_name.lower() if len(read_ext_name) > 0 and read_ext_name.isalpha() else template.extension_default_user_data['ext_name']
                ext_ucname = ext_name.capitalize()
                print("Extension module name set to: %s" % ext_name)
                
                print('3. Enter the extension description');
                read_ext_desc = raw_input("[{0}]:".format(template.extension_default_user_data['ext_desc']))
                ext_desc = read_ext_desc if len(read_ext_desc) > 0 else template.extension_default_user_data['ext_desc']
                print("Extension description set to: %s" % ext_desc)
                
                print('4. Enter the extension author name');
                read_author_name = raw_input("[{0}]:".format(template.extension_default_user_data['author_name']))
                author_name = read_author_name if len(read_author_name) > 0 else template.extension_default_user_data['author_name']
                print("Extension author name set to: %s" % author_name)
                
                print('5. Enter the extension author email');
                read_author_email = raw_input("[{0}]:".format(template.extension_default_user_data['author_email']))
                author_email = read_author_email if len(read_author_email) > 0 else template.extension_default_user_data['author_email']
                print("Extension author email set to: %s" % author_email)
                
                print('6. Select extension usage and distribution license, currently supported are: BSD'); #TODO put the dynamic listing here
                read_ext_license = raw_input("[{0}]:".format(template.extension_default_user_data['ext_license']))
                ext_license = read_ext_license if len(read_ext_license) > 0 and read_ext_license in template.extension_license else template.extension_default_user_data['ext_license']
                print("Extension usage and distribution license set to: %s" % ext_license)
                                
            except:
                print("\nInterrupted.")
                exit(1);
        
        if not os.path.exists(ext_skel_path):
            try:
                os.makedirs(ext_skel_path)
            except:
                print("Cannot create directory %s" % ext_skel_path)
                                        
        if os.access(ext_skel_path, os.W_OK):            
            for create_path_str in template.extension_dir_struct:
                try:
                    create_path = ("{0}/{1}".format(ext_skel_path,create_path_str)).format(extension=ext_name)
                    if not os.path.exists(create_path):
                        self.dmsg('htk_on_debug_info', "Creating path %s" % create_path, self.fromhere())
                        os.makedirs(create_path)
                except:
                    raise
                                            
            from hydratk.lib.system.fs import file_put_contents
                        
            for create_package_init_file_str in template.extension_package_files:
                try:
                    create_package_init_file = ("{0}/{1}".format(ext_skel_path,create_package_init_file_str)).format(extension=ext_name)                    
                    self.dmsg('htk_on_debug_info', "Creating package init file %s" % create_package_init_file, self.fromhere())
                    file_put_contents(create_package_init_file,template.extension_package_init_content)
                except:
                    raise
            
            try:
                ext_config_file = ("{0}/{1}".format(ext_skel_path, template.extension_data_files['ext.config'])).format(extension=ext_name)                    
                self.dmsg('htk_on_debug_info', "Creating config file %s" % ext_config_file, self.fromhere())
                config_file_data = template.extension_config.format(uc_extension=ext_ucname, extension=ext_name)
                file_put_contents(ext_config_file,config_file_data)
                
                ext_module_file = ("{0}/{1}".format(ext_skel_path, template.extension_data_files['ext.module'])).format(extension=ext_name)                    
                self.dmsg('htk_on_debug_info', "Creating extension module file %s" % ext_module_file, self.fromhere())
                ext_module_file_data = template.extension.format(
                                                                   ext_ucname=ext_ucname, 
                                                                   extension=ext_name,
                                                                   author_name=author_name,
                                                                   author_email=author_email,
                                                                   ext_desc=ext_desc,
                                                                   ext_year=ext_year
                                                                )                                                                
                file_put_contents(ext_module_file,ext_module_file_data)
                
                ext_bootstrapper_file = ("{0}/{1}".format(ext_skel_path, template.extension_data_files['ext.bootstrapper'])).format(extension=ext_name)                    
                self.dmsg('htk_on_debug_info', "Creating extension bootstrapper file %s" % ext_module_file, self.fromhere())
                ext_bootstrapper_file_data = template.extension_bootstrapper.format(
                                                                   extension=ext_name,
                                                                   author_name=author_name,
                                                                   author_email=author_email
                                                                )                                                                
                file_put_contents(ext_bootstrapper_file,ext_bootstrapper_file_data)                
                
                ext_translation_en_messages_file = ("{0}/{1}".format(ext_skel_path, template.extension_data_files['ext.translation.en.messages'])).format(extension=ext_name)                    
                self.dmsg('htk_on_debug_info', "Creating extension translation English messages file %s" % ext_translation_en_messages_file, self.fromhere())
                ext_translation_en_messages_file_data = template.extension_translation_en_messages.format(
                                                                   ext_ucname=ext_ucname,
                                                                   extension=ext_name,
                                                                   author_name=author_name,
                                                                   author_email=author_email                                                                                                                                       
                                                                )                                                                
                file_put_contents(ext_translation_en_messages_file, ext_translation_en_messages_file_data)
                
                ext_translation_cs_messages_file = ("{0}/{1}".format(ext_skel_path, template.extension_data_files['ext.translation.cs.messages'])).format(extension=ext_name)                    
                self.dmsg('htk_on_debug_info', "Creating extension translation Czech messages file %s" % ext_translation_cs_messages_file, self.fromhere())
                ext_translation_cs_messages_file_data = template.extension_translation_cs_messages.format(
                                                                   ext_ucname=ext_ucname, 
                                                                   extension=ext_name,
                                                                   author_name=author_name,
                                                                   author_email=author_email                                                                  
                                                                )                                                                
                file_put_contents(ext_translation_cs_messages_file, ext_translation_cs_messages_file_data)
                
                ext_translation_en_help_file = ("{0}/{1}".format(ext_skel_path, template.extension_data_files['ext.translation.en.help'])).format(extension=ext_name)                    
                self.dmsg('htk_on_debug_info', "Creating extension translation English help file %s" % ext_translation_en_help_file, self.fromhere())
                ext_translation_en_help_file_data = template.extension_translation_en_help.format(
                                                                   ext_ucname=ext_ucname,
                                                                   extension=ext_name,
                                                                   author_name=author_name,
                                                                   author_email=author_email                                                                                                                                       
                                                                )                                                                
                file_put_contents(ext_translation_en_help_file, ext_translation_en_help_file_data)
                
                ext_translation_cs_help_file = ("{0}/{1}".format(ext_skel_path, template.extension_data_files['ext.translation.cs.help'])).format(extension=ext_name)                    
                self.dmsg('htk_on_debug_info', "Creating extension translation Czech help file %s" % ext_translation_cs_help_file, self.fromhere())
                ext_translation_cs_help_file_data = template.extension_translation_cs_help.format(
                                                                   ext_ucname=ext_ucname,
                                                                   extension=ext_name,
                                                                   author_name=author_name,
                                                                   author_email=author_email                                                                                                                                       
                                                                )                                                                
                file_put_contents(ext_translation_cs_help_file, ext_translation_cs_help_file_data)
                
                ext_setup_py_file = ("{0}/{1}".format(ext_skel_path, template.extension_data_files['ext.setup.py'])).format(extension=ext_name)                    
                self.dmsg('htk_on_debug_info', "Creating extension setup file %s" % ext_setup_py_file, self.fromhere())
                ext_setup_py_file_data = template.extension_setup_py.format(
                                                                   extension=ext_name,
                                                                   ext_ucname=ext_ucname,                                                                
                                                                   author_name=author_name,
                                                                   author_email=author_email,
                                                                   ext_desc=ext_desc,
                                                                   dir='dir',
                                                                   file='file'                                                                                                                                  
                                                                )                                                                
                file_put_contents(ext_setup_py_file, ext_setup_py_file_data)
                
                ext_setup_cfg_file = ("{0}/{1}".format(ext_skel_path, template.extension_data_files['ext.setup.cfg'])).format(extension=ext_name)                    
                self.dmsg('htk_on_debug_info', "Creating extension additional setup config file %s" % ext_setup_cfg_file, self.fromhere())                                                                        
                file_put_contents(ext_setup_cfg_file, template.extension_setup_cfg)
                
                ext_license_file = ("{0}/{1}".format(ext_skel_path, template.extension_data_files['ext.license'])).format(extension=ext_name)                    
                self.dmsg('htk_on_debug_info', "Creating extension license file %s" % ext_license_file, self.fromhere())                                                                        
                file_put_contents(ext_license_file, template.extension_license[ext_license].format(ext_year=ext_year, author_name=author_name, author_email=author_email))
                
                ext_readme_file = ("{0}/{1}".format(ext_skel_path, template.extension_data_files['ext.readme'])).format(extension=ext_name)                    
                self.dmsg('htk_on_debug_info', "Creating extension readme file %s" % ext_readme_file, self.fromhere())                                                                        
                file_put_contents(ext_readme_file, template.extension_readme_rst.format(ext_ucname=ext_ucname,ext_desc=ext_desc))
                
                ext_requirements_file = ("{0}/{1}".format(ext_skel_path, template.extension_data_files['ext.requirements'])).format(extension=ext_name)                    
                self.dmsg('htk_on_debug_info', "Creating extension requirements file %s" % ext_requirements_file, self.fromhere())                                                                        
                file_put_contents(ext_requirements_file, template.extension_requirements)
                
                ext_manifest_file = ("{0}/{1}".format(ext_skel_path, template.extension_data_files['ext.manifest'])).format(extension=ext_name)                    
                self.dmsg('htk_on_debug_info', "Creating extension manifest file %s" % ext_manifest_file, self.fromhere())                                                                        
                file_put_contents(ext_manifest_file, template.extension_manifest)                
                
                result = True
                
            except:
                raise
                
        else:
            print("Cannot create extension skeleton in path %s" % ext_skel_path)
            print(os.access(ext_skel_path, os.W_OK))
        
        
        print("Completed.")
        return result  
            
    def create_lib_skel(self):
        """Method creates library skeleton
        
        Skeleton contains extension module, installation
        In default (non-interactive) mode the skeleton is created from template in ~/hydratk directory
        In interactive mode the skeleton wizard asks the user for several data (path, name, author, ...)
        
        Command line options - --force, --interactive, --lib-skel-path
        
        Args:
           none
        
        Returns:            
           bool: result
           
        """
                
        from hydratk.core import template;
        from os.path import expanduser
        default_install_path = "{0}/hydratk".format(expanduser("~"));
        result               = False
        force_cmd            = True if CommandlineTool.get_input_option('force') == True else False
        interactive          = True if CommandlineTool.get_input_option('interactive') == True else False
        lib_skel_path        = CommandlineTool.get_input_option('lib-skel-path')         
        lib_skel_path        = default_install_path if lib_skel_path in (False,'') else lib_skel_path
        '''Default data'''
        lib_name     = template.lib_default_user_data['lib_name']
        lib_ucname   = template.lib_default_user_data['lib_ucname'] 
        lib_desc     = template.lib_default_user_data['lib_desc']
        lib_year     = template.lib_default_user_data['lib_year']
        author_name  = template.lib_default_user_data['author_name']
        author_email = template.lib_default_user_data['author_email']
        lib_license  = template.lib_default_user_data['lib_license']
        
        if interactive:
            try:
                print('**************************************')
                print('*   Library skeleton create wizard   *')
                print('**************************************')
                print('This wizard will create HydraTK shared library development skeleton in following 6 steps')
                print('Hit ENTER for default value, CTRL + C to exit')
                
                print('1. Enter the directory, where the library structure will be created');
                read_lib_skel_path = raw_input("[{0}]:".format(default_install_path))
                lib_skel_path = read_lib_skel_path if len(read_lib_skel_path) > 0 else lib_skel_path
                print("Library skeleton directory set to: %s" % lib_skel_path)
                
                print('2. Enter the library module name, must be one word short unique string');
                read_lib_name = raw_input("[{0}]:".format(template.lib_default_user_data['lib_name']))
                lib_name = read_lib_name.lower() if len(read_lib_name) > 0 and read_lib_name.isalpha() else template.lib_default_user_data['lib_name']
                lib_ucname = lib_name.capitalize()
                print("Library module name set to: %s" % lib_name)
                
                print('3. Enter the library description');
                read_lib_desc = raw_input("[{0}]:".format(template.lib_default_user_data['lib_desc']))
                lib_desc = read_lib_desc if len(read_lib_desc) > 0 else template.lib_default_user_data['lib_desc']
                print("Library description set to: %s" % lib_desc)
                
                print('4. Enter the lib author name');
                read_author_name = raw_input("[{0}]:".format(template.lib_default_user_data['author_name']))
                author_name = read_author_name if len(read_author_name) > 0 else template.lib_default_user_data['author_name']
                print("lib author name set to: %s" % author_name)
                
                print('5. Enter the library author email');
                read_author_email = raw_input("[{0}]:".format(template.lib_default_user_data['author_email']))
                author_email = read_author_email if len(read_author_email) > 0 else template.lib_default_user_data['author_email']
                print("Library author email set to: %s" % author_email)
                
                print('6. Select lib usage and distribution license, currently supported are: BSD'); #TODO put the dynamic listing here
                read_lib_license = raw_input("[{0}]:".format(template.lib_default_user_data['lib_license']))
                lib_license = read_lib_license if len(read_lib_license) > 0 and read_lib_license in template.lib_license else template.lib_default_user_data['lib_license']
                print("Library usage and distribution license set to: %s" % lib_license)
                                
            except:
                print("\nInterrupted.")
                exit(1);
        
        if not os.path.exists(lib_skel_path):
            try:
                os.makedirs(lib_skel_path)
            except:
                print("Cannot create directory %s" % lib_skel_path)
                                        
        if os.access(lib_skel_path, os.W_OK):            
            for create_path_str in template.lib_dir_struct:
                try:
                    create_path = ("{0}/{1}".format(lib_skel_path,create_path_str)).format(lib_name=lib_name)
                    if not os.path.exists(create_path):
                        self.dmsg('htk_on_debug_info', "Creating path %s" % create_path, self.fromhere())
                        os.makedirs(create_path)
                except:
                    raise
                                            
            from hydratk.lib.system.fs import file_put_contents
            
            for create_package_init_file_str in template.lib_package_files:
                try:
                    create_package_init_file = ("{0}/{1}".format(lib_skel_path,create_package_init_file_str)).format(lib_name=lib_name)                    
                    self.dmsg('htk_on_debug_info', "Creating package init file %s" % create_package_init_file, self.fromhere())
                    file_put_contents(create_package_init_file,template.lib_package_init_content)
                except:
                    raise
            
            try:                                
                lib_module_file = ("{0}/{1}".format(lib_skel_path, template.lib_data_files['lib.module'])).format(lib_name=lib_name)                    
                self.dmsg('htk_on_debug_info', "Creating library module file %s" % lib_module_file, self.fromhere())
                lib_module_file_data = template.library.format(
                                                                   lib_ucname=lib_ucname, 
                                                                   lib_name=lib_name,
                                                                   author_name=author_name,
                                                                   author_email=author_email,
                                                                   lib_desc=lib_desc
                                                                  
                                                                )                                                                
                file_put_contents(lib_module_file,lib_module_file_data)                
                
                lib_setup_py_file = ("{0}/{1}".format(lib_skel_path, template.lib_data_files['lib.setup.py'])).format(lib_name=lib_name)                    
                self.dmsg('htk_on_debug_info', "Creating library setup file %s" % lib_setup_py_file, self.fromhere())
                lib_setup_py_file_data = template.lib_setup_py.format(
                                                                   lib_name=lib_name,
                                                                   lib_ucname=lib_ucname,                                                                
                                                                   author_name=author_name,
                                                                   author_email=author_email,
                                                                   lib_desc=lib_desc                                                                                                                                       
                                                                )                                                                
                file_put_contents(lib_setup_py_file, lib_setup_py_file_data)
                
                lib_setup_cfg_file = ("{0}/{1}".format(lib_skel_path, template.lib_data_files['lib.setup.cfg'])).format(lib_name=lib_name)                    
                self.dmsg('htk_on_debug_info', "Creating library additional setup config file %s" % lib_setup_cfg_file, self.fromhere())                                                                        
                file_put_contents(lib_setup_cfg_file, template.lib_setup_cfg)
                
                lib_license_file = ("{0}/{1}".format(lib_skel_path, template.lib_data_files['lib.license'])).format(lib_name=lib_name)                    
                self.dmsg('htk_on_debug_info', "Creating lib license file %s" % lib_license_file, self.fromhere())                                                                        
                file_put_contents(lib_license_file, template.lib_license[lib_license].format(ext_year=lib_year, author_name=author_name, author_email=author_email))
                
                lib_readme_file = ("{0}/{1}".format(lib_skel_path, template.lib_data_files['lib.readme'])).format(lib_name=lib_name)                    
                self.dmsg('htk_on_debug_info', "Creating library readme file %s" % lib_readme_file, self.fromhere())                                                                        
                file_put_contents(lib_readme_file, template.lib_readme_rst.format(lib_ucname=lib_ucname,lib_desc=lib_desc))
                
                lib_requirements_file = ("{0}/{1}".format(lib_skel_path, template.lib_data_files['lib.requirements'])).format(lib_name=lib_name)                    
                self.dmsg('htk_on_debug_info', "Creating library requirements file %s" % lib_requirements_file, self.fromhere())                                                                        
                file_put_contents(lib_requirements_file, template.lib_requirements)
                
                lib_manifest_file = ("{0}/{1}".format(lib_skel_path, template.lib_data_files['lib.manifest'])).format(lib_name=lib_name)                    
                self.dmsg('htk_on_debug_info', "Creating library manifest file %s" % lib_manifest_file, self.fromhere())                                                                        
                file_put_contents(lib_manifest_file, template.lib_manifest)                                
                
                result = True
                
            except:
                raise
                
        else:
            print("Cannot create library skeleton in path %s" % lib_skel_path)
            print(os.access(lib_skel_path, os.W_OK))
        
        
        print("Completed.")
        return result  
            
    def async_fn_ex(self, fn_id, *args, **kwargs):
        """Method sends functionality hook in asynchronous way as message
        
        Args:
           fn_id (str): functionality
           args (args): arguments
           kwargs (kwargs): key value arguments
        
        Returns:            
           void
           
        """
                
        if fn_id is None or fn_id == '':
            raise TypeError("fn_id: expected nonempty string")
        if fn_id not in self._async_fn_ex:
            raise KeyError("fn_id: {0} is not registered".format(fn_id))
        thr_id = self.get_thrid()
        msg = {
           'type' : "async_fn_ex",
           'from' : 'htk_obsrv@core.raptor',
           'to'   : 'any@core.raptor',
           'data' : {
                     'fn_id'  : fn_id,
                     'args'   : args,
                     'kwargs' : kwargs
                    }
        
        }
        self.send_msg(msg)        
        
    def send_msg(self, msg):
        """Method send message to queue

        Args:
           msg (obj): message
        
        Returns:            
           void
           
        """
                
        return self._send_msg(msg)
            
    def async_ext_fn(self, callback, result_callback, *args, **kwargs ):
        """Method send extension hook in asynchronous way as message
        
        Args:
           callback (tuple): callback
           result_callback (obj): str or tuple, callback
           args (args): arguments
           kwargs (kwargs): key value arguments
        
        Returns:            
           str: ticket id
           
        Raises:
           error: TypeError
           error: KeyError
           
        """
                
        if type(callback).__name__ != 'tuple': 
            raise TypeError("callback: tuple expected")
        obj, meth = callback
        if type(obj).__name__ not in ('Extension', 'str'):            
            raise TypeError("callback object: expected instance or str, got {0}".format(type(obj).__name__))
        if type(meth).__name__ != 'str' or meth == '':
            raise TypeError("callback method: expected nonempty str")        
        ext_name = obj.get_ext_name() if type(obj).__name__ == 'Extension' else obj
        if ext_name not in self._ext:
            raise KeyError("callback: undefined extension name: {0}".format(ext_name))
        
        result_obj  = None
        result_meth = None
        if result_callback is not None:
            if type(result_callback).__name__ not in ('str','tuple'):
                raise TypeError("result_callback object: expected str or tuple")
            if type(result_callback).__name__ == 'str':
                if result_callback == '':
                    raise TypeError("result_callback: empty string not acceptable")
                if result_callback not in self._async_fn: #fn_id
                    raise KeyError("result_callback fn_id: {0} is not registered".format(result_callback)) 
            else: #tuple
                pass
            
        ticket_id = self._new_async_ticket_id()
        self._new_async_ticket(ticket_id)
        msg = {
           'type' : "async_ext_fn",
           'from' : 'htk_obsrv@core.raptor',
           'to'   : 'any@core.raptor',
           'data' : {
                     'ticket_id' : ticket_id,
                     'callback' : {
                                   'ext_name'  : ext_name,
                                   'method'    : meth, 
                                   'args'      : args,
                                   'kwargs'    : kwargs
                                  }
                    }
        
        } 
        self.send_msg(msg)
        return ticket_id  
    
    def get_async_ticket_content(self, ticket_id):
        """Method gets ticket content
        
        Args:
           ticket_id (str): ticket
        
        Returns:            
           obj: content
           
        Raises:
           error: KeyError
           error: TypeError
           
        """
                
        if ticket_id is not None and ticket_id != '':
            if ticket_id in self._async_fn_tickets:
                return self._async_fn_tickets[ticket_id]
            raise KeyError("Ticket id: {0} doesn't exists".format(ticket_id))
        else:
            raise TypeError("Invalid ticket_id: {0}".format(type(ticket_id).__name__))
    
    def update_async_ticket_content(self, ticket_id, data):
        pass
            
    def async_ticket_completed(self, ticket_id):
        """Method checks if ticket processing is completed
        
        Args:
           ticket_id (str): ticket
        
        Returns:            
           bool: result
           
        Raises:
           error: KeyError
           error: TypeError
           
        """
                
        if ticket_id is not None and ticket_id != '':
            if ticket_id in self._async_fn_tickets:
                return self._async_fn_tickets[ticket_id]['completed']
            raise KeyError("Ticket id: {0} doesn't exists".format(ticket_id))
        else:
            raise TypeError("Invalid ticket_id: {0}".format(type(ticket_id).__name__))
        
    def delete_async_ticket(self, ticket_id):
        """Method deletes ticket
        
        Args:
           ticket_id (str): ticket
        
        Returns:            
           void
           
        """
                
        self._delete_async_ticket(ticket_id)
        
    def register_async_fn_ex(self, fn_id, callback, result_callback=None):  
        """Method registers functionality hook in asynchronous way
        
        Args:
           fn_id (str): functionality hook
           callback (callable): callback
           result_callback (callable): result callback
        
        Returns:            
           bool: True
           
        Raises:
           error: TypeError
           
        """
                      
        if fn_id is None or fn_id == '':
            raise TypeError("fn_id: expected nonempty string")        
        res_cb = None
        if result_callback is not None:
            if callable(result_callback) and type(result_callback).__name__ in ('function','instancemethod'):
                res_cb = {}
                res_cb['class_inst'] = None
                res_cb['func']   = result_callback
                if type(result_callback).__name__ == 'instancemethod':
                    res_cb['class_inst'] = result_callback.im_self
                    res_cb['func']   = result_callback.im_func
            else:
                raise TypeError('result_callback: expected callable function or instancemethod')
        if callable(callback) and type(callback).__name__ in ('function','instancemethod'):
            cb               = {}
            cb['class_inst'] = None
            cb['func']   = callback
            if type(callback).__name__ == 'instancemethod':                
                cb['class_inst'] = callback.im_self
                cb['func']   = callback.im_func
            self._async_fn_ex[fn_id] = {
                                          'callback' : cb,
                                          'result_callback' : res_cb 
                                       }            
            return True
        else:
            raise TypeError('callback: expected callable function or instancemethod')
    
    def bridge_fn_cb(self, fn_id_src, fn_id_dest):
        pass
    
    def reg_fn_cb(self, fn_id, callback, options=None):
        """Method is registering callback with specified fn_id.
           
           This method is usable for functionality extending, replacement. 
        
        Args:
           fn_id (str): functionality id
           callback (callable): callback
           options: not used
                   
        Returns:            
           bool: True
           
        Raises:
           error: TypeError
        
        """
        
        if fn_id is None or fn_id == '':
            raise TypeError("fn_id: expected nonempty string")
        if callable(callback):
            self._fn_callback[fn_id] = callback
            return True
        else:
            raise TypeError('callback: expected callable')
        #if self._run_mode >= const.CORE_RUN_MODE_PP_APP:
        
    def register_async_fn(self, fn_id, callback):
        """Method registers functionality hook in asynchronous way
        
        Args:
           fn_id (str): functionality hook
           callback (callable): callback
        
        Returns:            
           bool: True
           
        Raises:
           error: TypeError
           
        """   
             
        if fn_id is None or fn_id == '':
            raise TypeError("fn_id: expected nonempty string")
        if callable(callback):
            self._async_fn[fn_id] = callback
            return True
        else:
            raise TypeError('callback: expected callable')
        
    def get_ext(self, extension_name):
        """Method gets extensions
        
        Args:
           extension_name (str): extension
        
        Returns:            
           obj: Extension
           
        Raises:
           error: IndexError
           error: TypeError
           
        """
                
        if type(extension_name).__name__ == 'str' and extension_name != '':
            if extension_name in self._ext:                
                return self._ext[extension_name]                
            else:
                raise IndexError("Undefined extension {0}".format(extension_name))
        else:
            raise TypeError("Extension name string expected")
        