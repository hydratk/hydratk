# -*- coding: utf-8 -*-
"""This code is part of Hydra Toolkit library

.. module:: network.jms.simplejms
   :platform: Unix
   :synopsis: Simple JMS client for request based processing
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

from hydratk.lib.network.jms import client
from hydratk.lib.system import fs

class JMSClient(client.JMSClient, object):
    _request   = None    
    _response  = None

    
    @property
    def request(self):
        return self._request
    
    @request.setter
    def request(self, req):
        self._request = req
    
    @property
    def response(self):
        return self._response
    
    def send(self, jms_correlation_id):
        return client.JMSClient.send(
                               self, 
                               self._request.destination_queue, 
                               self._request.jms_type, 
                               self._request.message.content, 
                               jms_correlation_id
                             )
               
class JMSRequest(object):
    _msg                   = None
    _destination_queue     = None
    _jms_type              = None        
    
    def __init__(self, destination_queue, jms_type):        
        self._destination_queue = destination_queue
        self._jms_type          = jms_type      
    
    
    @property
    def destination_queue(self):
        return self._destination_queue
    
    @destination_queue.setter
    def destination_queue(self, queue):
        self._destination_queue = queue
    
    @property
    def jms_type(self):
        return self._jms_type
    
    @jms_type.setter
    def jms_type(self, type):
        self._jms_type = type
    
    @property
    def msg(self):
        return self._msg
    
    @msg.setter
    def msg(self, msg):
        self._msg = msg   
                     
    @property
    def message(self):
        return self._msg
    
    @message.setter
    def message(self, msg):
        self._msg = msg
        
class JMSRequestMessage(object):
    _bind_lchr = '['
    _bind_rchr = ']'
    _content   = None
    
    def __init__(self, content=None, source='file'):
        if content is not None:
            if source == 'file':
                self.load_from_file(content)
            if source == 'str':
                self._content = content  
                
    @property
    def content(self):        
        return self._content
    
    @content.setter
    def content(self, content):
        self._content = content
    
    def load_from_file(self,msg_file):
        self._content = fs.file_get_contents(msg_file)             
        
    def bind_var(self,*args,**kwargs):
        if self._content is not None:
            content = str(self._content)
            for bdata in args:
                for var,value in bdata.items():
                    bind_var = '{bind_lchr}{var}{bind_rchr}'.format(bind_lchr=self._bind_lchr,var=var,bind_rchr=self._bind_rchr)                
                    content = content.replace(str(bind_var), str(value))
            for var, value in kwargs.items():
                bind_var = '{bind_lchr}{var}{bind_rchr}'.format(bind_lchr=self._bind_lchr,var=var,bind_rchr=self._bind_rchr)                
                content = content.replace(str(bind_var), str(value))                
            self._content = content    
            
class JMSResponse(object):
    pass  