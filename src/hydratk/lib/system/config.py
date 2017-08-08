# -*- coding: utf-8 -*-
"""A useful module for configuration defaults

.. module:: lib.system.config
   :platform: Unix
   :synopsis: A useful module for configuration defaults.
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
import sys
import os

HTK_ROOT_DIR = '/'
HTK_ETC_DIR  = '/etc'
HTK_VAR_DIR  = '/var/local'

def update_htk_vars():
    """Function updates HTK config variables

    Returns:
       none

    """
    global HTK_ROOT_DIR
    global HTK_ETC_DIR
    global HTK_VAR_DIR
        
    if is_virtualized():        
        HTK_ROOT_DIR = sys.prefix
        HTK_ETC_DIR  = "{0}/etc".format(HTK_ROOT_DIR)
        HTK_VAR_DIR  = "{0}/var/local".format(HTK_ROOT_DIR)
    

    if 'HTK_ROOT_DIR' in os.environ or 'htk_root_dir' in os.environ:               
        tmp_dir = os.environ['HTK_ROOT_DIR'] if 'HTK_ROOT_DIR' in os.environ else os.environ['htk_root_dir']        
        if os.path.exists(tmp_dir):
            HTK_ROOT_DIR = tmp_dir    
            HTK_ETC_DIR  = "{0}/etc".format(HTK_ROOT_DIR)
            HTK_VAR_DIR  = "{0}/var/local".format(HTK_ROOT_DIR)            
                
    if 'HTK_ETC_DIR' in os.environ or 'htk_etc_dir' in os.environ:
        tmp_dir = os.environ['HTK_ETC_DIR'] if 'HTK_ETC_DIR' in os.environ else os.environ['htk_etc_dir']
        if os.path.exists(tmp_dir):
            HTK_ETC_DIR = tmp_dir
            
    if 'HTK_VAR_DIR' in os.environ or 'htk_var_dir' in os.environ:
        tmp_dir = os.environ['HTK_VAR_DIR'] if 'HTK_VAR_DIR' in os.environ else os.environ['htk_var_dir']
        if os.path.exists(tmp_dir):
            HTK_ETC_DIR = tmp_dir            
   

def is_virtualized():
    """Function determines if there's virtualized Python environment

    Returns:
       Bool : result

    """
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

    
def get_supported_os():
    """Function returns supported os string

    Returns:
       str : os string

    """    
    import platform
    os_result = {
       'compat' : '',          
       'name' : '',
       'version' : '',
       'status' : ''          
    }
    c_os = platform.system()
    if c_os not in ('Linux'): 
        raise SystemError('Unsupported operating system platform {0}'.format(c_os))
    
    if c_os == 'Linux':
        distinfo = platform.linux_distribution()
        os_result['name'] = distinfo[0]
        os_result['version'] = distinfo[1] 
        os_result['status'] = distinfo[2]
        
        # Debian based distros
        if os_result['name'].lower() in (
                                          'debian', 'ubuntu', 'edubuntu', 'kubuntu', 'linuxmint',
                                          'ubuntu gnome', 'ubuntu mate', 'ubuntu budgie',
                                          'lubuntu', 'xubuntu', 'ubuntu server', 'ubuntu studio',                                          
                                        ):
            os_result['compat'] = 'debian'
        # Red Hat based distros
        elif os_result['name'].lower() in (
                                           'red hat linux','centos','fedora',
                                           ):
            os_result['compat'] = 'redhat'           
        else:
            raise SystemError('Unsupported Linux distribution {0}'.format(os_result['name']))
        
    return os_result

              
update_htk_vars()
