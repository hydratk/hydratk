# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit

.. module:: hydratk.lib.network.rest.client
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
    res_header = None
    res_body = None
    verbose = None
    
    def __init__(self, verbose=False, cache=False, ignore_cert=True):
        
        self._mh = MasterHead.get_head() 
        
        if (cache):
            self._client = httplib2.Http('.cache', disable_ssl_certificate_validation=ignore_cert)
        else:
            self._client = httplib2.Http(disable_ssl_certificate_validation=ignore_cert)     
        
        self.verbose = verbose
        if (self.verbose):
            httplib2.debuglevel = 2
        
    def send_request(self, host, protocol='HTTP', port=None, path='/', user=None, passw=None, 
                     method='GET', headers=None, body=None, params=None, content_type=None):
        """Method sends request to server
        
        Args:
           host - server host, string, mandatory
           protocol - protocol, string, optional, default HTTP
           port - server port, int, optional
           path - server path, string, optional, default /
           user - username, string, optional
           passw - password, string, optional           
           method - HTTP method, string, optional, default GET
           headers - HTTP header, dictionary title:value, optional
           body - request body, string, optional, POST method used by default
           params - parameters, dictionary title:value, optional 
                  - sent in URL for GET method, in body for POST|PUT|DELETE method
           content_type - type of content, string, form|html|json|text|xml, optional

        Returns:
           status - int
           body - json object for content-type application/json
                - xml object for content-type application/xml
                - otherwise original string         
                
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
            
                self.res_header, self.res_body = self._client.request(url, method, body, headers)
            
            content_type = self.get_header('Content-Type')
            if ('json' in content_type):
                self.res_body = jsonlib2.read(self.res_body)
            elif ('xml' in content_type):               
                self.res_body = lxml.objectify.fromstring(self.res_body)
             
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_rest_response', self.res_header), self._mh.fromhere()) 
            ev = event.Event('rest_after_request')
            self._mh.fire_event(ev)               
                
            return self.res_header.status, self.res_body
            
        except httplib2.HttpLib2Error, ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return None   
        
    def get_header(self, title):
        """Method gets response header
        
        Args:
           title - header title, string, mandatory

        Returns:
           header - string
                
        """  
        
        title = title.lower()
        if (self.res_header.has_key(title)):        
            return self.res_header[title]
        else:
            return None 
    
    def get_body(self): 
        """Method gets response body
        
        Args:

        Returns:
           body - string
                
        """               
        
        return self.res_body                                                                                              