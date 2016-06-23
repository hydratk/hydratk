# -*- coding: utf-8 -*-
"""This code is a part of Hydra toolkit

.. module:: install.post_install
   :platform: Unix
   :synopsis: Module for post-install tasks
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from config import config as cfg
import command as cmd

def run_post_install():
    """Method runs post-install tasks

    Args:
       none

    Returns:
       void
    
    """     
    
    print('**************************************') 
    print('*     Running post-install tasks     *')    
    print('**************************************')
    
    for task in cfg['post_tasks']:
        print('\n*** Running task: {0} ***\n'.format(task))
        globals()[task]()     

def set_access_rights():
    """Method sets access rights

    Args:

    Returns:
       void
    
    """    
    
    for dir, right in cfg['rights'].items():
        cmd.set_rights(dir, right)                                