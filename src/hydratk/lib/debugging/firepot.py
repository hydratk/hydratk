# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit library

.. module:: lib.debugging.firepot
   :platform: Unix
   :synopsis: Raw implementation of FireLogger protocol for debugging purposes.
              Basic info was taken from https://github.com/binaryage/firelogger/wiki
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

from hydratk.lib.string.operation import str_split,file_get_contents
import time
import math
import datetime as dt
import json
import sys
import random
import pprint
import collections
import hashlib


class FirePot(object):
    _items = []
    _enabled = False
    _levels = ['debug', 'warning', 'info', 'error', 'critical']
    _name = 'python'
    _counter = 0
    _style = ''
    
    @staticmethod
    def enable(state):
        FirePot._enabled = state if state in (True,False) else False 
    
    @staticmethod
    def enabled():
        return FirePot._enabled    
        
    
    '''level,fmt, object....'''
    @staticmethod 
    def log(*args): 
        args = list(args)
        if not FirePot._enabled: return False
        fmt = ''
        level = 'debug'
        if type(args[0]).__name__ == 'str' and args[0] in FirePot._levels:
            level = args.pop(0)
        
        if type(args[0]).__name__ == 'str':
            fmt = args.pop(0)
            
        ctime = time.time()
                 
        fraction = str(ctime).split('.')[1]
        item = {                
                "name" : FirePot._name,
                "args": [],
                "level": level,
                "timestamp": ctime,
                "order": FirePot._counter,
                "time": time.strftime('%H:%I:%S') +'.'+ fraction[:3],
                "template": fmt,
                "message": fmt,                
                "pathname": sys._getframe(1).f_code.co_filename,
                "lineno": sys._getframe(1).f_lineno
                }
            
        if FirePot._style != '':
            item['style'] = FirePot._style '''CSS snippet'''
        
        FirePot._items.append(item)
        FirePot._counter += 1
        return True
        
    @staticmethod
    def flush_items():
        FirePot._items = []
        
    
    @staticmethod
    def push_item(item):
        pass
    
        
    @staticmethod
    def get_headers():
        result = False
        if len(FirePot._items) > 0:
            result = collections.OrderedDict()
            json_buf = json.dumps({'logs': FirePot._items})                                  
            json_buf = json_buf.encode('utf-8')                                    
            json_buf = json_buf.encode('base64')            
            id = int(hashlib.md5(json_buf).hexdigest(), 16)            
            res = str_split(json_buf,76) '''RFC 2045'''            
            k = 0
            for v in res:
                if v != "\n":
                    result["FireLogger-"+str(id)+"-"+str(k)] = v
                    k = k + 1
            
        return result
        