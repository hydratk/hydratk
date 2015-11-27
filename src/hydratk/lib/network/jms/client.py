# -*- coding: utf-8 -*-
"""This code is part of Hydra Toolkit library

.. module:: network.jms.client
   :platform: Unix
   :synopsis: Generic JMS client with support of WebLogic
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
jms_before_connect
jms_after_connect
jms_before_send
jms_after_send

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
import subprocess

class JMSClient:
    
    _mh = None
    _verbose = None
    _java = None
    _classpath = None
    _wrapper = None
    _separator = '&&&'
    _connection_factory = None
    _initial_context_factory = None
    _provider_url = None
    _security_principal = None
    _security_credentials = None
    
    def __init__(self, verbose=False):
        """Class constructor
           
        Called when the object is initialized
        Uses wrapped Java client program to access JMS provider 
        
        Args:                   
           verbose (bool): verbose mode
           
        """         
        
        self._mh = MasterHead.get_head()
        self._verbose = verbose
        
        self._java = self._mh.cfg['Libraries']['hydratk.lib.network.jms']['java']      
        self._classpath = self._mh.cfg['Libraries']['hydratk.lib.network.jms']['classpath'] 
        command = [self._java, '-cp', self._classpath, 'JMSClient']    
        self._wrapper = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)          
        
    def _read_stdout(self):
        """Method reads stdout from Java program

        Returns:
           list: output
                
        """          
        
        output = [self._wrapper.stdout.readline()]
        output.append(self._wrapper.stdout.readline())

        if (self._verbose):
            for line in output:
                self._mh.dmsg('htk_on_debug_info', line.rstrip(), self._mh.fromhere())
        
        return output
    
    def _get_result(self, output):
        """Method gets command result from stdout

        OK - True, command executed successfully
        ERR - False, command execution failed
        INFO - ignored, it is used for debugging purposes

        Returns:
           bool: result
                
        """             
        
        result = False
        for line in output:
            if ('OK - ' in line):
                result = True
            elif ('ERR - ' in line):
                result = False
        
        return result
        
    def connect(self, connection_factory, initial_context_factory, provider_url,
                security_principal=None, security_credentials=None):
        """Method sends command connect  
        
        Args:
           connection_factory (str): connection factory, JMS specific
           initial_context_factory (str): initial context factory, provider specific
           provider_url (str): URL
           security_principal (str): user
           security_credentials (str): password     

        Returns:
           bool: result
                
        """  
          
        self._connection_factory = connection_factory
        self._initial_context_factory = initial_context_factory
        self._provider_url = provider_url              
        self._security_principal = security_principal
        self._security_credentials = security_credentials       
        
        msg = 'connection_factory:{0}, initial_context_factory:{1}, provider_url:{2}, security_principal:{3}, security_credentials:{4}'.format(
               self._connection_factory, self._initial_context_factory, self._provider_url, self._security_principal, self._security_credentials)       
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_connecting', msg), self._mh.fromhere()) 
        
        ev = event.Event('jms_before_connect', self._connection_factory, self._initial_context_factory, self._provider_url,
                         self._security_principal, self._security_credentials)
        if (self._mh.fire_event(ev) > 0):
            self._connection_factory = ev.argv[0]  
            self._initial_context_factory = ev.argv[1] 
            self._provider_url = ev.argv[2] 
            self._security_principal = ev.argv[3] 
            self._security_credentials = ev.argv[4]                
        
        if (ev.will_run_default()): 
            command = 'connect{0}connectionFactory{1}{2}'.format(self._separator, self._separator, self._connection_factory) + \
                      '{0}initialContextFactory{1}{2}'.format(self._separator, self._separator, self._initial_context_factory) + \
                      '{0}providerURL{1}{2}'.format(self._separator, self._separator, self._provider_url)
                  
            if (self._security_principal != None):
                command += '{0}securityPrincipal{1}{2}'.format(self._separator, self._separator, self._security_principal) + \
                           '{0}securityCredentials{1}{2}'.format(self._separator, self._separator, self._security_credentials)
            
            command += '\n'             
            self._wrapper.stdin.write(command)
            
            result = self._get_result(self._read_stdout())
        
        if (result):
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_connected'), self._mh.fromhere()) 
            ev = event.Event('jms_after_connect')
            self._mh.fire_event(ev)         
        else:
            print 'ERROR'         
        
        return result
        
    def disconnect(self):
        """Method sends command disconnect            

        Returns:
           bool: result
                
        """           
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_disconnecting'), self._mh.fromhere())
        command = 'disconnect\n'
        self._wrapper.stdin.write(command)  
                
        result = self._get_result(self._read_stdout())
        if (result):
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_disconnected'), self._mh.fromhere())     
        else:
            print 'ERROR'   
        return result  
        
    def send(self, destination, jms_type, message, jms_correlation_id):
        """Method sends command send
        
        Args:
           destination (str): queue
           jms_type (str): message type
           message (str): message
           jms_correlation_id (str): correlation id

        Returns:
           bool: result
                
        """           
        
        msg = 'destination:{0}, jms_type:{1}, message:{2}, jms_correlation_id:{3}'.format(destination, jms_type,
              message, jms_correlation_id)
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_sending_msg', msg), self._mh.fromhere())         
        
        ev = event.Event('jms_before_send', destination, jms_type, message, jms_correlation_id)
        if (self._mh.fire_event(ev) > 0):        
            destination = ev.args[0]
            jms_type = ev.args[1]
            message = ev.args[2]
            jms_correlation_id = ev.args[3]
        
        if (ev.will_run_default()): 
            message = message.replace('\n', '')
            command = 'send{0}destination{1}{2}'.format(self._separator, self._separator, destination) + \
                      '{0}JMSCorrelationID{1}{2}'.format(self._separator, self._separator, jms_correlation_id) + \
                      '{0}JMSType{1}{2}'.format(self._separator, self._separator, jms_type) + \
                      '{0}message{1}{2}\n'.format(self._separator, self._separator, message)   
            self._wrapper.stdin.write(command)
            
            result = self._get_result(self._read_stdout())
        
        if (result):  
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_jms_msg_sent'), self._mh.fromhere())  
            ev = event.Event('jms_after_send')
            self._mh.fire_event(ev)    
        else:
            print 'ERROR'                  
       
        return result