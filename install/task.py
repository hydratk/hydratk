# -*- coding: utf-8 -*

import install.command as cmd
from subprocess import call

def run_pre_install(argv, cfg):  

    if (cmd.is_install_cmd(argv)):      
     
        print('**************************************') 
        print('*     Running pre-install tasks      *')    
        print('**************************************')
    
        for task in cfg['pre_tasks']:
            print('\n*** Running task: {0} ***\n'.format(task.__name__))
            task(cfg) 
            
def run_post_install(argv, cfg):       
    
    if (cmd.is_install_cmd(argv)):              
    
        print('**************************************') 
        print('*     Running post-install tasks     *')    
        print('**************************************')
    
        for task in cfg['post_tasks']:
            print('\n*** Running task: {0} ***\n'.format(task.__name__))
            task(cfg)    
            
def install_libs(cfg):           
    
    pckm = cmd.get_pck_manager()[0]  
         
    libs, modules = cfg['libs'], cfg['modules'] 
  
    for key in libs.keys():
        if (key in modules):
            lib_inst = []
            if ('repo' in libs[key]):
                lib_inst += libs[key]['repo']
            if (pckm in libs[key]):
                lib_inst += libs[key][pckm]
            for lib in lib_inst:
                cmd.install_pck(pckm, lib)                   
                
def install_modules(cfg):      
    
    for module in cfg['modules']:
        cmd.install_pip(module)  
        
def copy_files(cfg):      
    
    for file, dir in cfg['files']['data'].items():        
        cmd.copy_file(file, dir)               

def set_access_rights(cfg):       
    
    for dir, right in cfg['rights'].items():
        cmd.set_rights(dir, right)  

def set_config(cfg):    
     
    for file, dir in cfg['files']['config'].items(): 
        with open(file, 'r') as f:
            f_new = f.read()
        cfg_file = '/'+file
        with open(cfg_file, 'r') as f:
            f_curr = f.read()  
        
        if (f_curr != f_new):
            cmd.move_file(cfg_file, cfg_file+'_old')    
                 
        cmd.copy_file(file, dir) 
        
def set_manpage(cfg): 
        
    manpage = cfg['files']['manpage']
    call('gzip -c {0} > {1}'.format(manpage, '/usr/share/man/man1/'+manpage.split('/')[-1]), shell=True)                              