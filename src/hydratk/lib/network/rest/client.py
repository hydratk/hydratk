# -*- coding: utf-8 -*-
"""This code is part of Hydra Toolkit library

.. module:: network.rest.client
   :platform: Unix
   :synopsis: Generic REST client for protocols HTTP, HTTPS
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
rest_before_request
rest_after_request

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
import httplib2
import urllib
import jsonlib2
import lxml

default_ports = {
  'HTTP' : 80,
  'HTTPS': 443               
}

mime_types = {
  'form': 'application/x-www-form-urlencoded',
  'html': 'text/html',  
  'json': 'application/json',  
  'text': 'text/plain',
  'xml' : 'application/xml'
}

class RESTClient:
    
    _mh = None
    _client = None
    _res_header = None
    _res_body = None
    _verbose = None
    
    def __init__(self, verbose=False, cache=False, ignore_cert=True):
        """Class constructor
           
        Called when the object is initialized 
        
        Args:                   
           verbose (bool): verbose mode
           cache (bool): use local cache
           ignore_cert (bool): ignore untrusted certificate errors
           
        """         
        
        self._mh = MasterHead.get_head() 
        
        if (cache):
            self._client = httplib2.Http('.cache', disable_ssl_certificate_validation=ignore_cert)
        else:
            self._client = httplib2.Http(disable_ssl_certificate_validation=ignore_cert)     
        
        self._verbose = verbose
        if (self._verbose):
            httplib2.debuglevel = 2
        
    def send_request(self, host, protocol='HTTP', port=None, path='/', user=None, passw=None, 
                     method='GET', headers=None, body=None, params=None, content_type=None):
        """Method sends request to server
        
        Args:
           host (str): server host
           protocol (str): protocol
           port (int): server port
           path (str): server path
           user (str): username
           passw (str): password           
           method (str): HTTP method
           headers (dict): HTTP headers
           body (str): request body, POST method used by default
           params (dict): parameters, sent in URL for GET method, in body for POST|PUT|DELETE method
           content_type (str): type of content, form|html|json|text|xml

        Returns:
           tuple: status (int), body (str) (json object, xml object, otherwise original string)
       
        Raises:
           event: rest_before_request
           event: rest_after_request
                
        """          
        
        try:
            
            protocol = self.protocol.lower() if (protocol == None) else protocol
            port = default_ports[protocol.upper()] if (port == None) else port
            message = '{0}://{1}:{2}{3}'.format(protocol, host, port, path)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_rest_request', message, user, passw,
                          method, headers, body, params), self._mh.fromhere()) 
            
            ev = event.Event('rest_before_request', host, protocol, port, path, user, passw, method,
                             headers, body, params, content_type)
            if (self._mh.fire_event(ev) > 0):
                host = ev.argv(0)
                protocol = ev.argv(1)
                port = ev.argv(2)
                path = ev.argv(3)
                user = ev.argv(4)
                passw = ev.argv(5)
                method = ev.argv(6)
                headers = ev.argv(7)
                body = ev.argv(8)
                params = ev.argv(9)
                content_type = ev.argv(10)             
            
            if (ev.will_run_default()): 
                url = '{0}://{1}:{2}{3}'.format(protocol, host, port, path) 
            
                if (user != None):
                    self._client.add_credentials(user, passw)            
            
                if (params != None):                
                    if (method in ('GET', None)):
                        url = '{0}?{1}'.format(url, urllib.urlencode(params))  
                    elif (method in ('POST', 'PUT', 'DELETE')):
                        body = urllib.urlencode(params)  
                        content_type = 'form'        
                if (body != None and method in ('GET', None)):
                    method = 'POST'                    
                if (content_type != None and mime_types.has_key(content_type)):
                    if (headers == None):
                        headers = {}
                    headers['Content-Type'] = mime_types[content_type]
            
                self._res_header, self._res_body = self._client.request(url, method, body, headers)
            
            content_type = self.get_header('Content-Type')
            if ('json' in content_type):
                self._res_body = jsonlib2.read(self._res_body)
            elif ('xml' in content_type):               
                self._res_body = lxml.objectify.fromstring(self._res_body)
             
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_rest_response', self._res_header), self._mh.fromhere()) 
            ev = event.Event('rest_after_request')
            self._mh.fire_event(ev)               
                
            return self._res_header.status, self._res_body
            
        except httplib2.HttpLib2Error, ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return None   
        
    def get_header(self, title):
        """Method gets response header
        
        Args:
           title (str): header title

        Returns:
           str: header
                
        """  
        
        title = title.lower()
        if (self._res_header.has_key(title)):        
            return self._res_header[title]
        else:
            return None 
    
    def get_body(self): 
        """Method gets response body
        
        Args:

        Returns:
           str: body
                
        """               
        
        return self._res_body                                                                                              
