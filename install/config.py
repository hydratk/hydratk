# -*- coding: utf-8 -*-
"""This code is a part of Hydra toolkit

.. module:: install.config
   :platform: Unix
   :synopsis: Module with install config
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

config = {
  'pre_tasks' : [
                 'install_libs_from_repo',
                 'install_java',
                 'install_oracle',
                 'install_phantomjs'
                ],

  'post_tasks' : [
                  'set_access_rights',    
                  'compile_java_classes' 
                 ],
          
  'modes' : [
             'basic',
             'full',
             'custom'
            ],
          
  'modules' : {
               'basic' : [              
                          'psutil',
                          'pyyaml',
                          'pyzmq',
                          'setproctitle',
                          'xtermcolor',                                            
                         ],
               'full'  : [        
                          'cherrypy',
                          'cx_Oracle',
                          'httplib2',
                          'JPype1',
                          'jsonlib2',
                          'lxml',                
                          'MySQL-python', 
                          'paramiko',
                          'psycopg2',               
                          'pycurl',     
                          'python-ldap',                                                     
                          'python-ntlm',               
                          'scapy',
                          'selenium', 
                          'suds', 
                          'tftpy',
                          'tornado'                         
                         ]           
              },
          
  'files' : {
             'basic' : [
                        ('/etc/hydratk',                ['etc/hydratk/hydratk.conf']), 
                        ('/var/local/hydratk/dbconfig', ['var/local/hydratk/dbconfig/__init__.py'])
                       ],
             'full'  : [
                        ('/var/local/hydratk/java', ['src/hydratk/lib/network/jms/java/JMSClient.java']), 
                        ('/var/local/hydratk/java', ['src/hydratk/lib/network/jms/java/javaee.jar']),
                        ('/var/local/hydratk/java', ['src/hydratk/lib/network/dbi/java/DBClient.java'])  
                       ]            
            },
          
  'libs' : {
            'cx_Oracle'    : {
                              'apt-get' : [
                                           'libaio1',
                                           'libaio-dev'
                                          ],
                              'yum'     : [
                                           'libaio'
                                          ],
                              'url'     : 'http://download.oracle.com/otn/linux/instantclient/121020',
                              'file'    : [
                                           'instantclient-basic-linux.x64-12.1.0.2.0.zip',
                                           'instantclient-sdk-linux.x64-12.1.0.2.0.zip',
                                           'instantclient-sqlplus-linux.x64-12.1.0.2.0.zip'
                                          ],                              
                              'dir'     : 'instantclient_12_1',
                              'symlink' : {
                                           'libclntsh.so.12.1'      : 'libclntsh.so',
                                           'libclntshcore.so.12.1'  : 'libclnthshcore.so',
                                           'libocci.so.12.1'        : 'libocci.so'
                                          }
                             },
            'JPype1'       : {
                              'url'     : 'http://download.oracle.com/otn-pub/java/jdk/8u74-b02',
                              'file'    : 'jdk-8u74-linux-x64.tar.gz',
                              'dir'     : 'jdk1.8.0_74'
                             },
            'lxml'         : {
                              'repo'    : [
                                           'python-lxml'
                                          ]
                             },
            'MySQL-python' : {
                              'repo'    : [
                                           'mysql-devel'
                                          ],
                              'apt-get' : [
                                           'python-mysqldb'
                                          ]
                             },
            'psycopg2'     : {
                              'repo'    : [
                                           'python-psycopg2'
                                          ]
                             },             
            'pycurl'       : {
                              'repo'    : [
                                           'python-pycurl'
                                          ]
                             },
            'python-ldap'  : {
                              'apt-get' : [
                                           'libldap2-dev',
                                           'libsasl2-dev',
                                           'libssl-dev'
                                          ],
                              'yum'     : [
                                           'openldap-devel'
                                          ]
                             },
            'pyzmq'        : {                        
                              'apt-get' : [
                                           'g++', 
                                           'libzmq-dev'
                                          ],
                              'yum'     : [
                                           'gcc-c++', 
                                           'zeromq'
                                          ]
                             },                       
            'selenium'     : {
                              'apt-get' : [
                                           'libfontconfig'
                                          ],
                              'yum'     : [
                                           'fontconfig'
                                          ],
                              'url'     : 'https://bitbucket.org/ariya/phantomjs/downloads',
                              'file'    : 'phantomjs-2.1.1-linux-x86_64.tar.bz2',
                              'dir'     : 'phantomjs-2.1.1-linux-x86_64'
                             },
            'setproctitle' : {
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
             },
          
  'java' : {
            'dir'       : '/var/local/hydratk/java',
            'files'     : [
                           'DBClient.java', 
                           'JMSClient.java'
                          ],
            'classpath' : 'javaee.jar' 
           },
          
  'os' : {
          'inst_dir' : '/usr/local',
          'profile'  : '/etc/profile',
          'ldconfig' : '/etc/ld.so.conf.d'
         }                              
}