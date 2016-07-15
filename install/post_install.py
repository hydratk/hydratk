# -*- coding: utf-8 -*-

from install.config import config as cfg
import install.command as cmd

def run_post_install(argv):    
    
    if (cmd.is_install_cmd(argv)):              
    
        print('**************************************') 
        print('*     Running post-install tasks     *')    
        print('**************************************')
    
        for task in cfg['post_tasks']:
            print('\n*** Running task: {0} ***\n'.format(task))
            globals()[task]()  
            
def copy_files():  
    
    for file, dir in cfg['files'].items():        
        cmd.copy_file(file, dir)               

def set_access_rights():   
    
    for dir, right in cfg['rights'].items():
        cmd.set_rights(dir, right)                                