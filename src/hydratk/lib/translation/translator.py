# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit library

.. module:: translator
   :platform: Unix
   :synopsis: A useful module for application multilanguagee support.
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import sys
import pprint

PYTHON_MAJOR_VERSION = sys.version_info[0]

if PYTHON_MAJOR_VERSION == 2:   
    from __builtin__ import len
    

if PYTHON_MAJOR_VERSION == 3:    
    from builtins import len


class Translator():
    '''
    classdocs
    '''
    _msg_mod   = None
    _help_mod  = None    
    __language = ''
    __messages = {} #MultiDict
    __language = None

    def __init__(self, messages = ''):
        '''
        Constructor
        '''              
        if messages != '':
            if type(messages) is dict:
                self.__messages = messages
            else:                
                print(type(messages))
                print(messages)
                raise ValueError('Cannot assign an empty messages, dictionary expected')    
    @property
    def msg_mod(self):
        return self._msg_mod
    
    @msg_mod.setter
    def msg_mod(self,msg_module):
        self._msg_mod = msg_module
    
    @property
    def help_mod(self):
        return self._help_mod
    
    @help_mod.setter
    def help_mod(self,help_module):
        self._help_mod = help_module          
        pprint.pprint(self._help_mod.help_cmd) 
    
    def set_help_mod(self,help_module):
        self._help_mod = help_module
        
    def register_messages(self,messages):        
        if messages != '':
            if type(messages) is dict:
                self.__messages = messages                
            else:
                raise ValueError('Invalid messages type, dictionary expected')                
        else:
            raise ValueError('Cannot assign an empty messages, dictionary expected')                
        return True
        
    def set_language(self,lang):
        self.__language = lang
        
    def get_language(self):
        return self.__language
    
    def lmsg(self, lang, key,*args):              
        return self.__messages[lang][key] % args if self.__messages[lang][key] != {} else None
    
    def msg(self, key, *args):              
        return self.__messages[key] % args if key in self.__messages else key

    def add_msg(self,msg, id = ''):            
        result = 0        
        if type(msg).__name__ == 'dict':                        
            for msg_id, msg_text in msg.items():                    
                if (msg_id != '' and msg_text != ''):
                    self.__messages[msg_id] = msg_text
                    result = result + 1
                
        else:        
            if (id != '' and msg != ''):
                self.__messages[id] = msg
                result = 1
        return result
    
    def add_help(self, help):                  
        result = 0        
        if hasattr(help, 'help_cmd') and type(help.help_cmd).__name__ == 'dict':                        
            for help_cmd_id, help_cmd_text in help.help_cmd.items():                    
                if (help_cmd_id != '' and help_cmd_text != ''):
                    self._help_mod.help_cmd[help_cmd_id] = help_cmd_text
                    result = result + 1
                
        if hasattr(help, 'help_opt') and type(help.help_opt).__name__ == 'dict':                        
            for help_opt_id, help_opt_text in help.help_opt.items():                    
                if (help_opt_id != '' and help_opt_text != ''):
                    self._help_mod.help_opt[help_opt_id] = help_opt_text
                    result = result + 1
        
        if hasattr(help, 'help_cmd_args') and type(help.help_cmd_args).__name__ == 'dict':                        
            for help_cmd_args_id, help_cmd_args_text in help.help_cmd_args.items():                    
                if (help_cmd_args_id != '' and help_cmd_args_text != ''):
                    self._help_mod.help_cmd_args[help_cmd_args_id] = help_cmd_args_text
                    result = result + 1
                                
        return result
    
    def lang_add_msg(self, msg, lang):
        result = 0
        if lang == '' or len(lang) < 2: raise ValueError('Invalid value for language specified')
        if type(msg).__name__ == 'dict': 
            for msg_id, msg_text in msg.items():                    
                    if (lang != '' and msg_id != '' and msg_text != ''):
                        self.__messages[lang][msg_id] = msg_text
                        result = result + 1
        return result