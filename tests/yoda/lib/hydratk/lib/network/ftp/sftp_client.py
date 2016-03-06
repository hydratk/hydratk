# -*- coding: utf-8 -*-
"""This code is part of Hydra Toolkit library

.. module:: hydratk.lib.network.ftp.sftp_client
   :platform: Unix
   :synopsis: SFTP client unit tests library
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core.masterhead import MasterHead
from hydratk.lib.network.ftp.client import FTPClient
from paramiko import SFTPClient, Transport
from paramiko.ssh_exception import SSHException

class TestFTPClient():

    def __init__(self, verbose=False):
        
        hook = [
                {'event' : 'ftp_before_connect', 'callback' : self.handle_event },
                {'event' : 'ftp_after_connect', 'callback' : self.handle_event },
                {'event' : 'ftp_before_change_dir', 'callback' : self.handle_event },
                {'event' : 'ftp_before_download_file', 'callback' : self.handle_event },   
                {'event' : 'ftp_after_download_file', 'callback' : self.handle_event },    
                {'event' : 'ftp_before_upload_file', 'callback' : self.handle_event }, 
                {'event' : 'ftp_after_upload_file', 'callback' : self.handle_event },
                {'event' : 'ftp_before_delete_file', 'callback' : self.handle_event },  
                {'event' : 'ftp_before_make_dir', 'callback' : self.handle_event }, 
                {'event' : 'ftp_before_remove_dir', 'callback' : self.handle_event }           
               ]
        self._mh = MasterHead.get_head()
        self._mh.register_event_hook(hook)
        self._events = []
        
        self._client = FTPClient('SFTP', verbose)
        
    def handle_event(self, ev):
        
        self._events.append(ev._id)
        
    def mock_init(self, host):
        
        pass
        
    def connect(self, host, port=22, user=None, passw=None, path='/', ex=False):           
        
        def mock_init(self, host):
            
            if (ex):
                raise SSHException('Connect error')                
        
        def mock_connect(self, username, password):
            
            pass        
            
        def mock_chdir(self, path):
            
            pass
        
        def mock_getcwd(self):                      
            
            return path
        
        o_methods = [Transport.__init__, Transport.connect, SFTPClient.__init__, 
                     SFTPClient.chdir, SFTPClient.getcwd]
        try:
            Transport.__init__ = mock_init
            Transport.connect = mock_connect
            SFTPClient.__init__ = self.mock_init
            SFTPClient.chdir = mock_chdir
            SFTPClient.getcwd = mock_getcwd
            self._client._client = SFTPClient(None)
            return self._client.connect(host, port, user, passw, path)
        finally:
            Transport.__init__ = o_methods[0]
            Transport.connect = o_methods[1]
            SFTPClient.__init__ = o_methods[2]
            SFTPClient.chdir = o_methods[3]
            SFTPClient.getcwd = o_methods[4]
                
    def disconnect(self, ex=False):           

        def mock_close(self):
            
            if (ex):
                raise SSHException('Disconnect error')

        o_methods = [SFTPClient.__init__, SFTPClient.close]
        try:
            SFTPClient.__init__ = self.mock_init
            SFTPClient.close = mock_close
            self._client._client = SFTPClient(None)
            return self._client.disconnect()
        finally:
            SFTPClient.__init__ = o_methods[0]
            SFTPClient.close = o_methods[1]
                
    def list_dir(self, ex=False):
        
        def mock_listdir(self):
            
            if (ex):
                raise SSHException('List dir error')
            
            names = ['dir1', 'dir2', 'file1', 'file2']
            return names        
            
        o_methods = [SFTPClient.__init__, SFTPClient.listdir]
        try:
            SFTPClient.__init__ = self.mock_init
            SFTPClient.listdir = mock_listdir
            self._client._client = SFTPClient(None)
            return self._client.list_dir()
        finally:
            SFTPClient.__init__ = o_methods[0]
            SFTPClient.listdir = o_methods[0]
                
    def change_dir(self, path, ex=False):
        
        def mock_chdir(self, path):
            
            pass
        
        def mock_getcwd(self):
            
            if (ex):
                raise SSHException('Change dir error')  
            
            return '/home/hydratk'      
        
        o_methods = [SFTPClient.__init__, SFTPClient.chdir, SFTPClient.getcwd]
        try:
            SFTPClient.__init__ = self.mock_init
            SFTPClient.chdir = mock_chdir
            SFTPClient.getcwd = mock_getcwd
            self._client._client = SFTPClient(None)
            return self._client.change_dir(path)
        finally:
            SFTPClient.__init__ = o_methods[0]
            SFTPClient.chdir = o_methods[1]
            SFTPClient.getcwd = o_methods[2]
                
    def download_file(self, remote_path, local_path=None, ex=False):
         
        def mock_get(self, remote_path, lpath):
            
            if (ex):
                raise SSHException('Download file error')
            
        o_methods = [SFTPClient.__init__, SFTPClient.get]
        try:
            SFTPClient.__init__ = self.mock_init
            SFTPClient.get = mock_get
            self._client._client = SFTPClient(None)
            return self._client.download_file(remote_path, local_path)
        finally:
            SFTPClient.__init__ = o_methods[0]
            SFTPClient.get = o_methods[1]
                
    def upload_file(self, local_path, remote_path=None, ex=False):
        
        def mock_put(self, local_path, rpath):
            
            if (ex):
                raise SSHException('Upload file error')
            
        o_methods = [SFTPClient.__init__, SFTPClient.put]
        try:
            SFTPClient.__init__ = self.mock_init
            SFTPClient.put = mock_put
            self._client._client = SFTPClient(None)
            return self._client.upload_file(local_path, remote_path)
        finally:
            SFTPClient.__init__ = o_methods[0]
            SFTPClient.put = o_methods[1] 
                
    def delete_file(self, path, ex=False):
        
        def mock_remove(self, path):
            
            if (ex):
                raise SSHException('Delete file error')        
            
        o_methods = [SFTPClient.__init__, SFTPClient.remove]
        try:
            SFTPClient.__init__ = self.mock_init
            SFTPClient.remove = mock_remove
            self._client._client = SFTPClient(None)
            return self._client.delete_file(path)
        finally:
            SFTPClient.__init__ = o_methods[0]
            SFTPClient.remove = o_methods[1]                    
                
    def make_dir(self, path, ex=False):
                     
        def mock_mkdir(self, path):
            
            if (ex):
                raise SSHException('Make dir error')        
            
        o_methods = [SFTPClient.__init__, SFTPClient.mkdir]
        try:
            SFTPClient.__init__ = self.mock_init
            SFTPClient.mkdir = mock_mkdir
            self._client._client = SFTPClient(None)
            return self._client.make_dir(path)
        finally:
            SFTPClient.__init__ = o_methods[0]
            SFTPClient.mkdir = o_methods[1]  
                
    def remove_dir(self, path, ex=False):
                    
        def mock_rmdir(self, path):
            
            if (ex):
                raise SSHException('Remove dir error')        
            
        o_methods = [SFTPClient.__init__, SFTPClient.rmdir]
        try:
            SFTPClient.__init__ = self.mock_init
            SFTPClient.rmdir = mock_rmdir
            self._client._client = SFTPClient(None)
            return self._client.remove_dir(path)
        finally:
            SFTPClient.__init__ = o_methods[0]
            SFTPClient.rmdir = o_methods[1]                                                       