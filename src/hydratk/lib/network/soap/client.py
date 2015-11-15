# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit

.. module:: hydratk.lib.network.soap.client
   :platform: Unix
   :synopsis: Generic SOAP client
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
soap_before_load_wsdl
soap_after_load_wsdl
soap_before_request
soap_after_request

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
import suds
import lxml
import logging
import sys

class SOAPClient:
    
    _mh = None
    _client = None
    wsdl = None
    url = None
    location = None
    user = None
    passw = None
    endpoint = None
    headers = None
    verbose = None
    
    def __init__(self, verbose=False):
        
        self._mh = MasterHead.get_head()          
        
        self.verbose = verbose
        if (self.verbose):
            handler = logging.StreamHandler(sys.stderr)
            logger = logging.getLogger('suds.transport.http')
            logger.setLevel(logging.DEBUG), handler.setLevel(logging.DEBUG)
            logger.addHandler(handler)
            
    def load_wsdl(self, url, location='remote', user=None, passw=None, endpoint=None, headers=None): 
        """Method loads wsdl
        
        Args:
           url - WSDL URL, string, mandatory, URL for remote, file path for local
           location - WSDL location, string remote|local, optional, default remote
           user - username, string, optional
           passw - password, string, optional
           endpoint - service endpoint, string, optional, default endpoint from WSDL 
           headers - HTTP headers, dictionary of name:value, optional

        Returns:
           result - bool        
                
        """          
        
        try:
                        
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_soap_loading_wsdl', url,
                          user, passw, endpoint, headers), self._mh.fromhere())
            
            ev = event.Event('soap_before_load_wsdl', url, location, user, passw, endpoint, headers)
            if (self._mh.fire_event(ev) > 0):
                url = ev.argv(0)
                location = ev.argv(1)
                user = ev.argv(2)
                passw = ev.argv(3)
                endpoint = ev.argv(4)
                headers = ev.argv(5)         
        
            self.url = url
            self.location = location
            self.user = user
            self.passw = passw
            self.endpoint = endpoint  
            self.headers = headers
        
            if (ev.will_run_default()): 
                
                options = {}
                if (self.location == 'local'):
                    self.url = 'file://' + self.url
                if (self.user != None):
                    options['username'] = self.user
                    options['password'] = self.password
                if (self.endpoint != None):
                    options['location'] = self.endpoint
                if (self.headers != None):
                    options['headers'] = self.headers
        
                self._client = suds.client.Client(self.url, **options)  
                self.wsdl = self._client.wsdl
                
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_soap_wsdl_loaded'), self._mh.fromhere())
            ev = event.Event('soap_after_load_wsdl')
            self._mh.fire_event(ev)                   
                
            return True
            
        except suds.WebFault, ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False 
        
    def get_operations(self):
        """Method returns service operations
        
        Args:           

        Returns:
           operations - list of string
                
        """           
                               
        if (self.wsdl != None):
            operations = []
            for operation in self.wsdl.services[0].ports[0].methods.values():       
                operations.append(operation.name)  
            return operations
        
    def send_request(self, operation, body, headers=None):      
        """Method sends request
        
        Args:   
           operation - operation name, string, mandatory
           body - request body, string or xml, mandatory
           headers - HTTP headers, dictionary name:value, optional 
                   - headers SOAPAction, Content-Type are set automatically       

        Returns:
           response - response body, xml object
                
        """    
        
        try:
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_soap_request', operation, body, headers),
                          self._mh.fromhere()) 
            
            ev = event.Event('soap_before_request', operation, body, headers)
            if (self._mh.fire_event(ev) > 0):
                operation = ev.argv(0)
                body = ev.argv(1)
                headers = ev.argv(2)    
                
            if (ev.will_run_default()):                             
            
                if (headers != None):
                    self._client.set_options(headers=headers)
            
                nsmap = {'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/'}
                ns = '{%s}' % nsmap['soapenv']
                root = lxml.etree.Element(ns+'Envelope', nsmap=nsmap)
                lxml.etree.SubElement(root, ns+'Header')
                elem = lxml.etree.SubElement(root, ns+'Body')
            
                if (isinstance(body, str)):
                    body = lxml.etree.fromstring(body) 
                elem.append(body)           
            
                response = getattr(self._client.service, operation)(__inject = {'msg': lxml.etree.tostring(root)})                
        
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_soap_response', response), self._mh.fromhere()) 
            ev = event.Event('soap_after_request')
            self._mh.fire_event(ev)        
        
            response = lxml.etree.fromstring(str(response)) 
            return response
            
        except (suds.WebFault, Exception), ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return None                     