# -*- coding: utf-8 -*-
"""This code is part of Hydra Toolkit library

.. module:: network.jms.client
   :platform: Unix
   :synopsis: Generic JMS client
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
jms_before_connect
jms_after_connect
jms_before_send
jms_after_send
jms_before_receive
jms_after_receive

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from hydratk.lib.bridge.java import JavaBridge

class JMSClient:
    
    _mh = None
    _bridge = None
    _client = None
    _verbose = None
    _connection_factory = None
    _properties = None
    
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
            self._client = self._bridge.get_class('JMSClient', self._verbose) 
        
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
    def connection_factory(self):
        
        return self._connection_factory
    
    @property
    def properties(self):
        
        return self._properties                
        
    def connect(self, connection_factory, properties={}):
        """Method connectes to server
        
        Args:
           connection_factory: JMS connection factory
           properties (dict): JMS connection properties 

        Returns:
           bool: result
                
        """        
        
        try:
        
            msg = 'connection_factory:{0}, properties:{1}'.format(connection_factory, properties)       
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_connecting', msg), self._mh.fromhere()) 
        
            ev = event.Event('jms_before_connect', connection_factory, properties)
            if (self._mh.fire_event(ev) > 0):
                connection_factory = ev.argv[0]
                properties = ev.argv[1]                 
        
            self._connection_factory = connection_factory
            self._properties = properties
        
            if (ev.will_run_default()):             
                hashmap = self._bridge.init_hashmap(properties)
                result = self._client.connect(self._connection_factory, hashmap)
        
            if (result):
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_connected'), self._mh.fromhere()) 
                ev = event.Event('jms_after_connect')
                self._mh.fire_event(ev)         
            else:
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_jms_connecting_error'), self._mh.fromhere())        
        
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
        
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_disconnecting'), self._mh.fromhere())
                
            result = self._client.disconnect()
            if (result):
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_disconnected'), self._mh.fromhere())    
            else:
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_jms_disconnecting_error'), self._mh.fromhere())   
            
            return result
        
        except RuntimeError, ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return False           
        
    def send(self, destination_name, message, destination_type='queue', headers={}):
        """Method sends message
        
        Args:
           destination_name (str): queue|topic name
           message (str): message
           destination_type (str): queue|topic
           headers {dict}: JMS headers

        Returns:
           bool: result
                
        """   
        
        try:        
        
            msg = 'destination_name:{0}, message:{1}, destination_type:{2}, headers:{3}'.format(destination_name, message,
                  destination_type, headers)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_sending_msg', msg), self._mh.fromhere())         
        
            ev = event.Event('jms_before_send', destination_name, message, destination_type, headers)
            if (self._mh.fire_event(ev) > 0):        
                destination_name = ev.args[0]
                message = ev.args[1]
                destination_type = ev.args[2]
                headers = ev.args[3]
        
            if (ev.will_run_default()): 
                hashmap = self._bridge.init_hashmap(headers)
                result = self._client.send(destination_type, destination_name, hashmap, message)
        
            if (result):  
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_msg_sent'), self._mh.fromhere())  
                ev = event.Event('jms_after_send')
                self._mh.fire_event(ev)    
            else:
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_jms_sending_error'), self._mh.fromhere())                  
       
            return result 
    
        except RuntimeError, ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return False           
    
    def receive(self, destination_name, destination_type='queue', cnt=1, jms_correlation_id=None,
                jms_type=None):
        """Method receives messages
        
        Args:
           destination_name (str): queue|topic name
           destination_type (str): queue|topic
           cnt (int): count of messages
           jms_correlation_id (str): messages with given JMSCorrelationID
           jms_type (str): messages with given JMSType

        Returns:
           list: messages
                
        """           
        
        try:
        
            msg = 'destination_name:{0}, destination_type:{1}, count:{2}, jms_correlation_id:{3}, jms_type:{4}'.format(
                  destination_name, destination_type, cnt, jms_correlation_id, jms_type)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_receiving_msg', msg), self._mh.fromhere())         
        
            ev = event.Event('jms_before_receive', destination_name, destination_type)
            if (self._mh.fire_event(ev) > 0):        
                destination_name = ev.args[0]
                destination_type = ev.args[1]
                cnt = ev.args[2]
                jms_correlation_id = ev.args[3]
                jms_type = ev.args[4]
        
            if (ev.will_run_default()): 
                messages = self._client.receive(destination_type, destination_name, cnt, jms_correlation_id, jms_type)
        
            if (messages != None):
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_msg_received', len(messages)), self._mh.fromhere())  
                ev = event.Event('jms_after_receive')
                self._mh.fire_event(ev) 
            else:                   
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_jms_receiving_error'), self._mh.fromhere())
       
            return messages  
    
        except RuntimeError, ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return None           