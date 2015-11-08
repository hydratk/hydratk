# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit

.. module:: hydratk.lib.network.jms.client
   :platform: Unix
   :synopsis: Generic JMS client
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core.masterhead import MasterHead
import subprocess
import os

cfg = {   
    'url'                    : 't3://sxcipppr1.ux.to2cz.cz:8301,sxcipppr2.ux.to2cz.cz:8301', 
    'jar_path'               : '/var/local/hydratk/yoda/yoda-lib/o2apps/lib/jmsclient.jar',
    'java_command'           : 'java8',
    'connection_factory'     : 'javax/jms/QueueConnectionFactory',
    'initial_context_factory': 'weblogic.jndi.WLInitialContextFactory'
  }

class JMSClient:
    
    _mh = None
    _wrapper = None
    _separator = None
    java = None
    connection_factory = None
    initial_context_factory = None
    provider_url = None
    security_principal = None
    security_credentials = None
    
    def __init__(self, env='pre'):
        
        self._mh = MasterHead.get_head()
        self.java = cfg['java_command']
        jar = cfg['jar']
        if (os.path.exists(jar) == False):
            self._mh.dmsg('htk_on_error', 'missing jar file {0}'.format(jar), self._mh.fromhere())                                    
            return None  
                    
        self._wrapper = subprocess.Popen([self.java, '-jar', jar], stdin=subprocess.PIPE, 
                                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)  
        self._separator = '&&&'
            
        self.connection_factory = cfg['connection_factory']
        self.initial_context_factory = cfg['initial_context_factory']
        self.provider_url = cfg['url']                 
        self.security_principal = None
        self.security_credentials = None
        
    def connect(self):
        
        command = 'connect{0}connectionFactory{1}{2}'.format(self._separator, self._separator, self.connection_factory) + \
                  '{0}initialContextFactory{1}{2}'.format(self._separator, self._separator, self.initial_context_factory) + \
                  '{0}providerURL{1}{2}'.format(self._separator, self._separator, self.provider_url)
                  
        if (self.security_principal != None):
            command += '{0}securityPrincipal{1}{2}'.format(self._separator, self._separator, self.security_principal) + \
                       '{0}securityCredentials{1}{2}'.format(self._separator, self._separator, self.security_credentials)
        
        command += '\n'                
        self._wrapper.stdin.write(command)
        
    def disconnect(self):
        
        command = 'disconnect\n'
        self._wrapper.stdin.write(command)
        
    def send(self, destination, jms_type, message, jms_correlation_id):
        
        message = message.replace('\n', '')
        command = 'send{0}destination{1}{2}'.format(self._separator, self._separator, destination) + \
                  '{0}JMSCorrelationID{1}{2}'.format(self._separator, self._separator, jms_correlation_id) + \
                  '{0}JMSType{1}{2}'.format(self._separator, self._separator, jms_type) + \
                  '{0}message{1}{2}\n'.format(self._separator, self._separator, message)   
        self._wrapper.stdin.write(command)