# -*- coding: utf-8 -*-
"""This code is part of Hydra Toolkit library

.. module:: hydratk.lib.network.term.ssh_client
   :platform: Unix
   :synopsis: SSH client unit tests library
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core.masterhead import MasterHead
from hydratk.lib.network.term.client import TermClient
from paramiko import SSHClient
from paramiko.ssh_exception import SSHException

class TestTermClient():

    def __init__(self, verbose=False):
        
        hook = [
                {'event' : 'term_before_connect', 'callback' : self.handle_event },
                {'event' : 'term_after_connect', 'callback' : self.handle_event },
                {'event' : 'term_before_exec_command', 'callback' : self.handle_event },
                {'event' : 'term_after_exec_command', 'callback' : self.handle_event }                 
               ]
        self._mh = MasterHead.get_head()
        self._mh.register_event_hook(hook)
        self._events = []
        
        self._client = TermClient('SSH', verbose)
        
    def handle_event(self, ev):
        
        self._events.append(ev._id)

    def connect(self, host, port=22, user=None, passw=None, ex=False):   
        
        def mock_connect(self, host, port, user, passw):
            
            if (ex):
                raise SSHException('Connect error')
        
        o_method = SSHClient.connect
        try:
            SSHClient.connect = mock_connect
            return self._client.connect(host, port, user, passw)
        finally:
            SSHClient.connect = o_method    
            
    def disconnect(self, ex=False):   
        
        def mock_close(self):
            
            if (ex):
                raise SSHException('Disconnect error')
        
        o_method = SSHClient.close
        try:
            SSHClient.close = mock_close
            return self._client.disconnect()
        finally:
            SSHClient.close = o_method   
            
    def exec_command(self, command, input=None, ex=False):
        
        def mock_exec_command(self, command):
            
            if (ex):
                raise SSHException('Exec command error')
                  
            [stdin, stdout, stderr] = [mock_std(), mock_std(), mock_std()]
            if ('touch' in command):
                stdout.write('')
            elif ('which' in command):
                stdout.write('/usr/local/bin/htk')
            elif ('ls' in command):
                stdout.write('.\n..\n/home\n/root')
            elif ('su' in command):
                stderr.write('Permission denied')
            elif ('rm -i' in command):
                stdin.write(input)
                stderr.write('Are you sure ?')
            
            return stdin, stdout, stderr
        
        class mock_std():
            
            def __init__(self):
                self.data = ''
            
            def read(self):                
                return self.data
            
            def flush(self):                
                pass
            
            def write(self, data):                
                self.data += data
        
        o_method = SSHClient.exec_command
        try:
            SSHClient.exec_command = mock_exec_command
            return self._client.exec_command(command, input)
        finally:
            SSHClient.exec_command = o_method        