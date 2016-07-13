# -*- coding: utf-8 -*-
"""A useful module for application multilanguagee support

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
    """Class Translator
    """
    
    _msg_mod     = None
    _help_mod    = None    
    _language    = ''
    _messages    = {}
    _language    = None
    _debug_level = 1

    def __init__(self, messages=''):
        """Class constructor
        
        Called when object is initialized

        Args:
           messages (dict): message dictionary

        Raises:
           error: ValueError
    
        """
               
        if messages != '':
            if type(messages) is dict:
                self._messages = messages
            else:                
                print(type(messages))
                print(messages)
                raise ValueError('Cannot assign an invalid messages, dictionary expected')    
            
    @property
    def msg_mod(self):
        """ msg_mod property getter, setter """
        
        return self._msg_mod
    
    @msg_mod.setter
    def msg_mod(self, msg_module):
        """ msg_mod property setter """
        
        self._msg_mod = msg_module
    
    @property
    def help_mod(self):
        """ help_mod property getter, setter """
        
        return self._help_mod
    
    @help_mod.setter
    def help_mod(self, help_module):
        """ help_mod property setter """ 
        
        self._help_mod = help_module          
        pprint.pprint(self._help_mod.help_cmd) 
    
    def set_help_mod(self, help_module):
        """Methods sets help module

        Args:
           help_module (str): help module

        Returns:
           void
    
        """
                
        self._help_mod = help_module
        
    def register_messages(self, messages):
        """Methods registers langtexts

        Args:
           messages (dict): langtexts

        Returns:
           bool: True
           
        Raises:
           error: ValueError
    
        """
                        
        if messages != '':
            if type(messages) is dict:
                self._messages = messages                
            else:
                raise ValueError('Invalid messages type, dictionary expected')                
        else:
            raise ValueError('Cannot assign an empty messages, dictionary expected')                
        return True
    
    def set_debug_level(self, level):
        """Methods sets debug level

        Args:
           level (int): debug level, default 1

        Returns:
           void
    
        """
                
        self._debug_level = int(level) if int(level) > 0 else 1 
            
    def set_language(self, lang):
        """Methods sets language

        Args:
           lang (str): language

        Returns:
           void
    
        """
                
        self._language = lang
        
    def get_language(self):
        """Methods gets language

        Args:
           none

        Returns:
           str: language
    
        """
                
        return self._language
    
    def lmsg(self, lang, key, *args):      
        """Methods resolves langtext

        Args:
           lang (str): language
           key (str): langtext
           args (ags): langtext arguments

        Returns:
           str: resolved langtext
    
        """
                        
        return self._messages[lang][key] % args if self._messages[lang][key] != {} else None
    
    def msg(self, key, *args): 
        """Methods resolves langtext according to debug level

        Args:
           key (str): langtext
           args (ags): langtext arguments

        Returns:
           str: resolved langtext
    
        """
                                           
        return self._messages[key][:self._debug_level][-1].format(*args) if key in self._messages else key       

    def add_msg(self, msg, id=''): 
        """Methods adds new messages

        Args:
           msg (obj): dict (identified by key) or str, messages
           id (str): message identifier

        Returns:
           int: count of added messages
    
        """
                           
        result = 0        
        if type(msg).__name__ == 'dict':                        
            for msg_id, msg_text in msg.items():                    
                if (msg_id != '' and msg_text != ''):
                    self._messages[msg_id] = msg_text
                    result = result + 1
                
        else:        
            if (id != '' and msg != ''):
                self._messages[id] = msg
                result = 1
        return result
    
    def add_help(self, help):  
        """Methods adds new help texts

        Args:
           help (obj): help object

        Returns:
           int: count of added help texts
    
        """
                                
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
        """Methods adds new langtexts

        Args:
           msg (dict): langtexts
           lang (str): language

        Returns:
           int: count of added langtexts 
           
        Raises:
           error: ValueError
    
        """
                
        result = 0
        if lang == '' or len(lang) < 2: raise ValueError('Invalid value for language specified')
        if type(msg).__name__ == 'dict': 
            for msg_id, msg_text in msg.items():                    
                    if (lang != '' and msg_id != '' and msg_text != ''):
                        self._messages[lang][msg_id] = msg_text
                        result = result + 1
        return result