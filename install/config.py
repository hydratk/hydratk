# -*- coding: utf-8 -*-
"""This code is a part of Hydra toolkit

.. module:: install.config
   :platform: Unix
   :synopsis: Module with install config
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

config = {
  'pre_tasks' : [
                 'install_libs_from_repo'
                ],

  'post_tasks' : [
                  'set_access_rights'
                 ],
          
  'modules' : [            
               'setproctitle>=1.1.9',
               'pyzmq>=14.7.0',
               'psutil>=3.1.1',
               'pyyaml>=3.11',                              
               'xtermcolor>=1.3'                                                  
              ],
          
  'files' : [
             ('/etc/hydratk',                ['etc/hydratk/hydratk.conf']), 
             ('/var/local/hydratk/dbconfig', ['var/local/hydratk/dbconfig/__init__.py'])         
            ],
          
  'libs' : {
            'pyzmq>=14.7.0'       : {                        
                                     'apt-get' : [
                                                  'g++', 
                                                  'libzmq-dev'
                                                 ],
                                     'yum'     : [
                                                  'gcc-c++', 
                                                  'zeromq'
                                                 ]
                                    },                       
            'setproctitle>=1.1.9' : {
                                     'repo'    : [
                                                  'gcc', 
                                                  'wget', 
                                                  'bzip2', 
                                                  'tar'
                                                 ],
                                     'apt-get' : [
                                                  'python-dev'
                                                 ],
                                     'yum'     : [
                                                  'redhat-rpm-config', 
                                                   'python-devel'
                                                 ]
                                    }                    
           },
          
  'rights' : {
              '/etc/hydratk'       : 'a+rwx',
              '/var/local/hydratk' : 'a+rwx'
             }                              
}