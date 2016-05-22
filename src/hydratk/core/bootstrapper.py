# -*- coding: utf-8 -*
"""HydraTK core bootstrapper

.. module:: core.bootstrapper
   :platform: Unix
   :synopsis: HydraTK core bootstrapper
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import sys
from hydratk.lib.system.utils import Utils
from hydratk.core.dependencies import dep_modules


PYTHON_MAJOR_VERSION = sys.version_info[0]
if PYTHON_MAJOR_VERSION == 2:
    reload(sys)
    sys.setdefaultencoding('UTF8')
    
def _check_dependencies():
    """Method checks if all dependent modules can be loaded
    
    Modules are configured in hydratk.core.dependencies (including minimum version)
        
    Args:  
       none          
           
    Returns:
       bool: result, False if any module is missing            
                
    """       
    
    result = True
    for mod, modinfo in dep_modules.items():
        if Utils.module_loaded(mod):
            lmod = __import__(mod)
            if 'min-version' in modinfo:
                if not Utils.module_version_ok(modinfo['min-version'], lmod.__version__):
                    print("Dependency error: module %s found with version: %s, but at least version %s is required" % (mod, lmod.__version__, modinfo['min-version']))
                    result = False  
        else:
            print("Dependency error: missing module %s" % mod)
            result = False
    return result

def run_app():
    """Method runs HydraTK application
    
    Method is executed from htk command (automatically installed)
        
    Args: 
       none           
           
    Returns:   
       void     
                
    """
        
    if (_check_dependencies()):        
        from hydratk.core.masterhead import MasterHead
        
        mh = MasterHead.get_head()            
        mh.run_fn_hook('h_bootstrap') # run level specific processing
        trn = mh.get_translator()  
        mh.dmsg('htk_on_debug_info', trn.msg('htk_app_exit'), mh.fromhere())       
           
    sys.exit(0)

def run_app_prof():
    """Method runs HydraTK application in profiling mode
    
    Method is executed from htkprof command (automatically installed)
    C profiler lsprof is used
        
    Args:    
       none
    
    Returns:
       void             
                
    """    
    
    from hydratk.core.profiler import Profiler
    pr = Profiler()
    pr.start()
    run_app()
    pr.finish()
