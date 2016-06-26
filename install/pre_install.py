# -*- coding: utf-8 -*-

from config import config as cfg
import command as cmd

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

def install_libs_from_repo(requires):       
    
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