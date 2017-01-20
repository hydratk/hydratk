# -*- coding: utf-8 -*
"""HydraTK installation commands

.. module:: lib.install.command
   :platform: Unix
   :synopsis: HydraTK installation commands
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from subprocess import call, Popen, PIPE
from os import path
from sys import exit

def is_install_cmd(argv):
    """Method checks if installation is requested

    Args:
       argv (list): command arguments

    Returns:
       bool: result
    
    """    

    res = False    
    if ('install' in argv or 'bdist_egg' in argv or 'bdist_wheel' in argv):
        res = True

    return res

def get_pck_manager():  
    """Method returns system package manager
    
    Supported: apt-get, yum

    Args:
       none

    Returns:
       list: list of string
    
    """      
    
    pck_managers = ['apt-get', 'yum']
    
    pckm = []
    for pck in pck_managers:     
        if (is_installed(pck)):
            pckm.append(pck) 
    
    return pckm  

def is_installed(app): 
    """Method checks if system application is installed

    Args:
       app: (str): application

    Returns:
       bool: result
    
    """        
    
    cmd = ['which', app]
    proc = Popen(cmd, stdout=PIPE)
    out = proc.communicate() 

    result = True if (len(out[0]) > 0) else False
    return result   

def install_pck(pckm, pck): 
    """Method installs system package from repository

    Args:
       pckm (str): package manager
       pck: (str): package

    Returns:
       none
    
    """         
    
    print('Installing package {0}'.format(pck))
    
    if (pckm == 'apt-get'):
        cmd = 'apt-get -y install {0}'.format(pck)
    elif (pckm == 'yum'):
        cmd = 'yum -y install {0}'.format(pck)
        
    if (call(cmd, shell=True) != 0):
        print('Failed to install package {0}, hydratk installation failed.'.format(pck)) 
        exit(-1)
        
def create_dir(dst):
    """Method creates directory

    Args:
       dst (str): destination path

    Returns:
       none
    
    """      
    
    if (not path.exists(dst)):
        
        print('Creating directory {0}'.format(dst))
        cmd = 'mkdir -p {0}'.format(dst)
        
        if (call(cmd, shell=True) != 0):
            print('Failed to create directory {0}'.format(dst))     
        
def copy_file(src, dst):
    """Method copies file

    Args:
       src (str): source path
       dst (str): destination path

    Returns:
       none
    
    """      
    
    create_dir(dst)   
          
    print ('Copying file {0} to {1}'.format(src, dst))
    cmd = 'cp {0} {1}'.format(src, dst) 
    
    if (call(cmd, shell=True) != 0):
        print('Failed to copy {0} to {1}'.format(src, dst)) 
        
def move_file(src, dst):
    """Method moves file

    Args:
       src (str): source path
       dst (str): destination path

    Returns:
       none
    
    """     
    
    print('Moving file {0} to {1}'.format(src, dst)) 
    cmd = 'mv {0} {1}'.format(src, dst) 
    
    if (call(cmd, shell=True) != 0):
        print('Failed to move {0} to {1}'.format(src, dst))                                                                     
           
def set_rights(path, rights, recursive=True):
    """Method sets access rights

    Args:
       path (str): directory/file path
       rights (str): access rights 
       recursive (bool): set recursive rights

    Returns:
       none
    
    """         
    
    print('Setting rights {0} for {1}'.format(rights, path))
    
    if (recursive):
        cmd = 'chmod -R {0} {1}'.format(rights, path)
    else:
        cmd = 'chmod {0} {1}'.format(rights, path)
        
    if (call(cmd, shell=True) != 0):
        print('Failed to set rights for {0}'.format(path))  
        
def install_pip(module):
    """Method installs python module via pip

    Args:
       module (str): python module

    Returns:
       none
    
    """      
    
    print ('Installing module {0}'.format(module))
    
    cmd = 'pip install {0}'.format(module) 
    if (call(cmd, shell=True) != 0):
        print('Failed to install {0}, hydratk installation failed.'.format(module))
        exit(-1)       