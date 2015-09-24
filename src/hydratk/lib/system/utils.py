"""This code is a part of Pyx application framework

.. module:: system.utils
   :platform: Unix
   :synopsis: A useful module for misc utils.
.. moduleauthor:: Petr Czaderna <pc@headz.cz>

"""
import pkgutil;
import pkg_resources;
import pprint;

class Utils():
    
    @staticmethod
    def module_version(module):
        return pkg_resources.get_distribution(module).version
        
    @staticmethod
    def module_loaded(module):
        result = False;
        for importer, modname, ispkg in pkgutil.iter_modules():
            if modname == module:
                result = True;
                break;                 
        return result;
    
    @staticmethod
    def module_exists(module_name):        
        if globals().get(module_name, False):
            return True
        return False

    @staticmethod
    def module_version_ok(min_version,cur_version):
        from distutils.version import StrictVersion
        return StrictVersion(cur_version) >= StrictVersion(min_version)