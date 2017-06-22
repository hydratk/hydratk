# -*- coding: utf-8 -*
"""HydraTK common installation tasks

.. module:: lib.install.task
   :platform: Unix
   :synopsis: HydraTK common installation tasks
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from .command import *
import os
import hydratk.lib.system.config as syscfg
from hydratk.lib.system.io import rprint
from hydratk.lib.console.shellexec import shell_exec

try:
    os_info = syscfg.get_supported_os()
except Exception as exc:
    print(str(exc))
    exit(1)


def run_pre_install(argv, cfg):
    """Function run pre-install tasks

    Args:
       argv (list): command arguments
       cfg (dict): configuration

    Returns:
       none

    """

    if (is_install_cmd(argv)):

        print('**************************************')
        print('*     Running pre-install tasks      *')
        print('**************************************')

        profiles = get_profiles(argv)

        for task in cfg['pre_tasks']:
            print('*** Running task: {0} ***'.format(task.__name__))
            task(cfg, profiles)


def run_post_install(argv, cfg):
    """Function run post-install tasks

    Args:
       argv (list): command arguments
       cfg (dict): configuration

    Returns:
       none

    """

    if (is_install_cmd(argv)):

        print('**************************************')
        print('*     Running post-install tasks     *')
        print('**************************************')

        profiles = get_profiles(argv)

        for task in cfg['post_tasks']:
            print('*** Running task: {0} ***'.format(task.__name__))
            task(cfg, profiles)


def check_libs(pkcm, lib_inst, lib_check): 
    """Function checks installed library dependencies

    Args:
       argv (list): command arguments
       cfg (dict): configuration

    Returns:
       list : missing libraries

    """       
    missing_libs = []
    for lib in lib_inst:
        rprint('Checking {0}'.format(lib))
        if lib in lib_check and 'cmd' in lib_check[lib]:                        
            if shell_exec(lib_check[lib]['cmd']) > 0:
                rprint("...FAILED\n")
                print("   {0}".format(lib_check[lib]['errmsg']))
                missing_libs.append(lib)
            else:
                rprint("...OK\n")                
        else:
            raise SystemError('Missing check information for install library {0}'.format(lib))
            
    return missing_libs
    

def install_libs(cfg, profiles, *args):
    """Function installs system libraries

    Args:
       cfg (dict): configuration
       profiles (list): module profiles

    Returns:
       none

    """

    pckm = get_pck_manager()[0]
    libs, modules = cfg['libs'], cfg['modules']
    lib_inst = []
    lib_check = {}
            
    for mod in modules:
        module = mod['module']
        if (module in libs):

            do_install = True
            if ('profile' in mod):
                if ('full' not in profiles and mod['profile'] not in profiles + ['basic']):
                    do_install = False
                    
            if do_install:
                if (pckm in libs[module][os_info['compat']]):
                    #Be sure that list of installable libraries is unique
                    lib_inst = list(set(lib_inst).union(set(libs[module][os_info['compat']][pckm])))                                       
                    lib_check.update(libs[module][os_info['compat']]['check'])
                    
    #Check required libraries
    missing_libs = check_libs(pckm, lib_inst, lib_check)
    uid = os.getuid()
    if uid != 0 and len(missing_libs) > 0:
        print("\nRequired libraries are not present: {0}\nYou can install them yourself to make them visible to the installer\nor rerun the setup with root priviledges to install them with available package manager ({1})\n".format(",".join(missing_libs), pckm))    
        exit(1)
              
    for lib in missing_libs:
        install_pck(pckm, lib)


def install_modules(cfg, profiles, *args):
    """Method install python modules

    Args:
       cfg (dict): configuration
       profiles (list): module profiles

    Returns:
       none

    """

    for mod in cfg['modules']:
        module = mod['module'] + mod['version'] if ('version' in mod) else mod['module']

        do_install = True
        if ('profile' in mod):
            if ('full' not in profiles and mod['profile'] not in profiles + ['basic']):
                do_install = False

        if (do_install):
            install_pip(module)


def create_dirs(cfg, *args):
    """Method creates directories

    Args:
       cfg (dict): configuration

    Returns:
       none

    """

    for dir in cfg['dirs']:
        create_dir(dir)


def copy_files(cfg, *args):
    """Method copies data files

    Args:
       cfg (dict): configuration

    Returns:
       none

    """

    for file, dir in cfg['files']['data'].items():
        copy_file(file, dir)


def set_access_rights(cfg, *args):
    """Method sets access rights

    Args:
       cfg (dict): configuration

    Returns:
       none

    """

    for dir, right in cfg['rights'].items():
        set_rights(dir, right)


def set_config(cfg, *args):
    """Method sets configuration file

    Args:
       cfg (dict): configuration

    Returns:
       none

    """

    for file, dir in cfg['files']['config'].items():

        cfg_file = '/' + file
        if (os.path.exists(cfg_file)):
            with open(file, 'r') as f:
                f_new = f.read()
            with open(cfg_file, 'r') as f:
                f_curr = f.read()

            if (f_curr != f_new):
                move_file(cfg_file, cfg_file + '_old')

        copy_file(file, dir)


def set_manpage(cfg, *args):
    """Method sets manual page

    Args:
       cfg (dict): configuration

    Returns:
       none

    """

    manpage = cfg['files']['manpage']
    call('gzip -c {0} > {1}'.format(manpage,
                                    '/usr/share/man/man1/' + manpage.split('/')[-1]), shell=True)


def get_profiles(argv):
    """Method gets module profiles 

    Args:
       argv (list): input arguments

    Returns:
       list: profiles

    """

    profiles = ['full']
    for arg in argv:
        if ('--profile' in arg):
            profiles = arg.split('=')[1].split(',')
            argv.remove(arg)
            break

    return profiles
