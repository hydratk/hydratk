# -*- coding: utf-8 -*-
"""This code is part of Hydra Toolkit library

.. module:: network.dbi.sqlite_client
   :platform: Unix
   :synopsis: SQLite DB client
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
dbi_before_connect
dbi_after_connect
dbi_before_exec_query
dbi_after_exec_query

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from sqlite3 import Error, connect, Row

class DBClient():
    
    _mh = None
    _client = None
    _db_file = None
    
    def __init__(self):
        """Class constructor
           
        Called when the object is initialized          
           
        """    
        
        self._mh = MasterHead.get_head() 
        
    @property
    def client(self):
        """ SQLite client property getter """
        
        return self._client
    
    @property 
    def db_file(self):
        """ database file property getter """
        
        return self._db_file
        
    def connect(self, db_file):            
        """Method connects to database
        
        Args:            
           db_file (str): path to database file
             
        Returns:
           bool: result
           
        Raises:
           event: dbi_before_connect
           event: dbi_after_connect
                
        """        
        
        try:
                    
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_dbi_connecting', db_file), self._mh.fromhere())
            
            ev = event.Event('dbi_before_connect', db_file)
            if (self._mh.fire_event(ev) > 0):
                db_file = ev.argv(0)               
            
            if (ev.will_run_default()):
                self._db_file = db_file
                self._client = connect(self._db_file)
                self._client.execute('PRAGMA foreign_keys = ON')               

            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_dbi_connected'), self._mh.fromhere())
            ev = event.Event('dbi_after_connect')
            self._mh.fire_event(ev)   
                        
            return True
    
        except Error, ex:
            self._mh.dmsg('htk_on_error', 'database error: {0}'.format(ex), self._mh.fromhere())
            return False    
        
    def disconnect(self):
        """Method disconnects from database
        
        Args:            
             
        Returns:
           bool: result
                
        """        
        
        try:
        
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_dbi_disconnected'), self._mh.fromhere())
            self._client.close()
            
            return True
        
        except Error, ex:
            self._mh.dmsg('htk_on_error', 'database error: {0}'.format(ex), self._mh.fromhere())
            return False    
        
    def exec_query(self, query, bindings=None, fetch_one=False):
        """Method executes query
        
        Args:            
           query (str): query, binded variables are marked with ?
           bindings (list): query bindings 
           fetch_one (bool): fetch one row only
             
        Returns:
           tuple: result (bool), rows (list) (accessible by column name)
          
        Raises:
           event: dbi_before_exec_query
           event: dbi_after_exec_query   
                
        """        
        
        try:
                    
            message = query + ' binding: {0}'.format(bindings) if (bindings != None) else query
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_dbi_executing_query', message), self._mh.fromhere())
            
            ev = event.Event('dbi_before_exec_query', query, bindings, fetch_one)
            if (self._mh.fire_event(ev) > 0):
                query = ev.argv(0)
                bindings = ev.argv(1)
                fetch_one = ev.argv(2)          

            if (ev.will_run_default()):
                self._client.row_factory = Row
                cur = self._client.cursor()    
                
                if (bindings != None):
                    cur.execute(query, tuple(bindings))
                else:
                    cur.execute(query)      
                
                if (fetch_one):
                    rows = cur.fetchone()
                else:
                    rows = cur.fetchall()                
            
            cur.close()  
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_dbi_query_executed'), self._mh.fromhere())
            ev = event.Event('dbi_after_exec_query', True, rows)
            self._mh.fire_event(ev) 
                                      
            return True, rows
        
        except Error, ex:
            self._mh.dmsg('htk_on_error', 'database error: {0}'.format(ex), self._mh.fromhere())
            return False, None                    