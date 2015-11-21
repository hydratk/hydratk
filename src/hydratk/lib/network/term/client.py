# -*- coding: utf-8 -*-
"""This code is part of Hydra Toolkit library

.. module:: network.lib.term
   :platform: Unix
   :synopsis: Generic TERMINAL client for protocols: SSH
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
term_before_connect
term_after_connect
term_before_exec_command
term_after_exec_command

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
import paramiko
import logging

default_ports = {
  'SSH'   : 22
}

class TermClient:
    
    _mh = None
    _client = None
    _protocol = None
    _host = None    
    _port = None
    _user = None
    _passw = None
    _verbose = None
    
    def __init__(self, protocol='SSH', verbose=False):
        """Class constructor
           
        Called when the object is initialized 
        
        Args:
           protocol (str):  terminal protocol, SSH          
           verbose (bool): verbose mode
           
        """          
        
        self._mh = MasterHead.get_head()
        self._protocol = protocol.upper()        
        if (self._protocol == 'SSH'):            
            self._client = paramiko.SSHClient()   
        elif (self._protocol != 'SSH'):
            self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_term_unknown_protocol', self._protocol), self._mh.fromhere())
            return None
                         
        self._verbose = verbose 
        if (self._verbose):
            if (self._protocol == 'SSH'):                
                logging.basicConfig(level=logging.DEBUG)
                
    def connect(self, host, port=None, user=None, passw=None):
        """Method connects to server
        
        Args:
           host (str): server host
           port (int): server port, default protocol port
           user (str): username
           passw (str): password
           
        Returns:
           bool: result
           
        Raises:
           event: term_before_connect
           event: term_after_connect          
                
        """                  
        
        try:
            
            self._port = port if (port != None) else default_ports[self._protocol]
            message = '{0}/{1}@{2}:{3}'.format(user, passw, host, self._port)                            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_term_connecting', message), self._mh.fromhere())
            
            ev = event.Event('term_before_connect', host, self._port, user, passw)
            if (self._mh.fire_event(ev) > 0):
                host = ev.argv(0)
                self._port = ev.argv(1)
                user = ev.argv(2)
                passw = ev.argv(3)                    
            
            self._host = host
            self._user = user
            self._passw = passw
            
            if (ev.will_run_default()):                  
                if (self._protocol == 'SSH'):
                    self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    self._client.connect(self._host, self._port, self._user, self._passw)                
                
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_term_connected'), self._mh.fromhere()) 
            ev = event.Event('term_after_connect')
            self._mh.fire_event(ev)   
                                                   
            return True
        
        except paramiko.SSHException, ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            
            if (self._protocol == 'SSH'):
                self._client.close()
            
            return False            
                   
    def disconnect(self):
        """Method disconnects from server
           
        Returns:
           bool: result
                
        """           
         
        try:                                                 
                
            self._client.close()
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_term_disconnected'), self._mh.fromhere())  
            return True  
    
        except paramiko.SSHException, ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False                    
    
    def exec_command(self, command, input=None):
        """Method executes command
           
        Args:
           command (str): command
           input (str): input for interactive mode         
           
        Returns:
           tuple: result (bool), output (list) (stdout for result True, stderr for result False) 
           
        Raises:
           event: term_before_exec_command
           event: term_after_exec_command   
                
        """         
        
        try:
        
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_term_executing_command', command), self._mh.fromhere())              
            
            ev = event.Event('term_before_exec_command', command)
            if (self._mh.fire_event(ev) > 0):
                command = ev.argv(0)            
            
            if (ev.will_run_default()): 
                stdin, stdout, stderr = self._client.exec_command(command)
                
                if (input != None):
                    stdin.write(input + '\n')
                    stdin.flush()
                
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_term_command_executed'), self._mh.fromhere())
                ev = event.Event('term_after_exec_command')
                self._mh.fire_event(ev)               
            
                err = stderr.read().splitlines()            
                if (len(err) > 0 and input == None):
                    raise paramiko.SSHException(err)
                else:
                    out = stdout.read().splitlines()
                    out = out if (len(out) > 0) else None
                    return True, out
            
        except paramiko.SSHException, ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False, err                                