# -*- coding: utf-8 -*
"""HydraTK uninstallation tasks

.. module:: lib.install.uninstall
   :platform: Unix
   :synopsis: HydraTK uninstallation tasks
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

import hydratk.lib.install.command as cmd
from hydratk.core.masterhead import MasterHead
from sys import exit, argv

files = [
         '/usr/share/man/man1/htk.1',
         '/etc/hydratk',
         '/var/local/hydratk'
        ]

libs = {
  'network' : 'hydratk.lib.network.dependencies'
}

def run_uninstall():
    """Method runs installation script

    Args:
       none

    Returns:
       none
    
    """              
    
    module = argv[1] if (len(argv) > 1) else 'all'
    mh = MasterHead.get_head()
    mh.run_fn_hook('h_bootstrap')
        
    for title, ext in mh._ext.items():
        if (module in ['all', ext._ext_id] and hasattr(ext, '_uninstall')):
            uninstall_ext(ext._ext_id, ext._uninstall())
    
    import importlib
    for title, mod in libs.items():
        if (module in ['all', title]):
            try:
                lib_files = importlib.import_module(mod)._uninstall()
                uninstall_lib(title, lib_files)
            except ImportError:
                pass
    
    if (module == 'all'):
        cmd.uninstall_pip('hydratk')
        for f in files:
            cmd.remove(f)            

    exit(0)
    
def uninstall_ext(ext_id, files):
    """Method uninstalls extension

    Args:
       ext_id (str): extension id
       files (list): extension files

    Returns:
       none
    
    """      
    
    if (ext_id not in ['benchmark']):
        cmd.uninstall_pip('hydratk-ext-'+ext_id)
    
    for f in files:
        cmd.remove(f)  
        
def uninstall_lib(lib_id, files):   
    """Method uninstalls library

    Args:
       lib_id (str): library id
       files (list): library files

    Returns:
       none
    
    """  
    
    cmd.uninstall_pip('hydratk-lib-'+lib_id)  
    
    for f in files:
        cmd.remove(f)              