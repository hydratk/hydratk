# -*- coding: utf-8 -*
"""HydraTK common installation tasks

.. module:: lib.install.task
   :platform: Unix
   :synopsis: HydraTK common installation tasks
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from .command import *
from os import path


def run_pre_install(argv, cfg):
    """Method run pre-install tasks

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
            print('\n*** Running task: {0} ***\n'.format(task.__name__))
            task(cfg, profiles)


def run_post_install(argv, cfg):
    """Method run post-install tasks

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
            print('\n*** Running task: {0} ***\n'.format(task.__name__))
            task(cfg, profiles)


def install_libs(cfg, profiles, *args):
    """Method installs system libraries

    Args:
       cfg (dict): configuration
       profiles (list): module profiles

    Returns:
       none

    """

    pckm = get_pck_manager()[0]
    libs, modules = cfg['libs'], cfg['modules']
    lib_inst = []

    for mod in modules:
        module = mod['module']
        if (module in libs):

            do_install = True
            if ('profile' in mod):
                if ('full' not in profiles and mod['profile'] not in profiles + ['basic']):
                    do_install = False

            if (do_install):
                if ('repo' in libs[module]):
                    lib_inst += libs[module]['repo']
                if (pckm in libs[module]):
                    lib_inst += libs[module][pckm]

    for lib in lib_inst:
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
        module = mod['module']
        if ('version' in mod):
            module += mod['version']

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
        if (path.exists(cfg_file)):
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
