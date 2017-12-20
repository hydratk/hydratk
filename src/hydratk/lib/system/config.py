# -*- coding: utf-8 -*-
"""A useful module for configuration defaults

.. module:: lib.system.config
   :platform: Unix
   :synopsis: A useful module for configuration defaults.
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
import sys
import os
import re

HTK_ROOT_DIR = '/'
HTK_ETC_DIR  = '/etc'
HTK_VAR_DIR  = '/var/local'
HTK_LOG_DIR  = "{0}/hydratk/logs".format(HTK_VAR_DIR)
HTK_USR_DIR  = '/usr'
HTK_TMP_DIR  = '/tmp'

def update_htk_vars():
    """Function updates HTK config variables

    Returns:
       none

    """
    global HTK_ROOT_DIR
    global HTK_ETC_DIR
    global HTK_VAR_DIR
    global HTK_LOG_DIR
    global HTK_USR_DIR
    global HTK_TMP_DIR
        
    if is_virtualized():        
        HTK_ROOT_DIR = sys.prefix
        HTK_ETC_DIR  = "{0}/etc".format(HTK_ROOT_DIR)
        HTK_VAR_DIR  = "{0}/var/local".format(HTK_ROOT_DIR)
        HTK_LOG_DIR  = "{0}/hydratk/logs".format(HTK_VAR_DIR)
        HTK_USR_DIR  = "{0}/usr".format(HTK_ROOT_DIR)
        HTK_TMP_DIR  = "{0}/tmp".format(HTK_ROOT_DIR)
    

    if 'HTK_ROOT_DIR' in os.environ or 'htk_root_dir' in os.environ:               
        tmp_dir = os.environ['HTK_ROOT_DIR'] if 'HTK_ROOT_DIR' in os.environ else os.environ['htk_root_dir']        
        if os.path.exists(tmp_dir):
            HTK_ROOT_DIR = tmp_dir    
            HTK_ETC_DIR  = "{0}/etc".format(HTK_ROOT_DIR)
            HTK_VAR_DIR  = "{0}/var/local".format(HTK_ROOT_DIR)
            HTK_LOG_DIR  = "{0}/hydratk/logs".format(HTK_VAR_DIR)
            HTK_USR_DIR  = "{0}/usr".format(HTK_ROOT_DIR)
            HTK_TMP_DIR  = "{0}/tmp".format(HTK_ROOT_DIR)            
                
    if 'HTK_ETC_DIR' in os.environ or 'htk_etc_dir' in os.environ:
        tmp_dir = os.environ['HTK_ETC_DIR'] if 'HTK_ETC_DIR' in os.environ else os.environ['htk_etc_dir']
        if os.path.exists(tmp_dir):
            HTK_ETC_DIR = tmp_dir
            
    if 'HTK_VAR_DIR' in os.environ or 'htk_var_dir' in os.environ:
        tmp_dir = os.environ['HTK_VAR_DIR'] if 'HTK_VAR_DIR' in os.environ else os.environ['htk_var_dir']
        if os.path.exists(tmp_dir):
            HTK_ETC_DIR = tmp_dir
    
    if 'HTK_USR_DIR' in os.environ or 'htk_usr_dir' in os.environ:
        tmp_dir = os.environ['HTK_USR_DIR'] if 'HTK_USR_DIR' in os.environ else os.environ['htk_usr_dir']
        if os.path.exists(tmp_dir):
            HTK_USR_DIR = tmp_dir 
            
    if 'HTK_LOG_DIR' in os.environ or 'htk_log_dir' in os.environ:
        tmp_dir = os.environ['HTK_LOG_DIR'] if 'HTK_LOG_DIR' in os.environ else os.environ['htk_log_dir']
        if os.path.exists(tmp_dir):
            HTK_LOG_DIR = tmp_dir                         
   
    if 'HTK_TMP_DIR' in os.environ or 'htk_tmp_dir' in os.environ:
        tmp_dir = os.environ['HTK_TMP_DIR'] if 'HTK_TMP_DIR' in os.environ else os.environ['htk_tmp_dir']
        if os.path.exists(tmp_dir):
            HTK_TMP_DIR = tmp_dir                         

def is_virtualized():
    """Function determines if there's virtualized Python environment

    Returns:
       Bool : result

    """
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) or re.search('\.pyenv/', sys.prefix)

    
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
       'status' : '',
       'pckm' : ''
    }
    supported_systems = ('Linux', 'FreeBSD','Windows')
    c_os = platform.system()
    if c_os not in supported_systems:
        raise SystemError('Unsupported operating system platform {0}'.format(c_os))
    
    if c_os == 'Linux':
        distinfo = platform.linux_distribution(supported_dists=platform._supported_dists + ('arch', 'mageia',), full_distribution_name=0)
        os_result['name'] = distinfo[0]
        os_result['version'] = distinfo[1] 
        os_result['status'] = distinfo[2]
        
        # Debian based distros
        if os_result['name'].lower() in ('debian', 'ubuntu', 'linuxmint'):
            os_result['compat'] = 'debian'
            os_result['pckm'] = 'apt-get'
        # Red Hat based distros
        elif os_result['name'].lower() in ('redhat', 'centos', 'mandrake', 'mandriva', 'rocks', 'yellowdog'):
            os_result['compat'] = 'redhat'
            os_result['pckm'] = 'yum'
        # Fedora based distros
        elif os_result['name'].lower() in ('fedora'):
            os_result['compat'] = 'fedora'
            os_result['pckm'] = 'dnf'
        # SuSe based distros
        elif os_result['name'].lower() in ('suse'):
            os_result['compat'] = 'suse'
            os_result['pckm'] = 'zypper'
        # Slackware based distros
        elif os_result['name'].lower() in ('slackware'):
            os_result['compat'] = 'slackware'
        # Gentoo based distros
        elif os_result['name'].lower() in ('gentoo'):
            os_result['compat'] = 'gentoo'
            os_result['pckm'] = 'emerge'
        # Arch based distros
        elif os_result['name'].lower() in ('arch'):
            os_result['compat'] = 'arch'
            os_result['pckm'] = 'pacman'
        else:
            raise SystemError('Unsupported Linux distribution {0}'.format(os_result['name']))
    elif c_os == 'FreeBSD':
        os_result['compat'] = 'freebsd'
        os_result['pckm'] = 'pkg'
        
    if c_os == 'Windows':
        distinfo = platform.win32_ver()
        os_result['name']    = distinfo[0]
        os_result['version'] = distinfo[1] 
        os_result['status']  = distinfo[2]
        os_result['compat']  = 'windows'
            
    return os_result
              
update_htk_vars()
