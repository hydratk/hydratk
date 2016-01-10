# -*- coding: utf-8 -*-
"""This code is part of Hydra Toolkit library

.. module:: network.dbi.jdbc_client
   :platform: Unix
   :synopsis: Generic JDBC client
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
from hydratk.lib.bridge.java import JavaBridge

class DBClient:
    
    _mh = None
    _bridge = None
    _client = None
    _verbose = None
    _driver = None
    _conn_str = None
    _user = None
    _passw = None
    
    def __init__(self, verbose=False, jvm_path=None, classpath=None, options=[]):
        """Class constructor
           
        Called when the object is initialized
        Uses Java client program to access JMS provider 
        
        Args:                   
           verbose (bool): verbose mode
           jvm_path (str): JVM location, default from configuration
           classpath (str): Java classpath, default from configuration
           options (list): JVM options
           
        """         
        
        try:
        
            self._mh = MasterHead.get_head()
            self._verbose = verbose    
          
            self._bridge = JavaBridge(jvm_path, classpath)
            self._bridge.start(options)  
            self._client = self._bridge.get_class('DBClient', self._verbose) 
        
        except RuntimeError, ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())       
        
    def close(self):
        """Method stops JVM  
                
        """  
        
        self._bridge.stop()          
         
    @property
    def bridge(self):
        
        return self._bridge

    @property
    def client(self):
        
        return self._client
    
    @property
    def verbose(self):   
        
        return self._verbose   
    
    @property
    def driver(self):   
        
        return self.driver 
    
    @property
    def conn_str(self):   
        
        return self._conn_str 
    
    @property
    def user(self):   
        
        return self._user
    
    @property
    def passw(self):   
        
        return self._passw                             
        
    def connect(self, driver, conn_str, user, passw):
        """Method connectes to server
        
        Args:
           connection_factory: JMS connection factory
           properties (dict): JMS connection properties 

        Returns:
           bool: result
           
        Raises:
           event: dbi_before_connect
           event: dbi_after_connect           
                
        """        
        
        try:
        
            message = '{0}/{1}@{2}, driver:{3}'.format(user, passw, conn_str, driver)       
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_dbi_connecting', message), self._mh.fromhere())            
                              
            ev = event.Event('dbi_before_connect', driver, conn_str, user, passw)
            if (self._mh.fire_event(ev) > 0):
                driver = ev.args(0)
                conn_str = ev.argv(1)
                user = ev.argv(2)
                passw = ev.argv(3)                    
             
            if (ev.will_run_default()):      
                self._driver = driver
                self._conn_str = conn_str
                self._user = user
                self._passw = passw      
                  
                result = bool(self._client.connect(self._driver, self._conn_str, self._user, self._passw))
        
            if (result):                
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_dbi_connected'), self._mh.fromhere())
                ev = event.Event('dbi_after_connect')
                self._mh.fire_event(ev)  
            else:
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_dbi_connecting_error'), self._mh.fromhere())                      
        
            return result
    
        except RuntimeError, ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return False 
        
    def disconnect(self):
        """Method disconnects from server           

        Returns:
           bool: result
                
        """           
        
        try:
        
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_dbi_disconnecting'), self._mh.fromhere())
                
            result = bool(self._client.disconnect())
            if (result):
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_dbi_disconnected'), self._mh.fromhere())   
            else:
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_dbi_disconnecting_error'), self._mh.fromhere())   
            
            return result
        
        except RuntimeError, ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return False     
        
    def exec_query(self, query, bindings=[], fetch_one=False):
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
                arraylist = self.bridge.init_arraylist(bindings)
                rows = self._client.exec_query(query, arraylist, fetch_one)
             
                if (rows != None):                                                        
                    
                    if (len(rows) > 0):
                        columns = [i.lower() for i in rows[0]]  
                        if (len(rows) > 1):     
                            del rows[0]        
                            rows = [dict(zip(columns, row)) for row in rows] 
                        else:
                            rows = columns  
                    else:
                        rows = None             
                
                    result = True
                    self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_dbi_query_executed'), self._mh.fromhere())
                    ev = event.Event('dbi_after_exec_query', True, rows)
                    self._mh.fire_event(ev)                 
                
                else:
                    result = False
                    self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_dbi_query_error'), self._mh.fromhere())                              
                                                              
            return result, rows
        
        except RuntimeError, ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return False                