# -*- coding: utf-8 -*-
"""Module for handling commandline input options based on argparse 

.. module:: lib.console.cmdoptparser
   :platform: Unix
   :synopsis: Module for handling commandline input options based on argparse 
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import argparse

class CmdOptParserUndefined(Exception): pass
class CmdOptParserError(Exception): pass

class CmdOptParser(argparse.ArgumentParser):
    """Class CmdOptParses
    
    Inherited from ArgumentParser
    """
    
    _silent     = False
    _set_opts   = {}
    _unreg_opts = []
    _opt_group  = 'default'
    _options    =  {
                    'default' : {}               
                   }
    
    def error(self, message):
        """Method raises error
        
        Args:            
           message (str): message text
           
        Returns:
           void    
           
        Raises:
           error: CmdOptParserError
                
        """  
                
        raise CmdOptParserError(message)
    
    def set_default_opt_group(self, group_name):
        """Method sets default option group
        
        Args:            
           group_name (str): group name
           
        Returns:
           void    
           
        Raises:
           error: CmdOptParserUndefined
           error: TypeError
                
        """  
                
        if group_name is not None:
            if group_name in self._options:
                self._opt_group = group_name
            else:
                raise CmdOptParserUndefined('Undefined group {0}'.format(group_name))
        else:
            raise TypeError('Group name cannot be NoneType')
    
    def add_opt_groups(self, group_list):
        pass
        
    def add_opt_group(self, group_name):
        """Method adds new option group
        
        Args:            
           name (str): group name
           
        Returns:
           void    
           
        Raises:
           error: TypeError
                
        """  
                
        if group_name is not None:
            if group_name not in self._options:
                self._options[group_name] = {}
        else:
            raise TypeError('Group name cannot be NoneType')
    
    def _add_opt(self, option, d_option=None, has_value=False, allow_multiple=False, opt_group='default'):
        """Method adds new option
        
        Args:   
           option (obj): str or list, option 
           d_option (str): target option
           has_value (bool): option value allowed
           allow_multiple (bool): multiple option occurences allowed
           opt_group (str): option group
           
        Returns:
           bool: result
           
        Raises:
           error: CmdOptParserError
           error: TypeError    
                
        """  
                        
        if opt_group not in self._options:
            self.add_opt_group(opt_group)        
        if type(option).__name__ == 'list':
            for opt in option:
                if opt['option'] not in self._options[opt_group]:
                    kopt = opt['option']
                    del opt['option']
                    self._options[opt_group][kopt] = opt 
                else:
                    if self._silent == False:
                        raise CmdOptParserError('Option add duplicate {0}'.format(option))
            result = True
              
        elif type(option).__name__ == 'str':
            opt = {}
            if option not in self._options[opt_group]:
                if has_value == True:
                    if allow_multiple == True:
                        opt['action'] = 'append'
                    else:
                        opt['action'] = 'store'
                else:
                    opt['action'] = 'store_true'
                
                if d_option is not None:
                    opt['dest'] = d_option
                    
                self._options[opt_group][option] = opt
                result = True             
                
            else:
                if self._silent == False:
                    raise CmdOptParserError('Option add duplicate {0}'.format(option))
        else:
            raise TypeError('Unsupported option type {0}'.format(type(option)))                
        return result

        
    def add_opt(self, option, d_option=None, has_value=False, allow_multiple=False, opt_group='default'):
        """Method adds new option
        
        Args:   
           option (obj): str or list, option 
           d_option (str): target option
           has_value (bool): option value allowed
           allow_multiple (bool): multiple option occurences allowed
           opt_group (str): option group
           
        Returns:
           bool: result  
                
        """  
                
        result = False
        if type(opt_group).__name__ == 'list':
            for lopt_grp in opt_group:
                if lopt_grp not in self._options:
                    self.add_opt_group(lopt_grp)
                self._add_opt(option, d_option, has_value, allow_multiple, lopt_grp)
            result = True         
        elif  type(opt_group).__name__ == 'str':
            self._add_opt(option, d_option, has_value, allow_multiple, opt_group) 
            result = True
        
        return result
    
                   
    def add_getopt_opt(self, short_opt, long_opt, opt_map={}):
        """Method adds new option
        
        Args:   
           short_opt (list): short options 
           long_opt (list): long options
           opt_map (dict): option mapping
           
        Returns:
           void
                
        """  
                
        if type(short_opt).__name__ == 'list' and len(short_opt) > 0:
            for opt in short_opt:
                cur_opt = "-{0}".format(opt)
                d_option = opt_map[cur_opt] if cur_opt in opt_map else None
                has_value = True if opt[-1:] == '=' else False
                self.add_opt(cur_opt, d_option, has_value)
                
        if type(long_opt).__name__ == 'list' and len(long_opt) > 0:
            for opt in long_opt:
                cur_opt = "--{0}".format(opt)
                d_option = opt_map[cur_opt] if cur_opt in opt_map else None
                has_value = True if opt[-1:] == '=' else False
                self.add_opt(cur_opt, d_option, has_value)

    def parse(self, opt_group = 'default', hide_undef = True):
        """Method adds new option
        
        Args:   
           opt_group (str): option group
           hide_undef (bool): hide undefined options
           
        Returns:
           tuple: options (dict), undefined options 
           
        Raises:
           error: CmdOptParserUndefined 
                
        """  
                
        if opt_group not in self._options:
            raise CmdOptParserUndefined('Undefined group {0}'.format(opt_group))  
        for opt_name, opt_args in self._options[opt_group].items():            
            self.add_argument(opt_name, **opt_args)
            
        set_opts, unreg_opts = self.parse_known_args()
        set_opts             = vars(set_opts)        
        self._set_opts       = set_opts if hide_undef == False else self._strip_opts(set_opts)
        self._unreg_opts     = unreg_opts[:-1]
                
        return (self._set_opts, self._unreg_opts)
    
    def _strip_opts(self, opts):
        """Method strips options without value
        
        Args:   
           opts (dict): options
           
        Returns:
           dict: stripped options
             
                
        """  
                
        for opt, value in list(opts.items()):
            if value in (None,False):
                del opts[opt]
        return opts
        
    def opt_defined(self, option_name):
        """Method checks if option is defined
        
        Args:   
           option_name (str): option
           
        Returns:
           bool: result  
                
        """  
                
        return option_name in self._set_opts and self._set_opts[option_name] != False        
    
    def get_opt(self, option_name):  
        """Method gets option
        
        Args:   
           option_name (str): option
           
        Returns:
           dict: option, when defined
           bool: False, when not defined
                
        """  
                      
        return self._set_opts[option_name] if self.opt_defined(option_name) == True else False 
