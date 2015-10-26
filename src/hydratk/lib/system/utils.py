# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit

.. module:: system.utils
   :platform: Unix
   :synopsis: A useful module for misc utils.
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
import pkgutil
import pkg_resources


class Utils():
    
    @staticmethod
    def module_version(module):
        return pkg_resources.get_distribution(module).version
        
    @staticmethod
    def module_loaded(module):
        result = False
        for _, modname, _ in pkgutil.iter_modules(): #unused importer and ispkg
            if modname == module:
                result = True
                break                 
        return result
    
    @staticmethod
    def module_exists(module_name):        
        if globals().get(module_name, False):
            return True
        return False

    @staticmethod
    def module_version_ok(min_version,cur_version):
        from distutils.version import StrictVersion
        return StrictVersion(cur_version) >= StrictVersion(min_version)