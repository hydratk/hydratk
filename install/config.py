# -*- coding: utf-8 -*-

config = {
  'pre_tasks' : [
                 'version_update',
                 'install_libs_from_repo',
                 'install_pip'
                ],

  'post_tasks' : [
                  'copy_files',
                  'set_access_rights'
                 ],
          
  'modules' : [                           
               'pyyaml>=3.11',                              
               'xtermcolor>=1.3'                                                  
              ],
          
  'files' : {
             'etc/hydratk/hydratk.conf'               : '/etc/hydratk' ,
             'var/local/hydratk/dbconfig/__init__.py' : '/var/local/hydratk/dbconfig'        
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