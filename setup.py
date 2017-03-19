# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from sys import argv, version_info
import src.hydratk.lib.install.task as task

with open("README.rst", "r") as f:
    readme = f.read()
    
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Environment :: Other Environment",
    "Intended Audience :: Developers",
    "License :: Freely Distributable",
    "Operating System :: OS Independent",   
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python",    
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: Implementation",
    "Programming Language :: Python :: Implementation :: CPython", 
    "Programming Language :: Python :: Implementation :: PyPy",  
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Topic :: Utilities"
]

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
                  task.create_dirs,
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
          
  'dirs' : [
            '/var/local/hydratk/dbconfig'
           ],        
          
  'files' : {
             'config'  : {
                          'etc/hydratk/hydratk.conf' : '/etc/hydratk'
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

task.run_pre_install(argv, config)

entry_points = {
                'console_scripts': [
                    'htk = hydratk.core.bootstrapper:run_app',
                    'htkprof = hydratk.core.bootstrapper:run_app_prof',
                    'htkuninstall = hydratk.lib.install.uninstall:run_uninstall'             
                ]
               } 
     
setup(
      name='hydratk',
      version='0.5.0a.dev3',
      description='Fully extendable object oriented application toolkit with nice modular architecture',
      long_description=readme,
      author='Petr Czaderna, HydraTK team',
      author_email='pc@hydratk.org, team@hydratk.org',
      url='http://www.hydratk.org',
      license='BSD',
      packages=find_packages('src'),
      package_dir={'' : 'src'},
      classifiers=classifiers,
      zip_safe=False,      
      entry_points=entry_points,
      keywords='toolkit,utilities,testing,analysis',
      requires_python='>=2.6,!=3.0.*,!=3.1.*,!=3.2.*',
      platforms='Linux'
     )

task.run_post_install(argv, config)