# -*- coding: utf-8 -*-

from install.config import config as cfg
import install.command as cmd
from sys import version_info

def run_pre_install(argv):  
    
    requires = cfg['modules']
    
    if (cmd.is_install_cmd(argv)):      
     
        print('**************************************') 
        print('*     Running pre-install tasks      *')    
        print('**************************************')
    
        for task in cfg['pre_tasks']:
            print('\n*** Running task: {0} ***\n'.format(task))
            globals()[task](requires)          
    
    return requires 

def version_update(requires):
    
    major, minor = version_info[0], version_info[1]
    
    if (major == 2 and minor == 6):
        cfg['modules'].append('importlib')
        cfg['libs']['setproctitle>=1.1.9']['apt-get'][0] = 'python2.6-dev'
    elif (major == 3):
        cfg['libs']['setproctitle>=1.1.9']['apt-get'][0] = 'python3-dev'
        cfg['libs']['setproctitle>=1.1.9']['yum'][0] = 'python3-devel'

def install_libs_from_repo(requires):       
    
    pckm = cmd.get_pck_manager()[0]  
         
    libs = cfg['libs']    
    for key in libs.keys():
        if (key in requires):
            lib_inst = []
            if ('repo' in libs[key]):
                lib_inst += libs[key]['repo']
            if (pckm in libs[key]):
                lib_inst += libs[key][pckm]
            for lib in lib_inst:
                cmd.install_pck(pckm, lib)               