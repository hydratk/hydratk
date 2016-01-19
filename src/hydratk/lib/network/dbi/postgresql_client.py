# -*- coding: utf-8 -*-
"""This code is part of Hydra Toolkit library

.. module:: network.dbi.postgresql_client
   :platform: Unix
   :synopsis: PostgreSQL DB client
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
from psycopg2 import Error, connect
from string import replace

class DBClient():
    
    _mh = None
    _client = None
    _host = None
    _port = None
    _sid = None
    _user = None
    _passw = None
    
    def __init__(self):
        """Class constructor
           
        Called when the object is initialized          
           
        """    
        
        self._mh = MasterHead.get_head() 
        
    @property
    def client(self):
        """ PostgreSQL client property getter """
        
        return self._client
    
    @property
    def host(self):
        """ server host property getter """
        
        return self._host
    
    @property
    def port(self):
        """ server port property getter """
        
        return self._port
    
    @property
    def sid(self):
        """ server SID property getter """
        
        return self._sid
    
    @property
    def user(self):
        """ username property getter """
        
        return self._user
    
    @property
    def passw(self):
        """ user password property getter """
        
        return self._passw           
        
    def connect(self, host=None, port=5432, sid=None, user=None, passw=None, db_file=None):
        """Method connects to database
        
        Args:            
           host (str): hostname
           port (int): port
           sid (str): db instance
           user (str): username
           passw (str): password
             
        Returns:
           bool: result
           
        Raises:
           event: dbi_before_connect
           event: dbi_after_connect
                
        """        
        
        try:
                    
            message = '{0}/{1}@{2}:{3}/{4}'.format(user, passw, host, port, sid)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_dbi_connecting', message), self._mh.fromhere())
            
            ev = event.Event('dbi_before_connect', host, port, sid, user, passw, db_file)
            if (self._mh.fire_event(ev) > 0):
                host = ev.argv(0)
                port = ev.argv(1)
                sid = ev.argv(2)
                user = ev.argv(3)
                passw = ev.argv(4)
                db_file = ev.argv(5)               
            
            if (ev.will_run_default()):
                self._host = host     
                self._port = port           
                self._sid = sid
                self._user = user
                self._passw = passw
                
                self._client = connect(host=self._host, port=self._port, database=self._sid,
                                       user=self._user, password=self._passw)                   

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
                cur = self._client.cursor()    
                
                if (bindings != None):
                    query = replace(query, '?', '%s')
                    cur.execute(query, tuple(bindings))
                else:
                    cur.execute(query)

                if (cur.description == None):
                    return True, None
                columns = [i[0].lower() for i in cur.description]                    
                rows = [dict(zip(columns, row)) for row in cur]          
                
                if (fetch_one):
                    rows = rows[0] if (len(rows) > 0) else []            
            
            cur.close()  
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_dbi_query_executed'), self._mh.fromhere())
            ev = event.Event('dbi_after_exec_query', True, rows)
            self._mh.fire_event(ev) 
                                      
            return True, rows
        
        except Error, ex:
            self._mh.dmsg('htk_on_error', 'database error: {0}'.format(ex), self._mh.fromhere())
            return False, None             