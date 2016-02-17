# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit

.. module:: lib.console.cmdoptparser
   :platform: Unix
   :synopsis: Module for handling commandline input options based on argparse 
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import argparse

class CmdOptParserUndefined(Exception): pass
class CmdOptParserError(Exception): pass

class CmdOptParser(argparse.ArgumentParser):
    _silent     = False
    _set_opts   = {}
    _unreg_opts = []
    _opt_group  = 'default'
    _options    =  {
                    'default' : {}               
                   }
    
    def error(self, message):
        raise CmdOptParserError(message)
    
    def set_default_opt_group(self, group_name):
        if group_name is not None:
            if group_name in self._options:
                self._opt_group = group_name
            else:
                raise CmdOptParserUndefined('Undefined group {}'.format(group_name))
        else:
            raise TypeError('Group name cannot be NoneType')
    
    def add_opt_groups(self,group_list):
        pass
        
    def add_opt_group(self, group_name):
        if group_name is not None:
            self._options[group_name] = {}
        else:
            raise TypeError('Group name cannot be NoneType')
    
    def _add_opt(self, option, d_option = None, has_value = False, allow_multiple = False, opt_group = 'default'):        
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
                        raise CmdOptParserError('Option add duplicate {}'.format(option))
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
                    raise CmdOptParserError('Option add duplicate {}'.format(option))
        else:
            raise TypeError('Unsupported option type {}'.format(type(option)))                
        return result

        
    def add_opt(self, option, d_option = None, has_value = False, allow_multiple = False, opt_group = 'default'):
        result = False
        if type(opt_group).__name__ == 'list':
            for lopt_grp in opt_group:
                if lopt_grp not in self._options:
                    self.add_opt_group(lopt_grp)
                self._add_opt(option, d_option, has_value, allow_multiple, lopt_grp)
            result = True         
        elif  type(opt_group).__name__ == 'str':
            self._add_opt(option, d_option, has_value, allow_multiple, opt_group) 
        
        return result
    
                   
    def add_getopt_opt(self, short_opt, long_opt, opt_map = {}):
        if type(short_opt).__name__ == 'str' and len(short_opt) > 0:
            i = 0
            cur_opt = ''
            for c in short_opt:
                if c != ':':
                    cur_opt = "-{}".format(c)
                    d_option = opt_map[cur_opt] if cur_opt in opt_map else None
                    has_value = True if short_opt[i+1] == ':' else False
                    self.add_opt(cur_opt, d_option, has_value)
                
        if type(long_opt).__name__ == 'list' and len(long_opt) > 0:
            for opt in long_opt:
                cur_opt = "--{}".format(opt)
                d_option = opt_map[cur_opt] if cur_opt in opt_map else None
                has_value = True if opt[-1:] == '=' else False
                self.add_opt(cur_opt, d_option, has_value)
    
    def parse(self, opt_group = 'default'):
        if opt_group not in self._options:
            raise CmdOptParserUndefined('Undefined group {}'.format(opt_group))  
        for opt_name, opt_args in self._options[opt_group].items():            
            self.add_argument(opt_name, **opt_args)
            
        set_opts, unreg_opts = self.parse_known_args()
        self._set_opts       = vars(set_opts)
        self._unreg_opts     = unreg_opts
                
        return (self._set_opts, self._unreg_opts)

    def opt_defined(self, option_name):
        return option_name in self._set_opts and self._set_opts[option_name] != False        
    
    def get_opt(self, option_name):        
        return self._set_opts[option_name] if self.opt_defined(option_name) == True else False 
