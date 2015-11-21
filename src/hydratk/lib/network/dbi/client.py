# -*- coding: utf-8 -*-
"""This code is part of Hydra Toolkit library

.. module:: network.dbi.client
   :platform: Unix
   :synopsis: Generic DB client for databases: SQLite, Oracle, MySQL, PostgreSQL
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
dbi_before_connect
dbi_after_connect
dbi_before_exec_query
dbi_after_exec_query
dbi_before_call_proc
dbi_after_call_proc

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
import string
import sqlite3
import cx_Oracle
import MySQLdb
import psycopg2

default_ports = {
  'ORACLE'    : 1521,
  'MYSQL'     : 3306,
  'POSTGRESQL': 5432
}

data_types = {
  'ORACLE': {
     'int'      : cx_Oracle.NUMBER,
     'float'    : cx_Oracle.NUMBER,
     'string'   : cx_Oracle.STRING,
     'timestamp': cx_Oracle.TIMESTAMP,
     'clob'     : cx_Oracle.CLOB,
     'blob'     : cx_Oracle.BLOB
  }              
}

class DBClient:
    
    _mh = None
    _client = None
    _engine = None;
    _host = None;
    _port = None;
    _sid = None;
    _user = None;
    _passw = None;
    _db_file = None;
    
    def __init__(self, engine='SQLITE'):
        """Class constructor
           
        Called when the object is initialized 
        
        Args:
           engine (str): database engine, SQLITE|ORACLE|MYSQL|POSTGRESQL           
           
        """         
        
        self._mh = MasterHead.get_head()
        self._engine = engine.upper() 
        
        if (self._engine not in ('SQLITE', 'ORACLE', 'MYSQL', 'POSTGRESQL')):
            self._mh.dmsg('htk_on_error', self._mh.trn.msg('htk_dbi_unknown_engine', self._engine), self._mh.fromhere())
            return None        
        
    def connect(self, host=None, port=None, sid=None, user=None, passw=None, db_file=None):
        """Method connects to database
        
        Args:            
           host (str): hostname, used for Oracle, MySQL, PostgreSQL only
           port (int): port, used for Oracle, MySQL, PostgreSQL only
           sid (str): db instance, used for Oracle, MySQL, PostgreSQL only
           user (str): username, used for Oracle, MySQL, PostgreSQL only
           passw (str): password, used for Oracle, MySQL, PostgreSQL only 
           db_file (str): path to database file, used for SQLite only
             
        Returns:
           bool: result
           
        Raises:
           event: dbi_before_connect
           event: dbi_after_connect
                
        """        
        
        try:
                    
            if (self._engine != 'SQLITE'):
                self._port = port if (port != None) else default_ports[self._engine]
                message = '{0}/{1}@{2}:{3}/{4}'.format(user, passw, host, self._port, sid)
            else:
                message = '{0}'.format(db_file)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_dbi_connecting', message), self._mh.fromhere())
            
            ev = event.Event('dbi_before_connect', host, self._port, sid, user, passw, db_file)
            if (self._mh.fire_event(ev) > 0):
                host = ev.argv(0)
                self.port = ev.argv(1)
                sid = ev.argv(2)
                user = ev.argv(3)
                passw = ev.argv(4)
                db_file = ev.argv(5)               
            
            if (ev.will_run_default()):
                if (self._engine == 'SQLITE'):
                    self._db_file = db_file
                    self._client = sqlite3.connect(self._db_file)
                    self._client.execute('PRAGMA foreign_keys = ON')
                else:
                    self._host = host                
                    self._sid = sid
                    self._user = user
                    self._passw = passw
                
                    if (self._engine == 'ORACLE'):
                        dsn_str = cx_Oracle.makedsn(self._host, self.port, self._sid)
                        self._client = cx_Oracle.connect(dsn=dsn_str, user=self._user, password=self._passw)
                    elif (self._engine == 'MYSQL'):
                        self._client = MySQLdb.connect(host=self._host, port=self.port, db=self._sid, user=self._user, 
                                                       passwd=self._passw)
                    elif (self._engine == 'POSTGRESQL'):
                        self._client = psycopg2.connect(host=self._host, port=self.port, database=self._sid,
                                                        user=self._user, password=self._passw)

            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_dbi_connected'), self._mh.fromhere())
            ev = event.Event('dbi_after_connect')
            self._mh.fire_event(ev)   
                        
            return True
        
        except (sqlite3.Error, cx_Oracle.Error, MySQLdb.Error, psycopg2.Error), ex:
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
        
        except (sqlite3.Error, cx_Oracle.Error, MySQLdb.Error, psycopg2.Error), ex:
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
                if (self._engine == 'SQLITE'):
                    self._client.row_factory = sqlite3.Row
            
                cur = self._client.cursor()    
                
                if (bindings != None):
                    if (self._engine == 'ORACLE'):
                        for i in xrange(0, len(bindings)):
                            query = string.replace(query, '?', ':{0}'.format(i+1), 1)
                    elif (self._engine in ('MYSQL', 'POSTGRESQL')):
                        query = string.replace(query, '?', '%s')

                    cur.execute(query, tuple(bindings))
                else:
                    cur.execute(query)
                
                if (self._engine in ('ORACLE', 'MYSQL', 'POSTGRESQL')):
                    if (cur.description == None):
                        return True, None
                    columns = [i[0].lower() for i in cur.description]
                    rows = [dict(zip(columns, row)) for row in cur]           
                
                if (fetch_one):
                    if (self._engine == 'SQLITE'):
                        rows = cur.fetchone()
                    else:
                        rows = rows[0]
                else:
                    if (self._engine == 'SQLITE'):
                        rows = cur.fetchall()                
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_dbi_query_executed'), self._mh.fromhere())
            ev = event.Event('dbi_after_exec_query', True, rows)
            self._mh.fire_event(ev)                             
            return True, rows
        
        except (sqlite3.Error, cx_Oracle.Error, MySQLdb.Error, psycopg2.Error), ex:
            self._mh.dmsg('htk_on_error', 'database error: {0}'.format(ex), self._mh.fromhere())
            return False, None 
        
    def call_proc(self, p_name, param_names=[], i_values={}, o_types={}, type='proc', ret_type=None):
        """Method calls procedure/function from database
        
        Supported for ORACLE, MySQL only
        
        Args:
           p_name (str): procedure name
           param_names (list): parameter names (input, output)
           i_values (dict): input parameter values
           o_types (dict): output parameter types  
           type (str): code type, func|function|proc|procedure
           ret_type (str): return type, string, optional, used for function only                    
             
        Returns:
           tuple: result (bool) (for function only), params (list)
           
        Raises:
           event: dbi_before_call_proc
           event: dbi_after_call_proc
                
        """        
        
        try:                    
        
            message = p_name + ' param: {0}'.format(i_values) if (len(i_values) > 0) else p_name
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_dbi_calling_proc', message), self._mh.fromhere())
            
            ev = event.Event('dbi_before_call_proc', p_name, param_names, i_values, o_types, type, ret_type)
            if (self._mh.fire_event(ev) > 0):
                p_name = ev.argv(0)
                param_names = ev.argv(1)
                i_values = ev.argv(2)   
                o_types = ev.argv(3)
                type = ev.argv(4)
                ret_type = ev.argv(5)                          
            
            if (ev.will_run_default()):
                if (self._engine in ('SQLITE', 'POSTGRESQL')):
                    self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_dbi_unknown_method', self._engine), self._mh.fromhere())
                    return None
                elif (type not in ('func', 'function', 'proc', 'procedure')):
                    self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_dbi_unknown_type', self.type), self._mh.fromhere())
                    return None
                
                cur = self._client.cursor()
            
                params = []
                for name in param_names:
                    if (i_values.has_key(name)):
                        params.append(i_values[name])
                    elif (self._engine == 'ORACLE' and o_types.has_key(name)):
                        params.append(cur.var(data_types[self._engine][o_types[name].lower()])) 
                    else:
                        params.append(None)                               
                
                if (type in ('func', 'function')):
                    result = cur.callfunc(p_name, data_types[self._engine][ret_type.lower()], params) 
                else:
                    cur.callproc(p_name, params)
                
                    if (self._engine == 'MYSQL'):
                        query = 'SELECT '                    
                        for i in xrange(0, len(params)):
                            query += '@_{0}_{1},'.format(p_name, i)   
                        cur.execute(query[:-1])
                        params = cur.fetchone()
                                   
                output = {}
                i = 0 
                for param in params:
                    name = param_names[i]
                
                    if (self._engine == 'ORACLE'):                                        
                        if (param.__class__.__module__ == 'cx_Oracle'):
                            param = param.getvalue()
                        if (o_types.has_key(name) and o_types[name] == 'int' and param != None):
                            param = int(param)
                        
                    output[name] = param
                    i = i+1              
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_dbi_proc_called'), self._mh.fromhere())
            if (type in ('func', 'function')): 
                ev = event.Event('dbi_after_call_proc', result, output) 
                self._mh.fire_event(ev)               
                return result, output
            else:
                ev = event.Event('dbi_after_call_proc', output) 
                self._mh.fire_event(ev)                 
                return output
        
        except (cx_Oracle.Error, MySQLdb.Error), ex:
            self._mh.dmsg('htk_on_error', 'database error: {0}'.format(ex), self._mh.fromhere())
            return None                                     