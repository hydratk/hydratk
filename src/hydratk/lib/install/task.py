# -*- coding: utf-8 -*
"""HydraTK common installation tasks

.. module:: lib.install.task
   :platform: Unix
   :synopsis: HydraTK common installation tasks
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

import hydratk.lib.install.command as cmd
from subprocess import call

def run_pre_install(argv, cfg):  
    """Method run pre-install tasks

    Args:
       argv (list): command arguments
       cfg (dict): configuration

    Returns:
       none
    
    """      

    if (cmd.is_install_cmd(argv)):      
     
        print('**************************************') 
        print('*     Running pre-install tasks      *')    
        print('**************************************')
    
        for task in cfg['pre_tasks']:
            print('\n*** Running task: {0} ***\n'.format(task.__name__))
            task(cfg) 
            
def run_post_install(argv, cfg): 
    """Method run post-install tasks

    Args:
       argv (list): command arguments
       cfg (dict): configuration

    Returns:
       none
    
    """        
    
    if (cmd.is_install_cmd(argv)):              
    
        print('**************************************') 
        print('*     Running post-install tasks     *')    
        print('**************************************')
    
        for task in cfg['post_tasks']:
            print('\n*** Running task: {0} ***\n'.format(task.__name__))
            task(cfg)    
            
def install_libs(cfg):  
    """Method installs system libraries

    Args:
       cfg (dict): configuration

    Returns:
       none
    
    """          
    
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
    """Method install python modules

    Args:
       cfg (dict): configuration

    Returns:
       none
    
    """        
    
    for module in cfg['modules']:
        cmd.install_pip(module)  
        
def copy_files(cfg):  
    """Method copies data files

    Args:
       cfg (dict): configuration

    Returns:
       none
    
    """      
    
    for file, dir in cfg['files']['data'].items():        
        cmd.copy_file(file, dir)               

def set_access_rights(cfg):  
    """Method sets access rights

    Args:
       cfg (dict): configuration

    Returns:
       none
    
    """       
    
    for dir, right in cfg['rights'].items():
        cmd.set_rights(dir, right)  

def set_config(cfg):
    """Method sets configuration file

    Args:
       cfg (dict): configuration

    Returns:
       none
    
    """      
     
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
    """Method sets manual page

    Args:
       cfg (dict): configuration

    Returns:
       none
    
    """  
        
    manpage = cfg['files']['manpage']
    call('gzip -c {0} > {1}'.format(manpage, '/usr/share/man/man1/'+manpage.split('/')[-1]), shell=True)                              