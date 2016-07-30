# -*- coding: utf-8 -*-
"""HydraTK commands and options

.. module:: core.commandopt
   :platform: Unix
   :synopsis: HydraTK commands and options
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

'''
Options mapping
Alias - option xxx can have aliases -x (short option), --xxx (long option)
Value - option is used as xxx <value> or xxx if value is/isn't configured
'''
opt = {
      'htk' : {
            '-c'               :  {
                                    'd_opt'           : 'config',
                                    'has_value'       : True,
                                    'allow_multiple'  : False                           
                                  },
            '--config'         :  {
                                    'd_opt'           : 'config',
                                    'has_value'       : True,
                                    'allow_multiple'  : False                            
                                  },                             
            '--config-db-file' :  {
                                    'd_opt'           : 'config-db-file',
                                    'has_value'       : True,
                                    'allow_multiple'  : False                            
                                  }, 
            '-d'               :  {
                                    'd_opt'           : 'debug',
                                    'has_value'       : True,
                                    'allow_multiple'  : False                            
                                  },                             
            '--debug'          :  {
                                    'd_opt'           : 'debug',
                                    'has_value'       : True,
                                    'allow_multiple'  : False                            
                                  },
            '-e'               :  {
                                    'd_opt'           : 'debug-channel',
                                    'has_value'       : True,
                                    'allow_multiple'  : False                            
                                  },                      
            '--debug-channel'  :  {
                                    'd_opt'           : 'debug-channel',
                                    'has_value'       : True,
                                    'allow_multiple'  : False                            
                                  },                                                                              
            '--ext-skel-path'  :  {
                                    'd_opt'           : 'ext-skel-path',
                                    'has_value'       : True,
                                    'allow_multiple'  : False                            
                                  },
            '-f '              :  {
                                    'd_opt'           : 'force',
                                    'has_value'       : False,
                                    'allow_multiple'  : False                            
                                  },      
            '--force'          :  {
                                    'd_opt'           : 'force',
                                    'has_value'       : False,
                                    'allow_multiple'  : False                            
                                  },
            '-i'               :  {
                                    'd_opt'           : 'interactive',
                                    'has_value'       : False,
                                    'allow_multiple'  : False                            
                                  },      
            '--interactive'    :  {
                                    'd_opt'           : 'interactive',
                                    'has_value'       : False,
                                    'allow_multiple'  : False                            
                                  },
            '-l'               :  {
                                    'd_opt'           : 'language',
                                    'has_value'       : True,
                                    'allow_multiple'  : False                            
                                  },      
            '--language'       :  {
                                    'd_opt'           : 'language',
                                    'has_value'       : True,
                                    'allow_multiple'  : False                            
                                  },
            '--lib-skel-path'  :  {
                                    'd_opt'           : 'lib-skel-path',
                                    'has_value'       : True,
                                    'allow_multiple'  : False                            
                                  },
            '-m'               :  {
                                    'd_opt'           : 'run-mode',
                                    'has_value'       : True,
                                    'allow_multiple'  : False                            
                                  },                               
            '--run-mode'       :  {
                                    'd_opt'           : 'run-mode',
                                    'has_value'       : True,
                                    'allow_multiple'  : False                            
                                  }                                                                                                                   
                                                                
      }
}

''' target options '''
d_opt = {         
       'htk': [
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
}

''' long options '''
long_opt = {
       'htk': [
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
}

''' short options '''
short_opt = {
              'htk' : [
                       'c',
                       'd',
                       'e',
                       'f',
                       'i',
                       'l',
                       'm'
                      ]             
            }

''' commands '''
cmd = {
      'htk' : [
                'create-config-db',
                'create-ext-skel',
                'create-lib-skel', 
                'start',
                'stop',
                'help',
                'list-extensions' 
              ]               
      }
