# -*- coding: utf-8 -*-
"""This code is part of Hydra Toolkit library

.. module:: database.dbodriver
   :platform: Unix
   :synopsis: DBODriver abstract class
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

from abc import ABCMeta, abstractmethod
import inspect
import sys
import os

class DBODriver(object):
    __metaclass__ = ABCMeta
    
    _cursor         = None
    _dbcon          = None
    _result_as_dict = True
    _dsn            = None 
    _driver_options = {}
    _username       = None
    _password       = None

    @property
    def dbcon(self):        
        return self._dbcon 
    
    @property
    def cursor(self):
        return self._cursor
    
    def __init__(self, dsn, username=None, password=None, driver_options={}, autoconnect = True):        
        '''
        Constructor
        '''
        self._dsn            = dsn
        self._username       = username
        self._password       = password
        if len(driver_options) > 0:
            self._apply_driver_options(driver_options)
                    
        if self._parse_dsn(dsn) is not True:
            raise Exception("Error initialize database driver, dsn parse {0} error".format(dsn))
        
        try:
            if autoconnect == True:
                self.connect()
            
        except Exception as e:
            exc = DBODriverException(str(e))
            exc.parent_exc = e
            raise exc 
    
        
    @abstractmethod
    def _parse_dsn(self, dsn):
        '''
        Parses driver specific dsn string
                
        Args: 
           dsn (string): driver specific dsn format
                              
        Raises:
           DBODriverException: on error                     
       '''
        pass
     
    @abstractmethod
    def _apply_driver_options(self):
        pass
    
    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
 
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass
    
    @abstractmethod
    def commit(self):
        pass
    
    @abstractmethod
    def error_code(self):
        pass
    
    @abstractmethod
    def error_info(self):
        pass
    
    @abstractmethod
    def qexec(self):
        pass
    
    @abstractmethod
    def get_attribute(self):
        pass    
    
    @abstractmethod
    def in_transaction(self):
        pass
    
    @abstractmethod
    def last_insert_id(self):
        pass
    
    @abstractmethod
    def prepare(self):
        pass
    
    @abstractmethod
    def query(self):
        pass
    
    @abstractmethod
    def quote(self):
        pass
    
    @abstractmethod
    def rollback(self):
        pass
    
    @abstractmethod
    def set_attribute(self):
        pass
    
    @abstractmethod
    def table_exists(self, table_name):
        pass
    
    @abstractmethod
    def database_exists(self):
        pass
    
    @abstractmethod
    def remove_database(self):
        pass
    

class DBODriverStatement(object):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def bind_column(self):
        pass
    
    @abstractmethod
    def bind_param(self):
        pass
    
    @abstractmethod
    def bind_value(self):
        pass
    
    @abstractmethod
    def close_cursor(self):
        pass
    
    @abstractmethod
    def column_count(self):
        pass
    
    @abstractmethod
    def debug_dump_params(self):
        pass
    
    @abstractmethod
    def error_info(self):
        pass
    
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def fetch(self):
        pass
    
    @abstractmethod
    def fetch_all(self):
        pass
    
    @abstractmethod
    def fetch_column(self):
        pass
    
    @abstractmethod
    def fetch_object(self):
        pass
    
    @abstractmethod
    def get_attribute(self):
        pass
    
    @abstractmethod
    def get_column_meta(self):
        pass
    
    @abstractmethod
    def next_rowset(self):
        pass
    
    @abstractmethod
    def row_count(self):
        pass
    
    @abstractmethod
    def set_attribute(self):
        pass
    
    @abstractmethod
    def set_fetch_mode(self):
        pass
    

class DBODriverException(Exception):
    _error_info = {}
    _call_path  = None
    _message    = None
    _module     = None 
    _func       = None  
    _file       = None
    _line       = None
    _parent_exc = None
    
    @property
    def message(self):
        return self._message
    
    @property
    def call_path(self):
        return self._call_path
        
    @property
    def file(self):
        return self._file
    
    @property
    def line(self):
        return self._line

    @property
    def func(self):
        return self._func
    
    @property
    def module(self):
        return self._module    
        
    @property
    def parent_exc(self):
        return self._parent_exc
    
    @parent_exc.setter
    def parent_exc(self,exc):
        self._parent_exc = exc
    
    def __init__(self, msg):
        self._message   = msg
        trace           = self.get_trace(2)
        self._file      = trace['file']
        self._line      = trace['line']
        self._call_path = trace['call_path']
        self._func      = trace['func']
        self._module    = trace['module']
        
    def __str__(self):
        return repr(self._message)
    
    def get_trace(self, level):
        fname = sys._getframe(level).f_code.co_filename
        modname = os.path.basename(fname)
        modarg = modname.split('.')                   
        frm = inspect.stack()[1]
        mod = inspect.getmodule(frm[0])
        call_path = mod.__name__ if hasattr(mod,'__name__') else '__main__'        
        return {'file': sys._getframe(1).f_code.co_filename,
                'line' : sys._getframe(1).f_lineno,
                'module' : modarg[0],
                'func': sys._getframe(1).f_code.co_name,
                'call_path' : call_path  
                }  