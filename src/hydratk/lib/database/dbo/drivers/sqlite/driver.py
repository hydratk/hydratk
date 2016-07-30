# -*- coding: utf-8 -*-
"""DBO SQlite driver

.. module:: lib.database.dbo.drivers.sqlite.driver
   :platform: Unix
   :synopsis: DBO SQlite driver
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import sqlite3
import os
from hydratk.lib.database.dbo import dbodriver 

class DBODriver(dbodriver.DBODriver):
    """Class DBODriver
    """
    
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
        """Method detects if is running in memory or file mode
        
        Args:   
           dsn (str): dsn
           
        Returns:
           bool: result
                
        """ 
                
        result = True
        if dsn.find('::') > 0:
            self._mode = 'MEMORY'
        elif dsn.find(':') > 0:
            self._mode = 'FILE'
        else:
            result = False
        
        return result
        
    def _parse_dsn(self, dsn): 
        """Method parses dsn
        
        Args:   
           dsn (str): dsn
           
        Returns:
           bool: True
           
        Raises:
           exception: Exception
                
        """ 
                
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
        """Method sets driver options
        
        Args:   
           driver_option (dict): driver options
           
        Returns:
           void
                
        """ 
                
        for optname, optval in driver_options.items():
            if optname in self._driver_options:
                self._driver_options[optname] = optval
            
        
    def connect(self):
        """Method connects to database
        
        Args:   
           none
           
        Returns:
           void
                
        """ 
                
        if (self._mode == 'FILE' and os.path.exists(os.path.dirname(self._dbfile)) == False):
            os.makedirs(os.path.dirname(self._dbfile))       
        self._dbcon = sqlite3.connect(
                                      self._dbfile, 
                                      self._driver_options['timeout'],
                                      self._driver_options['detect_types']
                                    )                    
        self._cursor = self._dbcon.cursor()              
    
    def close(self):
        """Method disconnects from database
        
        Args:  
           none 
           
        Returns:
           void
           
        Raises:
           exception: DBODriverException
                
        """ 
                
        if type(self._dbcon).__name__ == 'Connection':
            self._dbcon.close()
        else:
            raise dbodriver.DBODriverException('Not connected')  
                
    def commit(self):
        """Method commits transaction
        
        Args:
           none   
           
        Returns:
           void
           
        Raises:
           exception: DBODriverException
                
        """ 
                
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
        """Method executes query
        
        Args:   
           sql (str): SQL query
           parameters (args): query parameters
           
        Returns:
           obj: cursor
                
        """ 
                
        return self._cursor.execute(sql, *parameters)
        
    def quote(self):
        pass
    
    def rollback(self):
        """Method rollbacks transaction
        
        Args: 
           none  
           
        Returns:
           void
           
        Raises:
           exception: DBODriverException
                
        """ 
                
        if type(self._dbcon).__name__ == 'Connection':
            self._dbcon.rollback()
        else:
            raise dbodriver.DBODriverException('Not connected') 
    
    def set_attribute(self):
        pass

    def __getitem__(self, name):
        """Method gets item
        
        Args:   
           name (str): item name
           
        Returns:
           obj: item value
                
        """ 
                
        if hasattr(sqlite3, name):
            return getattr(sqlite3, name)
            
    def __getattr__(self,name):
        """Method gets attribute
        
        Args:   
           name (str): attribute name
           
        Returns:
           obj: attribute value
                
        """ 
                
        if type(self._dbcon).__name__ == 'Connection':    
            if hasattr(self._dbcon, name):
                return getattr(self._dbcon,name)
            
            if hasattr(sqlite3, name):
                return getattr(sqlite3,name) 
            
    def table_exists(self, table_name):
        """Method checks if table exists
        
        Args:   
           table_name (str): table
           
        Returns:
           bool: result (not working now)
                
        """ 
                
        if table_name is not None and table_name != '':
            query = "SELECT count(*) found FROM sqlite_master where type='table' and tbl_name=?"
            recs = self._cursor.execute(query, [table_name]).fetchone()
            result = True if (recs[0] == 1) else False
        return result
        
    def database_exists(self):
        """Method checks if database exists
        
        Args: 
           none 
           
        Returns:
           bool: result
                
        """ 
                
        result = False
        if self._mode == 'FILE':
            if os.path.exists(self._dbfile) and os.path.isfile(self._dbfile) and os.path.getsize(self._dbfile) > 0:
                result = True
        else: #MEMORY mode
            result = True
        
        return result
    
    def remove_database(self):
        """Method deletes database file
        
        Args:
           none   
           
        Returns:
           bool: result
                
        """ 
                
        result = False
        if self._mode == 'FILE':
            if os.path.exists(self._dbfile) and os.path.isfile(self._dbfile):
                os.unlink(self._dbfile)
                result = True
        return result
    
    def erase_database(self):
        """Method drops database
        
        Args:  
           none 
           
        Returns:
           void
                
        """ 
                
        tables = list(self._cursor.execute("select name from sqlite_master where type is 'table'"))
        query = ''
        for col in tables:
            query += "drop table if exists {0};".format(col[0])        
        self._cursor.executescript(query)
        self._cursor.execute("VACUUM;")
    
    def result_as_dict(self, state):   
        """Method enables query result in dictionary form
        
        Args:   
           state (bool): enable dictionary
           
        Returns:
           void
           
        Raises:
           error: TypeError
                
        """ 
                    
        if state in (True, False):
            self._result_as_dict = state
            if state == True:                
                self._dbcon.row_factory = self.dict_factory
                self._cursor = self._dbcon.cursor()
            else:
                self._dbcon.row_factory = None
                self._cursor = self._dbcon.cursor()
        else:
            raise TypeError('Boolean value expected')
        