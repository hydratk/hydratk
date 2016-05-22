# -*- coding: utf-8 -*-
"""HydraTK properties module

.. module:: core.propertyhead
   :platform: Unix
   :synopsis: HydraTK properties module
.. moduleauthor:: Petr Czaderna <pc@headz.cz>

"""

from hydratk.core import const
from hydratk.translation.core import info

class PropertyHead(object):
    """Class PropertyHead
    """
    
    @property
    def current_async_ticket_id(self):
        """current_async_ticket_id property getter"""
        
        return self._current_async_ticket_id
    
    @property
    def async_fn_tickets(self):
        """async_fn_tickets property getter, setter"""
                
        return self._async_fn_tickets
    
    @async_fn_tickets.setter
    def async_fn_tickets(self, data):
        """async_fn_tickets property setter"""
                
        self._async_fn_tickets = data
           
    @property
    def fn_cb_shared(self):
        """fn_cb_shared property getter, setter"""
                
        return self._fn_cb_shared
    
    @fn_cb_shared.setter
    def fn_cb_shared(self, d):
        """fn_cb_shared property setter"""
                
        self._fn_cb_shared = d
    
    @property
    def cbm(self):
        """cbm property getter"""
                
        return self._cbm #CallbackManager instance
        
    @property
    def cli_cmdopt_profile(self):
        """opt_profile property getter"""
                
        return self._opt_profile
    
    @property
    def cfg(self):
        """config property getter"""
                
        return self._config
    
    @property
    def debug(self):
        """debug property getter"""
                
        return self._debug
    
    @property
    def debug_level(self):
        """debug_level property getter"""
                
        return self._debug_level
    
    @property
    def ext_cfg(self):
        """extensions config property getter"""
                
        return self._config['Extensions']
    
    @property
    def lang(self):
        """language property getter, setter"""
                
        return self._language
    
    @lang.setter
    def lang(self,language):
        """language property setter"""
                
        self._language = language if language in info.languages else const.DEFAULT_LANGUAGE
        
    @property
    def runlevel(self):
        """runlevel property getter"""
                
        return self._runlevel
    
    @property
    def run_mode(self):
        """run_mode property getter, setter"""
                
        return self._run_mode
    
    @run_mode.setter
    def run_mode(self, mode):
        """run_mode property setter"""
                
        if mode in(
                   const.CORE_RUN_MODE_PP_APP,
                   const.CORE_RUN_MODE_PP_APP,
                   const.CORE_RUN_MODE_PP_DAEMON                   
                   ):
            self._run_mode = mode