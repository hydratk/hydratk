# -*- coding: utf-8 -*-
"""Useful module for creating string macros and enhancements

.. module:: lib.parser.smp
   :platform: Unix
   :synopsis: Simple macro parser
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
import re

class MacroParser(object):
    """Class MacroParser
    """
    _regexp = []
    _hooks = {}
    _default_hook = None

    def __init__(self, regexp=None):
        if regexp == None:
            regexp = [
                      {'regexp' : r'\$\(([a-z,A-Z,0-9,_]*)\)', 'processor' : self._var_processor},
                      {'regexp' : r'\$\(([a-z,A-Z,0-9,_]*)\(([a-z,A-Z,0-9,_,=,\s,\',\",\,]*)\)\)', 'processor' : self._fn_processor}
                     ]
        self.add_regexp(regexp)

    def add_regexp(self, regexp, replace = False):
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

    def add_var_hook(self, name, cb = None):
        """Method registers macro variable hook

        Args:
           name (str): macro
           cb (callable): callback

        Returns:
           void

        """

        if type(name).__name__ == 'dict':
            self._hooks.update(name)
            
        elif type(name).__name__ == 'str' and callable(cb):
            self._hooks[name] = cb
            
        

    def set_default_var_hook(self, cb):
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
           content (str): parsed string

        """        
        if len(self._regexp) > 0:
            for regexp in self._regexp:                
                content =  re.sub(regexp['regexp'], regexp['processor'], content)
        return content

    def _var_processor(self, match):
        """Method executes macro string

        Args:
           match (obj): regexp group

        Returns:
           mixed: callback result
                      
        Raises:  
        """
        mdef = match.group(1).strip()
        if mdef in self._hooks:
            return self._hooks[mdef]()
        elif callable(self._default_hook):
            return self._default_hook(mdef)
        else:
            raise Exception('Undefined hook')

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
            raise Exception('Undefined hook')
