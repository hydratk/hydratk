# -*- coding: utf-8 -*
"""HydraTK core bootstrapper

.. module:: core.bootstrapper
   :platform: Unix
   :synopsis: HydraTK core bootstrapper
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import sys
import os
from hydratk.lib.system.utils import Utils

PYTHON_MAJOR_VERSION = sys.version_info[0]
if PYTHON_MAJOR_VERSION == 2:
    reload(sys)
    sys.setdefaultencoding('UTF8')

dep_modules = {
    'importlib': {
        'package': 'importlib'
    },
    'psutil': {
        'min-version': '3.1.1',
        'package': 'psutil'
    },
    'setproctitle': {
        'min-version': '1.1.9',
        'package': 'setproctitle'
    },
    'xtermcolor': {
        'min-version': '1.3',
        'package': 'xtermcolor'
    },
    'yaml': {
        'min-version': '3.11',
        'package': 'pyyaml'
    },
    'zmq': {
        'min-version': '14.7.0',
        'package': 'pyzmq'
    }
}

lib_dependencies = {
    'hydratk-lib-network': 'hydratk.lib.network.dependencies',
    'hydratk-lib-numeric': 'hydratk.lib.numeric.dependencies'
}


def _check_dependencies(dep_modules=dep_modules, source='hydratk'):
    """Method checks if all dependent modules can be loaded

    Args:  
       dep_modules (dict): dependent modules 
       source (str): source hydratk module         

    Returns:
       bool: result, False if any module is missing            

    """

    result = True
    for mod, modinfo in dep_modules.items():
        try:
            lmod = __import__(mod)
            if ('min-version' in modinfo):
                version = lmod.__version__ if (
                    hasattr(lmod, '__version__')) else Utils.module_version(modinfo['package'])
                if (not Utils.module_version_ok(modinfo['min-version'], version)):
                    print("Dependency error for %s: module %s found with version: %s, but at least version %s is required, upgrade package %s" % (
                          source, mod, version, modinfo['min-version'], modinfo['package']))
                    result = False
        except ImportError:
            if ('optional' not in modinfo or modinfo['optional'] == False):
                print("Dependency error for %s: missing module %s, install package %s" % (
                    source, mod, modinfo['package']))
                result = False

    import importlib
    for lib, mod in lib_dependencies.items():
        try:
            dep_modules = importlib.import_module(mod).get_dependencies()
            for mod, modinfo in dep_modules.items():
                try:
                    lmod = __import__(mod)
                    if ('min-version' in modinfo):
                        version = lmod.__version__ if (
                            hasattr(lmod, '__version__')) else Utils.module_version(modinfo['package'])
                    if (not Utils.module_version_ok(modinfo['min-version'], version)):
                        print("Dependency error for %s: module %s found with version: %s, but at least version %s is required, upgrade package %s" % (
                              lib, mod, version, modinfo['min-version'], modinfo['package']))
                        result = False
                except ImportError:
                    if ('optional' not in modinfo or modinfo['optional'] == False):
                        print("Dependency error for %s: missing module %s, install package %s" % (
                            lib, mod, modinfo['package']))
                        result = False
        except ImportError:
            pass

    return result


def check_home_param():
    """Method checks for home parameter presence --home or -h to replace htk_root_dir location
    
    Args:
       none
    
    Returns:            
       bool: htk_root_changed 
    
    """
    
    htk_root_changed = False
    i = 0        
    for o in sys.argv:
        if o == 'help':
            break
        if o == '-h' or o == '--home':
            if sys.argv.index(o) < (len(sys.argv) - 1):
                from os.path import expanduser
                os.environ['htk_root_dir'] = expanduser("~")
                print("UPDATED OS ENVIRON WITH {0}".format(os.environ['htk_root_dir']))                    
                htk_root_changed = True
        i = i + 1
    return htk_root_changed

def run_app():
    """Method runs HydraTK application

    Method is executed from htk command (automatically installed)

    Args: 
       none           

    Returns:   
       void     

    """

    if (_check_dependencies()):
        check_home_param() #check for -h, --home switch
        
        from hydratk.core.masterhead import MasterHead
        mh = MasterHead.get_head()        
        mh.run_fn_hook('h_bootstrap')  # run level specific processing
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
