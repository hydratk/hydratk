# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit

.. module:: core.extension
   :platform: Unix
   :synopsis: HydraTK extensions implementation class
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

from hydratk.lib.exceptions import *

class Extension:
    _ext_id            = 'Undefined'
    _ext_name          = 'Undefined'
    _ext_version       = 'Undefined'
    _ext_author        = 'Undefined'
    _ext_year          = 'Undefined'
    ''' MasterHead object reference '''           
    _mh                = None     
    '''
    classdocs    
    '''
    
    def __getattr__(self,name):
        if hasattr(self.__class__, '_wrap_hydra_attrs') and self._wrap_hydra_attrs == True:
            if hasattr(self._mh, name):
                return self._mh[name]
    
    def __init__(self, core_instance = None):                  
        self._mh = core_instance
        self._init_extension()        
        
        if hasattr(self.__class__, '_check_dependencies') and callable(getattr(self.__class__, '_check_dependencies')):
            self._check_dependencies()
        
        if hasattr(self.__class__, '_do_imports') and callable(getattr(self.__class__, '_do_imports')):
            self._do_imports()        
        
        if hasattr(self.__class__, '_register_actions') and callable(getattr(self.__class__, '_register_actions')):
            self._register_actions()                   

    def get_ext_name(self):
        return self._ext_name
    
    def get_ext_version(self):
        return self._ext_version
    
    def get_ext_author(self):
        return self._ext_author
    
    def get_ext_info(self):
        return self._ext_name +' v'+ self._ext_version + ' (c) [' + self._ext_year + ' '+ self._ext_author + ']'    