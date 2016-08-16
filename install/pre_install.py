# -*- coding: utf-8 -*-

from install.config import config as cfg
import install.command as cmd
from sys import version_info
from os import system

def run_pre_install(argv):  
    
    requires = cfg['modules']
    
    if (cmd.is_install_cmd(argv)):      
     
        print('**************************************') 
        print('*     Running pre-install tasks      *')    
        print('**************************************')
    
        for task in cfg['pre_tasks']:
            print('\n*** Running task: {0} ***\n'.format(task))
            requires = globals()[task](requires)          
    
    return requires 

def version_update(requires):
    
    major, minor = version_info[0], version_info[1]
    
    cfg['modules'].insert(0, 'setproctitle>=1.1.9')
    cfg['modules'].insert(1, 'psutil>=3.1.1')
    cfg['modules'].insert(2, 'pyzmq>=14.7.0')
    
    module = 'setproctitle>=1.1.9'
    if (major == 2 and minor == 6):     
        cfg['libs'][module]['apt-get'][0] = 'python2.6-dev'
    elif (major == 3):
        cfg['libs'][module]['apt-get'][0] = 'python2.6-devel'
        cfg['libs'][module]['apt-get'][0] = 'python3-dev'
        cfg['libs'][module]['yum'][0] = 'python3-devel'
        
    return requires

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
                
    return requires
                
def install_pip(requires):   
    
    major, minor = version_info[0], version_info[1]  
    
    if (major == 2 and minor == 6):
        system('pip install importlib') 
        
    system('pip install setproctitle>=1.1.9')
    requires.append('setproctitle>=1.1.9')
    system('pip install psutil>=3.1.1')
    requires.append('psutil>=3.1.1')
    system('pip install pyzmq>=14.7.0')
    requires.append('pyzmq>=14.7.0')
        
    return requires                           