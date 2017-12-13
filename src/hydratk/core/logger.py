# -*- coding: utf-8 -*-
"""HydraTK core integrated logging features

.. module:: core.logger
   :platform: Unix
   :synopsis: HydraTK core integrated logging features
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import sys
import os
import hydratk.lib.system.config as syscfg
from hydratk.lib.system.fs import file_put_contents
from hydratk.core import const


class Logger(object):
    """Class Logger
    """
    _error_info           = const.ERROR_INFO
    _warning_info         = const.WARNING_INFO
    _exception_info       = const.EXCEPTION_INFO
    _log_profiles         = {}
    _log_default_profiles = {
        'debug' : [ 
           {
            'log_type'      : 'debug',   
            'level'         : const.DEBUG_LEVEL,
            'channel'       : const.DEBUG_CHANNEL, 
            'output_handler': 'screen',
            'format'        : '{timestamp} DEBUG({level}): {callpath}.{func}:[{thrid}]: {msg}',
            'term_color'    : '#CC6600'                
           }
        ],
        'error' : [ 
           {
            'log_type'      : 'error',   
            'output_handler': 'screen',
            'format'        : '{timestamp} ERROR: {callpath}.{func}:[{thrid}]: {msg}',
            'term_color'    : '#ff0000'                
           }
        ],
        'exception' : [ 
           {
            'log_type'      : 'exception',   
            'output_handler': 'screen',
            'format'        : "{timestamp} EXCEPTION: {extype}:[{thrid}]: {msg}\n{trace}",
            'term_color'    : '#800080'                
           }
        ],
        'warning' : [ 
           {
            'log_type'      : 'warning',   
            'output_handler': 'screen',
            'format'        : '{timestamp} WARNING: {callpath}.{func}:[{thrid}]: {msg}',
            'term_color'    : '#ffff00'                
           }
        ]                
    } 
    _log_handlers         = {}
    _log_formaters        = {}  
    _log_event2log_type   = {
       'htk_on_debug_info'         : 'debug',
       'htk_on_error'              : 'error',
       'htk_on_warning'            : 'warning',
       'htk_on_uncaught_exception' : 'exception'            
    }
    
    _emulate_print = True

    def spout(self, data):
        """Method prints data

        Args:     
           data (str): data

        Returns:

        """

        lf = "\n" if self._emulate_print == True else ""
        sys.stdout.write(data + lf)
        sys.stdout.flush()
        
    def _log_init_handlers(self):
        """Method initialize default Logger output handlers

        Args:     
           
        Returns:
          void
          
        """        
        self._log_handlers = {}
        self._log_handlers['screen']  = self._log_screen_handler
        self._log_handlers['logfile'] = self._log_file_handler
    
    
    def _log_init_msg_formaters(self):
        """Method initialize default Logger output formaters

        Args:     
           
        Returns:
          void
          
        """        
        self._log_formaters = {}
        self._log_formaters['debug']     = self.dbg_format_msg
        self._log_formaters['error']     = self.dbg_format_msg
        self._log_formaters['warning']   = self.dbg_format_msg
        self._log_formaters['exception'] = self.dbg_format_exception_msg
        #self._log_formaters['warning']  = self._log_file_handler        
            
    def _log_init_profiles(self):
        """Method loads active Logger profiles from config

        Args:     
           data (str): data

        Returns:
           void

        """        
        self._log_profiles = {}  #reset settings        
        for profile_name, profile in self._config['Logger'].items():           
            if profile['enabled'] == 1:                 
                if 'format' in profile and 'format_cache' in profile and profile['format_cache'] == 1:                      
                    profile['format'] = self._config_mp.parse(profile['format']) #interpreting macros an caching macro results                                    
                if not self.register_log_output_profile(profile['log_type'], profile):
                    raise ValueError('Logger failed to register config profile: {0}'.format(profile_name)) 
    
        self.dmsg("Initialized logger profiles") 
        
    def _log_event(self, ev, *args):
        """Method is transforming event data through the Logger profiles

        Args:     
           ev (obj): Event object
           *args (mixed) : unpacked Event parameters

        Returns:
           bool: result

        """               
        result = False        
        if ev.id in self._log_event2log_type:
            log_type = self._log_event2log_type[ev.id]
            log_profiles = self._log_profiles if len(self._log_profiles) > 0 else self._log_default_profiles
            
            if log_type in log_profiles: #if there's profile registered for log_type                
                for profile in log_profiles[log_type]:                
                    self._log_handlers[profile['output_handler']](profile, *args)
                    
                result = True #processing finished
        return result        
                                
        #there's no handler mapping for input event
          
    def _log_screen_handler(self, profile, *args):
        """Method is default screen output handler implementation

        Args:     
           profile (dict): logger dictionary profile
           *args (mixed) : unpacked message parameters

        Returns:
           bool: result

        """                     
        msg = self._log_formaters[profile['log_type']](profile, *args)
        if type(msg).__name__ == 'str' and msg != '':
            print(msg)
            sys.stdout.flush()

    
    def _log_file_handler(self, profile, *args): 
        """Method is default logfile output handler implementation

        Args:     
           profile (dict): logger dictionary profile
           *args (mixed) : unpacked message parameters

        Returns:
           bool: result

        """                             
        if 'log_file' in profile and profile['log_file'] != '':
            log_file = self._config_mp.parse(profile['log_file'])
            log_dir = os.path.dirname(log_file)
            w_ready = False
            if os.path.isdir(log_dir) == False:
                if 'missing_dir' in profile and profile['missing_dir'] == 'autocreate':
                    try:
                        os.makedirs(log_dir)
                        w_ready = True
                    except OSError:
                        #warning unable to create directory, loggin to enabled
                        pass
            else:
                w_ready = True
            if w_ready:
                msg = self._log_formaters[profile['log_type']](profile, *args)
                if type(msg).__name__ == 'str' and msg != '':       
                    file_put_contents(log_file, msg, mode='a')
                        
        else:
            pass
            #todo warning logfile not configured
        
    
    def log_rotate(self, source, dest, zip=True):        
        os.rename(source, dest)
        f_in = open(dest, 'rb')
        f_out = gzip.open("%s.gz" % dest, 'wb')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
        os.remove(dest) 