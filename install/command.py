# -*- coding: utf-8 -*-
"""This code is a part of Hydra toolkit

.. module:: install.command
   :platform: Unix
   :synopsis: Module for common commands used in installation tasks
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from subprocess import call, Popen, PIPE

def get_pck_manager():
    """Method detects package managers

    Args:
       none

    Returns:
       list: managers
    
    """    
    
    pck_managers = ['apt-get', 'yum']
    
    pckm = []
    for pck in pck_managers:     
        if (is_installed(pck)):
            pckm.append(pck) 
    
    return pckm  

def is_installed(app):
    """Method checks if application is installed

    Args:
       app (str): application

    Returns:
       bool: result
    
    """      
    
    cmd = ['which', app]
    proc = Popen(cmd, stdout=PIPE)
    out = proc.communicate() 

    result = True if (len(out[0]) > 0) else False
    return result   

def install_pck(pckm, pck):
    """Method installs package

    Args:
       pckm (str): package manager, apt-get|yum
       pck (str): package name

    Returns:
       void
    
    """     
    
    print('Installing package: {0}'.format(pck))
    
    if (pckm == 'apt-get'):
        cmd = 'apt-get -y install {0}'.format(pck)
    elif (pckm == 'yum'):
        cmd = 'yum -y install {0}'.format(pck)
        
    if (call(cmd, shell=True) != 0):
        print('Failed to install package {0}'.format(pck))                                                       
           
def set_rights(path, rights, recursive=True):
    """Method sets acces rights

    Args:
       path (str): directory or file path
       rights (str): access rights in Unix style
       recursive (bool): set recursive rights

    Returns:
       void
    
    """     
    
    print('Setting rights for {0}'.format(path))
    
    if (recursive):
        cmd = 'chmod -R {0} {1}'.format(rights, path)
    else:
        cmd = 'chmod {0} {1}'.format(rights, path)
        
    if (call(cmd, shell=True) != 0):
        print('Failed to set rights for {0}'.format(path))     