# -*- coding: utf-8 -*-
"""This code is part of Hydra Toolkit library

.. module:: hydratk.lib.network.ftp.sftp_client
   :platform: Unix
   :synopsis: SFTP client unit tests library
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core.masterhead import MasterHead
from hydratk.lib.network.ftp.client import FTPClient
from tftpy import TftpShared, TftpClient

class TestFTPClient():

    def __init__(self, verbose=False):
        
        hook = [
                {'event' : 'ftp_before_connect', 'callback' : self.handle_event },
                {'event' : 'ftp_after_connect', 'callback' : self.handle_event },
                {'event' : 'ftp_before_download_file', 'callback' : self.handle_event },   
                {'event' : 'ftp_after_download_file', 'callback' : self.handle_event },    
                {'event' : 'ftp_before_upload_file', 'callback' : self.handle_event }, 
                {'event' : 'ftp_after_upload_file', 'callback' : self.handle_event }         
               ]
        self._mh = MasterHead.get_head()
        self._mh.register_event_hook(hook)
        self._events = []
        
        self._client = FTPClient('TFTP', verbose)
        
    def handle_event(self, ev):
        
        self._events.append(ev._id)
        
    def mock_init(self, host):
        
        pass
        
    def connect(self, host, port=69, ex=False):           
        
        def mock_init(self, host, port):
            
            if (ex):
                raise TftpShared.TftpException('Connect error')
        
        o_method = TftpClient.__init__
        try:
            TftpClient.__init__ = mock_init
            return self._client.connect(host, port)
        finally:
            TftpClient.__init__ = o_method
                
    def download_file(self, remote_path, local_path=None, ex=False):
         
        def mock_download(self, remote_path, lpath):
            
            if (ex):
                raise TftpShared.TftpException('Download file error')
            
        o_methods = [TftpClient.__init__, TftpClient.download]
        try:
            TftpClient.__init__ = self.mock_init
            TftpClient.download = mock_download
            self._client._client = TftpClient(None)
            return self._client.download_file(remote_path, local_path)
        finally:
            TftpClient.__init__ = o_methods[0]
            TftpClient.download = o_methods[1]
                
    def upload_file(self, local_path, remote_path=None, ex=False):
        
        def mock_upload(self, local_path, rpath):
            
            if (ex):
                raise TftpShared.TftpException('Upload file error')
            
        o_methods = [TftpClient.__init__, TftpClient.upload]
        try:
            TftpClient.__init__ = self.mock_init
            TftpClient.upload = mock_upload
            self._client._client = TftpClient(None)
            return self._client.upload_file(local_path, remote_path)
        finally:
            TftpClient.__init__ = o_methods[0]
            TftpClient.upload = o_methods[1]                                                   