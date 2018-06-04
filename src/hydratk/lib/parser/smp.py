# -*- coding: utf-8 -*-
"""Useful module for creating string macros and enhancements

.. module:: lib.parser.smp
   :platform: Unix
   :synopsis: Simple macro parser
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import re
import time

class MacroParser(object):
    """Class MacroParser
    """

    _regexp            = []
    _hooks             = {}
    _hook_result_cache = {}
    _default_hook      = None


    def __init__(self, regexp=None):
        """Class constructor

        Called when object is initialized

        Args:
           regexp (list): regexp matches required by add_regexp

        """

        from hydratk.core.masterhead import MasterHead

        if regexp == None:
            regexp = [
                      {'regexp' : r'\$\(([^\x28-\x29]+)\)', 'processor' : self._var_processor},                     
                      {'regexp' : r'\$\(([^\x28-\x29]+)\(([^\x28-\x29]+)\)\)', 'processor' : self._fn_processor}                    
                     ]
        self.add_regexp(regexp)

        self._mh = MasterHead.get_head()

    def add_regexp(self, regexp, replace=False, prepend=False):
        """Method adds list of regexp matches
        
        Args:
           regexp (list): regexp matches in format [{'regexp' : r'expression', 'processor' : callable }] 
           replace (bool) : whether to add or replace current regexp list        

        Returns:
           void

        """

        if type(regexp).__name__ == 'list':
            if replace == True:
                self._regexp = regexp
            else:
                if prepend == True:
                    self._regexp = regexp + self._regexp
                else:
                    self._regexp += regexp

    def add_var_hooks(self, *args, **kwargs):
        """Method registers macro hooks for each variable

        Macro is identified by name and contains callback

        Args:
           args (args): arguments
           kwargs (kwargs): key value arguments

        Returns:
           void

        """

        for hdata in args:
            for mdef, cb in hdata.items():
                if type(mdef).__name__ == 'str' and mdef != '' and callable(cb):
                    self._hooks[mdef] = cb

        for mdef, cb in kwargs.items():
            if type(mdef).__name__ == 'str' and mdef != '' and callable(cb):
                self._hooks[mdef] = cb

    def add_var_hook(self, name, cb = None, hook_result_cache = False):
        """Method registers macro variable hook

        Args:
           name (str): macro
           cb (callable): callback
           hook_result_cache (mixed) : False for none, otherwise dict

        Returns:
           void

        """
        hook_set = False 
        if type(name).__name__ == 'dict':
            self._hooks.update(name)            
            hook_set = True   
        elif type(name).__name__ == 'str':
            self._hooks[name] = cb
            hook_set = True
            

        if hook_set == True and type(hook_result_cache).__name__ == 'dict':
            cache_data = {}
            cache_data['ttl'] = hook_result_cache['ttl'] if 'ttl' in hook_result_cache else None
            cache_data['created'] = False
            self._hook_result_cache[name] = cache_data
                             

    def set_default_var_hook(self, cb):
        """Method sets default hook

        Args:
           cb (callable): callback

        Returns:
           bool

        """

        result = False
        if callable(cb):
            self._default_hook = cb
            result = True

        return result

    def parse(self, content):
        """Method parses macro string

        Args:
           content (str): macro string

        Returns:
           str: parsed string

        """

        if len(self._regexp) > 0:            
            for regexp in self._regexp:                                
                while True:
                    content, match  =  re.subn(regexp['regexp'], regexp['processor'], content, re.UNICODE)
                    if match == 0:
                        break

        return content

    def _var_processor(self, match):
        """Method executes macro string

        Args:
           match (obj): regexp group

        Returns:
           mixed: callback result
                      
        Raises:
          Exception: Undefined hook

        """

        mdef = match.group(1).strip()
        if mdef in self._hooks:
            if mdef in self._hook_result_cache: #we have cache definition
                if self._hook_result_cache[mdef]['created'] == False:
                    self._hook_result_cache[mdef]['value'] = self._hooks[mdef]() if callable(self._hooks[mdef]) else self._hooks[mdef]
                    self._hook_result_cache[mdef]['created'] = True
                    
                elif 'expire' in self._hook_result_cache[mdef]:
                    if self._hook_result_cache[mdef]['expire'] <= self._hook_result_cache[mdef]['ttl'] + time.time(): #expirec cache
                        #rebuilding cache
                        self._hook_result_cache[mdef]['value'] = self._hooks[mdef]() if callable(self._hooks[mdef]) else self._hooks[mdef]
                        self._hook_result_cache[mdef]['expire'] = self._hook_result_cache[mdef]['ttl'] + time.time()
                    
                #valid cache
                return self._hook_result_cache[mdef]['value']
                    
            else:                              
                return self._hooks[mdef]() if callable(self._hooks[mdef]) else self._hooks[mdef]
        elif callable(self._default_hook):
            return self._default_hook(mdef)
        else:
            raise Exception(self._mh._trn.msg('htk_lib_undefined_hook'))

    def _fn_processor(self, match):
        """Method is processing macro function

        Args:
           match (obj): regexp match group

        Returns:
           obj: callback result
           
        Raises:
           Exception: Undefined hook
              
        """

        fn = match.group(1).strip()
        args   = []
        kwargs = {}
        rparams = match.group(2).strip().split(',')
        for p in rparams:
            p = p.strip()
            m = re.match(r'([a-z,A-Z,0-9,_]*)\s?=\s?(.*)', p)
            if m is not None:
                val = m.group(2)
                if val[0] == val[-1] and val.startswith(("'", '"')):
                    val = val[1:-1]
                kwargs[m.group(1)] = val
            else:
                if p[0] == p[-1] and p.startswith(("'", '"')):
                    p = p[1:-1]
                args.append(p)        
        if fn in self._hooks:
            return self._hooks[fn](*args,**kwargs)
        elif callable(self._default_hook):
            return self._default_hook(*args,**kwargs)
        else:
            raise Exception(self._mh._trn.msg('htk_lib_undefined_hook'))
