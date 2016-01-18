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