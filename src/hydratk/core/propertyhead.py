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
    def lang(self):
        return self._language
    
    @lang.setter
    def lang(self,language):
        self._language = language if language in info.languages else const.DEFAULT_LANGUAGE
        
    @property
    def runlevel(self):
        return self._runlevel