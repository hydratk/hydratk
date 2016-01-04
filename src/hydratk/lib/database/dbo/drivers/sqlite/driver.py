# -*- coding: utf-8 -*-
"""This code is part of Hydra Toolkit library

.. module:: database.dbo.drivers.sqlite.driver
   :platform: Unix
   :synopsis: DBO SQlite driver
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import sqlite3
import os
from hydratk.lib.database.dbo import dbodriver 

class DBODriver(dbodriver.DBODriver):
    _mode           = 'FILE' #MEMORY
    _dbfile         = None
    _driver_options = {
                   'timeout'           : 5.0,
                   'detect_types'      : 0,
                   'isolation_level'   : None, #available “DEFERRED”, “IMMEDIATE” or “EXCLUSIVE”
                   'check_same_thread' : None,
                   'factory'           : 'Connection',
                   'cached_statements' : 100
                  }
    
    def _detect_mode(self, dsn):
        result = True
        if dsn.find('::') > 0:
            self._mode = 'MEMORY'
        elif dsn.find(':') > 0:
            self._mode = 'FILE'
        else:
            result = False
        return result
        
    def _parse_dsn(self, dsn): 
        if self._detect_mode(dsn):
            if self._mode == 'FILE':
                dbfile = dsn.split(':')[1]
                if dbfile != '':
                    self._dbfile = dbfile
                else:
                    raise Exception("Error initialize database driver, dsn parse {0} error, database file cannot be an empty string".format(dsn))
            elif self._mode == 'MEMORY':
                self._dbfile = ':memory:'
        return True
    
    def _apply_driver_options(self, driver_options):
        for optname, optval in driver_options.items():
            if optname in self._driver_options:
                self._driver_options[optname] = optval
            
        
    def connect(self):        
        self._dbcon = sqlite3.connect(
                                      self._dbfile, 
                                      self._driver_options['timeout'],
                                      self._driver_options['detect_types']
                                    )
        self._cursor = self._dbcon.cursor()              
    
    def close(self):
        if type(self._dbcon).__name__ == 'Connection':
            self._dbcon.close()
        else:
            raise dbodriver.DBODriverException('Not connected')  
                
    def commit(self):
        if type(self._dbcon).__name__ == 'Connection':
            self._dbcon.commit()
        else:
            raise dbodriver.DBODriverException('Not connected')    
             
    def error_code(self):
        pass
    
    def error_info(self):
        pass
    
    def qexec(self):
        pass
    
    def get_attribute(self):
        pass    
    
    def in_transaction(self):
        pass
    
    def last_insert_id(self):
        pass
    
    def prepare(self):
        pass
    
    def query(self):
        pass
    
    def execute(self, sql, *parameters):
        return self._cursor.execute(sql, *parameters)
        
    def quote(self):
        pass
    
    def rollback(self):
        if type(self._dbcon).__name__ == 'Connection':
            self._dbcon.rollback()
        else:
            raise dbodriver.DBODriverException('Not connected') 
    
    def set_attribute(self):
        pass

    def __getitem__(self, name):
        if hasattr(sqlite3, name):
            return getattr(sqlite3, name)
            
    def __getattr__(self,name):
        if type(self._dbcon).__name__ == 'Connection':    
            if hasattr(self._dbcon, name):
                return getattr(self._dbcon,name)
            
            if hasattr(sqlite3, name):
                return getattr(sqlite3,name) 
            
    def table_exists(self, table_name):
        result = False
        if table_name is not None and table_name != '':
            query = "SELECT count(*) found FROM sqlite_master where type='table' and tbl_name=?"
            self._cursor.execute(query, table_name)
            print(self._cursor.fetchone())
        return result
        
    def database_exists(self):
        result = False
        if self._mode == 'FILE':
            if os.path.exists(self._dbfile) and os.path.isfile(self._dbfile) and os.path.getsize(self._dbfile) > 0:
                result = True
        else: #MEMORY mode
            result = True
        
        return result
    
    def remove_database(self):
        result = False
        if self._mode == 'FILE':
            if os.path.exists(self._dbfile) and os.path.isfile(self._dbfile):
                result = os.unlink(self._dbfile)
        return result