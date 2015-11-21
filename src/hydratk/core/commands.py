# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit

.. module:: core.commands
   :platform: Unix
   :synopsis: HydraTK commands and options
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
                     'ext-skel-path',                     
                     'force',
                     'interactive',
                     'language',
                     'lib-skel-path',                  
                    ]
short_opts        = 'dcilxt'

getopt_long_opts  = [
                     'config=',
                     'config-db-file=',
                     'ext-skel-path=',
                     'debug=',
                     'force',
                     'interactive',
                     'language=',
                     'lib-skel-path='                    
                    ]
getopt_short_opts = 'c:d:fil:'                    