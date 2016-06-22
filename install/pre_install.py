# -*- coding: utf-8 -*-
"""This code is a part of Hydra toolkit

.. module:: install.pre_install
   :platform: Unix
   :synopsis: Module for pre-install tasks
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from config import config as cfg
import command as cmd

def run_pre_install():
    """Method runs pre-install tasks

    Args:
       none

    Returns:
       tuple: requires (list), data_files (list)
    
    """    
    
    print('********************************')
    print('*    HydraTK installation      *')
    print('********************************')    
    
    requires = cfg['modules']
    data_files = cfg['files']
     
    print('**************************************') 
    print('*     Running pre-install tasks      *')    
    print('**************************************')
    
    for task in cfg['pre_tasks']:
        print('\n*** Running task: {0} ***\n'.format(task))
        globals()[task](requires)          
    
    return (requires, data_files)  

def install_libs_from_repo(requires):
    """Method installs libraries from repositories

    Args:
       requires (list): required libraries

    Returns:
       void
    
    """        
    
    pckm = cmd.get_pck_manager()[0]  
         
    libs = cfg['libs']    
    for key in libs.keys():
        if (key in requires):
            lib_inst = []
            if (libs[key].has_key('repo')):
                lib_inst += libs[key]['repo']
            if (libs[key].has_key(pckm)):
                lib_inst += libs[key][pckm]
            for lib in lib_inst:
                cmd.install_pck(pckm, lib)               