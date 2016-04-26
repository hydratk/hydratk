# -*- coding: utf-8 -*-
"""This code is a part of Hydra framework

.. module:: core.propertyhead
   :platform: Unix
   :synopsis: HydraTK properties module
.. moduleauthor:: Petr Czaderna <pc@headz.cz>

"""

from hydratk.core import const
from hydratk.translation.core import info

class PropertyHead(object):
    
    @property
    def current_async_ticket_id(self):
        return self._current_async_ticket_id
    
    @property
    def async_fn_tickets(self):
        return self._async_fn_tickets
    
    @async_fn_tickets.setter
    def async_fn_tickets(self, data):
        self._async_fn_tickets = data
           
    @property
    def fn_cb_shared(self):
        return self._fn_cb_shared
    
    @fn_cb_shared.setter
    def fn_cb_shared(self, d):
        self._fn_cb_shared = d
    
    @property
    def cbm(self):
        return self._cbm #CallbackManager instance
        
    @property
    def cli_cmdopt_profile(self):
        return self._opt_profile
    
    @property
    def cfg(self):
        return self._config
    
    @property
    def debug(self):
        return self._debug
    
    @property
    def debug_level(self):
        return self._debug_level
    
    @property
    def ext_cfg(self):
        return self._config['Extensions']
    
    @property
    def lang(self):
        return self._language
    
    @lang.setter
    def lang(self,language):
        self._language = language if language in info.languages else const.DEFAULT_LANGUAGE
        
    @property
    def runlevel(self):
        return self._runlevel
    
    @property
    def run_mode(self):
        return self._run_mode
    
    @run_mode.setter
    def run_mode(self, mode):
        if mode in(
                   const.CORE_RUN_MODE_PP_APP,
                   const.CORE_RUN_MODE_PP_APP,
                   const.CORE_RUN_MODE_PP_DAEMON                   
                   ):
            self._run_mode = mode