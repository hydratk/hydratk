# -*- coding: utf-8 -*-
"""HYdraTK commands and options

.. module:: core.commands
   :platform: Unix
   :synopsis: HydraTK commands and options, legacy deprecated version, will be removed soon 
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

commands          = [
                    'create-config-db',
                    'create-ext-skel',
                    'create-lib-skel', 
                    'start',
                    'stop',
                    'help',
                    'list-extensions' 
                    ]
                    
long_opts         = [
                     'debug',
                     'config',
                     'config-db-file',
                     'debug-channel',
                     'ext-skel-path',                     
                     'force',
                     'interactive',
                     'language',
                     'lib-skel-path',
                     'run-mode'                                      
                    ]
short_opts        = [
                     'c',
                     'd',
                     'e',
                     'f',
                     'i',
                     'l',
                     'm'
                    ]

getopt_long_opts  = [
                     'config=',
                     'config-db-file=',
                     'ext-skel-path=',
                     'debug=',
                     'debug-channel=',
                     'force',
                     'interactive',
                     'language=',
                     'lib-skel-path='
                     'run-mode='                    
                    ]
getopt_short_opts = [
                     'c',
                     'd',
                     'e',
                     'f',
                     'i',
                     'l',
                     'm'
                    ]                   