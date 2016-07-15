# -*- coding: utf-8 -*-
"""HydraTK python system hooks

.. module:: core.hookhead
   :platform: Unix
   :synopsis: HydraTK python system hooks
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
import sys
import imp

from hydratk.translation.config import packages_map

class ModuleLoader():
    """Class ModuleLoader
    """
    
    _package_path = None
    
    def find_module(self, module_name, package_path):
        """Method imports module langtexts
        
        Args:     
           module_name (str): full module name
           package_path (str): full package 
           
        Returns:
           obj: ModuleLoeader
                
        """         
        
        if module_name in packages_map:   #translation messages handling         
            self._import_package_messages(module_name, packages_map[module_name])
            return None   
        else:
            #TODO remove, this is for testing purposes only
            if module_name == 'yodahelpers.o2.soc.pc.customerusage':
                print("Load request {0} {1}".format(module_name, package_path))                
                self._package_path = package_path        
                return self
        return None
    
    def load_module(self, module_name):
        """Method loads module
        
        Args:     
           module_name (str): full module name
           
        Returns:
           obj: module
                
        """  
                
        if module_name in packages_map: #translation messages handling
            return None
        else:
            if module_name in sys.modules:
                return sys.modules[module_name]
            mod = module_name.split('.')[-1:][0] if module_name.count('.') > 0 else module_name 
            module_info = imp.find_module(mod, self._package_path)
            module = imp.load_module(mod, *module_info)
            sys.modules[module_name] = module
            sys.modules[mod] = module
                    
            return module   


        