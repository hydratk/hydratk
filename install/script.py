# -*- coding: utf-8 -*-

from sys import version_info
import install.task as task

run_pre_install = task.run_pre_install
run_post_install = task.run_post_install

def version_update(cfg):
    
    major, minor = version_info[0], version_info[1]

    module = 'setproctitle>=1.1.9'
    if (major == 2 and minor == 6):     
        cfg['modules'].insert(0, 'importlib')
        cfg['libs'][module]['apt-get'][0] = 'python2.6-dev'
    elif (major == 3):
        cfg['libs'][module]['apt-get'][0] = 'python2.6-devel'
        cfg['libs'][module]['apt-get'][0] = 'python3-dev'
        cfg['libs'][module]['yum'][0] = 'python3-devel'

config = {
  'pre_tasks' : [
                 version_update,
                 task.install_libs,
                 task.install_modules
                ],

  'post_tasks' : [
                  task.set_config,
                  task.copy_files,
                  task.set_access_rights,
                  task.set_manpage
                 ],
          
  'modules' : [ 
               'setproctitle>=1.1.9',
               'pyzmq>=14.7.0',
               'psutil>=3.1.1',                          
               'pyyaml>=3.11',                                             
               'xtermcolor>=1.3'                                              
              ],
          
  'files' : {
             'config'  : {
                          'etc/hydratk/hydratk.conf' : '/etc/hydratk'
                         },
             'data'    : { 
                          'var/local/hydratk/dbconfig/__init__.py' : '/var/local/hydratk/dbconfig'
                         },
             'manpage' : 'doc/htk.1'        
            },
          
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
              '/etc/hydratk'       : 'a+r',
              '/var/local/hydratk' : 'a+rwx'
             }                              
}