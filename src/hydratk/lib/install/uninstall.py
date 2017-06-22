# -*- coding: utf-8 -*
"""HydraTK uninstallation tasks

.. module:: lib.install.uninstall
   :platform: Unix
   :synopsis: HydraTK uninstallation tasks
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

import hydratk.lib.install.command as cmd
import hydratk.lib.system.config as syscfg
from hydratk.core.masterhead import MasterHead
from hydratk.core.bootstrapper import dep_modules
from sys import exit, argv

files = [
    '/usr/share/man/man1/htk.1',
    '{0}/hydratk'.format(syscfg.HTK_ETC_DIR),
    '{0}/hydratk'.format(syscfg.HTK_VAR_DIR)
]

libs = {
    'network': 'hydratk.lib.network.dependencies',
    'numeric': 'hydratk.lib.numeric.dependencies'
}


def run_uninstall():
    """Method runs installation script

    Args:
       none

    Returns:
       none

    """

    cnt = len(argv)
    uninst_pymod = True if (cnt > 1 and argv[1] == '-y') else False
    htkmod = argv[
        cnt - 1] if (cnt > 2 or (cnt == 2 and argv[1] != '-y')) else 'all'

    mh = MasterHead.get_head()
    mh.run_fn_hook('h_bootstrap')

    for title, ext in mh._ext.items():
        if (htkmod in ['all', ext._ext_id] and ext._ext_id not in ['benchmark']):
            if (hasattr(ext, '_uninstall')):
                ext_files, ext_mods = ext._uninstall()
            else:
                ext_files, ext_mods = [], {}
            ext_mods = _get_dependencies(ext_mods) if (uninst_pymod) else {}
            uninstall_ext(ext._ext_id, ext_files, ext_mods)

    import importlib
    for title, mod in libs.items():
        if (htkmod in ['all', title]):
            try:
                lib = importlib.import_module(mod)
                if (hasattr(lib, '_uninstall')):
                    lib_files, lib_mods = lib._uninstall()
                else:
                    lib_files, lib_mods = [], {}
                lib_mods = _get_dependencies(
                    lib_mods) if (uninst_pymod) else {}
                uninstall_lib(title, lib_files, lib_mods)
            except ImportError:
                pass

    if (htkmod == 'all'):
        cmd.uninstall_pip('hydratk')

        for f in files:
            cmd.remove(f)

        if (uninst_pymod):
            for mod in _get_dependencies(dep_modules):
                if (mod != 'importlib'):
                    cmd.uninstall_pip(mod)

    exit(0)


def uninstall_ext(ext_id, files, mods):
    """Method uninstalls extension

    Args:
       ext_id (str): extension id
       files (list): extension files
       mods (list): dependent modules

    Returns:
       none

    """

    cmd.uninstall_pip('hydratk-ext-' + ext_id)

    for f in files:
        cmd.remove(f)

    for mod in mods:
        if ('hydratk' not in mod):
            cmd.uninstall_pip(mod)


def uninstall_lib(lib_id, files, mods):
    """Method uninstalls library

    Args:
       lib_id (str): library id
       files (list): library files
       mods (list): dependent modules

    Returns:
       none

    """

    cmd.uninstall_pip('hydratk-lib-' + lib_id)

    for f in files:
        cmd.remove(f)

    for mod in mods:
        if ('hydratk' not in mod):
            cmd.uninstall_pip(mod)


def _get_dependencies(dependencies):
    """Method gets dependent modules

    Args:
       dependencies (dict): dependent modules

    Returns:
       list

    """

    mods = []
    for key, val in dependencies.items():
        mods.append(val['package'])

    return mods
