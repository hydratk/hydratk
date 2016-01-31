# -*- coding: utf-8 -*-
"""This code is a part of Hydra toolkit

.. module:: install.custom_install
   :platform: Unix
   :synopsis: Module for custom installation scripts
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from setuptools.command.install import install
from sys import stdout
from subprocess import call
from os import path

class CustomInstall(install):
    
    def run(self):
        install.run(self)
        
        for key, val in scripts.items():
            self.execute(val, [], msg='Running {0} script'.format(key)) 
            
htk_dir = '/var/local/hydratk'
cfg_dir = '/etc/hydratk'             

def set_access_rights():
    
    stdout.write('Setting rights for {0}\n'.format(htk_dir))
    cmd = 'chmod -R a+rwx {0}'.format(htk_dir)
    if (call(cmd, shell=True) != 0):
        stdout.write('Failed to set rights\n')
        
    stdout.write('Setting rights for {0}\n'.format(cfg_dir))
    cmd = 'chmod -R a+r {0}'.format(cfg_dir)
    if (call(cmd, shell=True) != 0):
        stdout.write('Failed to set rights\n')  
        
def compile_java_classes():
    
    java_dir = path.join(htk_dir, 'java') 
    java_files = ['DBClient.java', 'JMSClient.java']
    
    for java_file in java_files:
        stdout.write('Compiling {0}\n'.format(java_file))
        cmd = 'javac -cp javaee.jar {0}\n'.format(java_file) 
        if (call(cmd, cwd=java_dir, shell=True) != 0):
            stdout.write('Failed to compile {0}\n'.format(java_file))                  
        
scripts = {
  'set_access_rights'    : set_access_rights,
  'compile_java_classes' : compile_java_classes
}            
    
