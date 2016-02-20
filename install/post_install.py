# -*- coding: utf-8 -*-
"""This code is a part of Hydra toolkit

.. module:: install.post_install
   :platform: Unix
   :synopsis: Module for post-install tasks
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from config import config as cfg
import command as cmd
from setuptools.command.install import install
from os import path

def run_post_install():
    
    print('**************************************') 
    print('*     Running post-install tasks     *')    
    print('**************************************')
    
    for task in cfg['post_tasks']:
        print('\n*** Running task: {0} ***\n'.format(task))
        globals()[task]()     

def set_access_rights():
    
    for dir, right in cfg['rights'].items():
        cmd.set_rights(dir, right)

        
def compile_java_classes():
    
    dir = cfg['java']['dir'] 
    if (path.exists(dir)):
        classpath = cfg['java']['classpath']
        for file in cfg['java']['files']:
            cmd.compile_java_class(dir, file, classpath)                                 