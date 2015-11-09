# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit

.. module:: hydratk.lib.network.dbi.client
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
    engine = None;
    host = None;
    port = None;
    sid = None;
    user = None;
    passw = None;
    db_file = None;
    
    def __init__(self, engine='SQLITE'):
        
        self._mh = MasterHead.get_head()
        self.engine = engine.upper() 
        
        if (self.engine not in ('SQLITE', 'ORACLE', 'MYSQL', 'POSTGRESQL')):
            self._mh.dmsg('htk_on_error', self._mh.trn.msg('htk_dbi_unknown_engine', self.engine), self._mh.fromhere())
            return None        
        
    def connect(self, host=None, port=None, sid=None, user=None, passw=None, db_file=None):
        """Method connects to database
        
        Args:            
           host - hostname, string, optional, used for Oracle, MySQL, PostgreSQL only
           port - port, int, optional, used for Oracle, MySQL, PostgreSQL only
           sid - db instance, string, optional, used for Oracle, MySQL, PostgreSQL only
           user - username, string, optional, used for Oracle, MySQL, PostgreSQL only
           passw - password, string, optional, used for Oracle, MySQL, PostgreSQL only 
           db_file - path to database file, string, optional, used for SQLite only  
        Returns:
           result - bool
                
        """        
        
        try:
                    
            if (self.engine != 'SQLITE'):
                self.port = port if (port != None) else default_ports[self.engine]
                message = '{0}/{1}@{2}:{3}/{4}'.format(user, passw, host, self.port, sid)
            else:
                message = '{0}'.format(db_file)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_dbi_connecting', message), self._mh.fromhere())
            
            ev = event.Event('dbi_before_connect', host, self.port, sid, user, passw, db_file)
            if (self._mh.fire_event(ev) > 0):
                host = ev.argv(0)
                self.port = ev.argv(1)
                sid = ev.argv(2)
                user = ev.argv(3)
                passw = ev.argv(4)
                db_file = ev.argv(5)               
            
            if (ev.will_run_default()):
                if (self.engine == 'SQLITE'):
                    self.db_file = db_file
                    self._client = sqlite3.connect(self.db_file)
                    self._client.execute('PRAGMA foreign_keys = ON')
                else:
                    self.host = host                
                    self.sid = sid
                    self.user = user
                    self.passw = passw
                
                    if (self.engine == 'ORACLE'):
                        dsn_str = cx_Oracle.makedsn(self.host, self.port, self.sid)
                        self._client = cx_Oracle.connect(dsn=dsn_str, user=self.user, password=self.passw)
                    elif (self.engine == 'MYSQL'):
                        self._client = MySQLdb.connect(host=self.host, port=self.port, db=self.sid, user=self.user, 
                                                       passwd=self.passw)
                    elif (self.engine == 'POSTGRESQL'):
                        self._client = psycopg2.connect(host=self.host, port=self.port, database=self.sid,
                                                        user=self.user, password=self.passw)

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
          result - bool 
                
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
          query - query, string, mandatory, binded variables are marked with ?
          bindings - query bindings, list, optional 
          fetch_one - fetch one row only, bool, optional, default False
             
        Returns:
          result - bool
          rows - record rows accessible by column 
                
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
                if (self.engine == 'SQLITE'):
                    self._client.row_factory = sqlite3.Row
            
                cur = self._client.cursor()    
                
                if (bindings != None):
                    if (self.engine == 'ORACLE'):
                        for i in xrange(0, len(bindings)):
                            query = string.replace(query, '?', ':{0}'.format(i+1), 1)
                    elif (self.engine in ('MYSQL', 'POSTGRESQL')):
                        query = string.replace(query, '?', '%s')

                    cur.execute(query, tuple(bindings))
                else:
                    cur.execute(query)
                
                if (self.engine in ('ORACLE', 'MYSQL', 'POSTGRESQL')):
                    if (cur.description == None):
                        return True, None
                    columns = [i[0].lower() for i in cur.description]
                    rows = [dict(zip(columns, row)) for row in cur]           
                
                if (fetch_one):
                    if (self.engine == 'SQLITE'):
                        rows = cur.fetchone()
                    else:
                        rows = rows[0]
                else:
                    if (self.engine == 'SQLITE'):
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
          p_name - procedure name, string, mandatory
          param_names - parameter names (input, output), list of string, optional
          i_values - input parameter values, dictionary name:value, optional
          o_types - output parameter types, dictionary name:type, optional  
          type - code type, func|function|proc|procedure, optional, default proc
          ret_type - return type, string, optional, used for function only                    
             
        Returns:
          result - bool, used for function only 
          params - parameters, dictionary name:value
                
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
                if (self.engine in ('SQLITE', 'POSTGRESQL')):
                    self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_dbi_unknown_method', self.engine), self._mh.fromhere())
                    return None
                elif (type not in ('func', 'function', 'proc', 'procedure')):
                    self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_dbi_unknown_type', self.type), self._mh.fromhere())
                    return None
                
                cur = self._client.cursor()
            
                params = []
                for name in param_names:
                    if (i_values.has_key(name)):
                        params.append(i_values[name])
                    elif (self.engine == 'ORACLE' and o_types.has_key(name)):
                        params.append(cur.var(data_types[self.engine][o_types[name].lower()])) 
                    else:
                        params.append(None)                               
                
                if (type in ('func', 'function')):
                    result = cur.callfunc(p_name, data_types[self.engine][ret_type.lower()], params) 
                else:
                    cur.callproc(p_name, params)
                
                    if (self.engine == 'MYSQL'):
                        query = 'SELECT '                    
                        for i in xrange(0, len(params)):
                            query += '@_{0}_{1},'.format(p_name, i)   
                        cur.execute(query[:-1])
                        params = cur.fetchone()
                                   
                output = {}
                i = 0 
                for param in params:
                    name = param_names[i]
                
                    if (self.engine == 'ORACLE'):                                        
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