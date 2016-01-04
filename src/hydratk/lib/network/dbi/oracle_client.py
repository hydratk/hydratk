# -*- coding: utf-8 -*-
"""This code is part of Hydra Toolkit library

.. module:: network.dbi.oracle_client
   :platform: Unix
   :synopsis: ORACLE DB client
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
from cx_Oracle import Error, connect, NUMBER, STRING, TIMESTAMP, CLOB, BLOB
from string import replace

class DBClient():
    
    _mh = None
    _client = None
    _host = None
    _port = None
    _sid = None
    _user = None
    _passw = None
    
    _data_types = {
       'int'      : NUMBER,
       'float'    : NUMBER,
       'string'   : STRING,
       'timestamp': TIMESTAMP,
       'clob'     : CLOB,
       'blob'     : BLOB
    }
    
    def __init__(self):
        """Class constructor
           
        Called when the object is initialized          
           
        """    
        
        self._mh = MasterHead.get_head() 
        
    @property
    def client(self):
        
        return self._client
    
    @property
    def host(self):
        
        return self._host
    
    @property
    def port(self):
        
        return self._port
    
    @property
    def sid(self):
        
        return self._sid
    
    @property
    def user(self):
        
        return self._user
    
    @property
    def passw(self):
        
        return self._passw                    
        
    def connect(self, host=None, port=1521, sid=None, user=None, passw=None, db_file=None):
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
            
            ev = event.Event('dbi_before_connect', host, port, sid, user, passw)
            if (self._mh.fire_event(ev) > 0):
                host = ev.argv(0)
                port = ev.argv(1)
                sid = ev.argv(2)
                user = ev.argv(3)
                passw = ev.argv(4)            
            
            if (ev.will_run_default()):
                self._host = host 
                self._port = port               
                self._sid = sid
                self._user = user
                self._passw = passw
                
                dsn_str = '{0}:{1}/{2}'.format(self._host, self._port, self._sid)
                self._client = connect(user=self._user, password=self._passw, dsn=dsn_str)                      

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
                    for i in xrange(0, len(bindings)):
                        query = replace(query, '?', ':{0}'.format(i+1), 1)

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
        
    def call_proc(self, p_name, param_names=[], i_values={}, o_types={}, type='proc', ret_type=None):
        """Method calls procedure/function from database
        
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
                if (type not in ('func', 'function', 'proc', 'procedure')):
                    self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_dbi_unknown_type', self.type), self._mh.fromhere())
                    return None
                
                cur = self._client.cursor()
            
                params = []
                for name in param_names:
                    if (i_values.has_key(name)):
                        params.append(i_values[name])
                    elif (o_types.has_key(name)):
                        params.append(cur.var(self._data_types[o_types[name].lower()])) 
                    else:
                        params.append(None)                               
                
                if (type in ('func', 'function')):
                    result = cur.callfunc(p_name, self._data_types[ret_type.lower()], params) 
                else:
                    cur.callproc(p_name, params)
                                   
                output = {}
                i = 0 
                for param in params:
                    name = param_names[i]
                                                    
                    if (param.__class__.__module__ == 'cx_Oracle'):
                        param = param.getvalue()
                    if (o_types.has_key(name) and o_types[name] == 'int' and param != None):
                        param = int(param)
                        
                    output[name] = param
                    i = i+1              
            
            cur.close()  
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_dbi_proc_called'), self._mh.fromhere())
            
            if (type in ('func', 'function')): 
                ev = event.Event('dbi_after_call_proc', result, output) 
                self._mh.fire_event(ev)               
                return result, output
            else:
                ev = event.Event('dbi_after_call_proc', output) 
                self._mh.fire_event(ev)                 
                return output
        
        except Error, ex:
            self._mh.dmsg('htk_on_error', 'database error: {0}'.format(ex), self._mh.fromhere())
            return None          