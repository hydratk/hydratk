# -*- coding: utf-8 -*-
"""HydraTK core module dependency definitions

.. module:: core.dependencies
   :platform: Unix
   :synopsis: HydraTK core module dependency definitions
.. moduleauthor:: Petr Czaderna <pc@headz.cz>

"""

dep_modules = {
                 'zmq' : {
                          'min-version' : '14.3.1',
                          'desc' : 'Zero message queue'
                         },
                 'yaml' : {
                          'min-version' : '3.11',
                          'desc' : 'YAML parser'
                         },
                 'setproctitle': {
                          'desc' : 'System process title changer'       
                         },
                 'sqlite3' : {
                          'desc' : 'SQLite v3 database handler'    
                         }  
                }

"""
Module not working currently under pypy3 2.4.0
                'psutil': {
                           'desc' : 'System and process utilities'  
                         } 
                         
"""