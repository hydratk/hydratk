# -*- coding: utf-8 -*-

"""This code is a part of Hydra toolkit

.. module:: hookhead
   :platform: Unix
   :synopsis: Python system hooks.
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
from hydratk.translation.config import packages_map

class TranslationMsgLoader():
    
    def find_module(self, module_name, package_path):
        if module_name in packages_map:            
            self._import_package_messages(module_name, packages_map[module_name])   
        
        return None
    
    def load_module(self, module_name):        
        return None

        