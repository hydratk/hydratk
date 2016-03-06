# -*- coding: utf-8 -*-
"""This code is part of Hydra Toolkit library

.. module:: hydratk.lib.network.ftp.ftp_client
   :platform: Unix
   :synopsis: FTP client unit tests library
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core.masterhead import MasterHead
from hydratk.lib.network.ftp.client import FTPClient
from ftplib import FTP, FTP_TLS, Error

class TestFTPClient():

    def __init__(self, secured=False, verbose=False):
        
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
        
        self._client = FTPClient('FTP', secured, verbose)
        
    def handle_event(self, ev):
        
        self._events.append(ev._id)
        
    def connect(self, host, port=21, user=None, passw=None, path='/', ex=False):           
        
        def mock_connect(self, host, port):
            
            pass
        
        def mock_login(self, user, passw):
            
            pass
            
        def mock_prot_p(self):
            
            if (ex):
                raise Error('Connect error')
            
        def mock_cwd(self, path):
            
            pass
        
        def mock_pwd(self):                        
                        
            return path          
        
        if (not self._client._secured):
            o_methods = [FTP.connect, FTP.login, FTP.cwd, FTP.pwd]
            try:
                FTP.connect = mock_connect
                FTP.login = mock_login
                FTP.cwd = mock_cwd
                FTP.pwd = mock_pwd
                return self._client.connect(host, port, user, passw, path)
            finally:
                FTP.connect = o_methods[0]
                FTP.login = o_methods[1] 
                FTP.cwd = o_methods[2]
                FTP.pwd = o_methods[3]
        else:
            o_methods = [FTP_TLS.connect, FTP_TLS.login, FTP_TLS.prot_p, FTP_TLS.cwd, FTP_TLS.pwd]
            try:
                FTP_TLS.connect = mock_connect
                FTP_TLS.login = mock_login
                FTP_TLS.prot_p = mock_prot_p
                FTP_TLS.cwd = mock_cwd
                FTP_TLS.pwd = mock_pwd
                return self._client.connect(host, port, user, passw)
            finally:
                FTP_TLS.connect = o_methods[0]
                FTP_TLS.login = o_methods[1]
                FTP_TLS.prot_p = o_methods[2]    
                FTP_TLS.cwd = o_methods[3]
                FTP_TLS.pwd = o_methods[4]
                
    def disconnect(self, ex=False):           

        def mock_quit(self):
            
            if (ex):
                raise Error('Disconnect error')
        
        if (not self._client._secured):
            o_method = FTP.quit
            try:
                FTP.quit = mock_quit
                return self._client.disconnect()
            finally:
                FTP.quit = o_method
        else:
            o_method = FTP_TLS.quit
            try:
                FTP_TLS.quit = mock_quit
                return self._client.disconnect()
            finally:
                FTP_TLS.quit = o_method   
                
    def list_dir(self, ex=False):
        
        def mock_nlst(self):
            
            if (ex):
                raise Error('List dir error')
            
            names = ['.', '..', 'dir1', 'dir2', 'file1', 'file2']
            return names
            
        if (not self._client._secured):
            o_method = FTP.nlst
            try:
                FTP.nlst = mock_nlst
                return self._client.list_dir()
            finally:
                FTP.nlst = o_method
        else:
            o_method = FTP_TLS.nlst
            try:
                FTP_TLS.nlst = mock_nlst
                return self._client.list_dir()
            finally:
                FTP_TLS.nlst = o_method    
                
    def change_dir(self, path, ex=False):
        
        def mock_cwd(self, path):
            
            pass
        
        def mock_pwd(self):
            
            if (ex):
                raise Error('Change dir error')
            
            return '/home/hydratk'
        
        if (not self._client._secured):
            o_methods = [FTP.cwd, FTP.pwd]
            try:
                FTP.cwd = mock_cwd
                FTP.pwd = mock_pwd
                return self._client.change_dir(path)
            finally:
                FTP.cwd = o_methods[0]
                FTP.pwd = o_methods[1]
        else:
            o_methods = [FTP_TLS.cwd, FTP_TLS.pwd]
            try:
                FTP_TLS.cwd = mock_cwd
                FTP_TLS.pwd = mock_pwd
                return self._client.change_dir(path)
            finally:
                FTP_TLS.cwd = o_methods[0]
                FTP_TLS.pwd = o_methods[1]
                
    def download_file(self, remote_path, local_path=None, ex=False):
        
        def mock_retrbinary(self, cmd, write):
            
            if (ex):
                raise Error('Download file error')  
            
            write('File downloaded')
            
        if (not self._client._secured):
            o_method = FTP.retrbinary
            try:
                FTP.retrbinary = mock_retrbinary
                return self._client.download_file(remote_path, local_path)
            finally:
                FTP.retrbinary = o_method
        else:
            o_method = FTP_TLS.retrbinary
            try:
                FTP_TLS.retrbinary = mock_retrbinary
                return self._client.download_file(remote_path, local_path)
            finally:
                FTP_TLS.retrbinary = o_method 
                
    def upload_file(self, local_path, remote_path=None, ex=False):
        
        def mock_storbinary(self, cmd, f):
            
            if (ex):
                raise Error('Upload file error')
            
        if (not self._client._secured):
            o_method = FTP.storbinary
            try:
                FTP.storbinary = mock_storbinary
                return self._client.upload_file(local_path, remote_path)
            finally:
                FTP.storbinary = o_method
        else:
            o_method = FTP_TLS.storbinary
            try:
                FTP_TLS.storbinary = mock_storbinary
                return self._client.upload_file(local_path, remote_path)
            finally:
                FTP_TLS.storbinary = o_method    
                
    def delete_file(self, path, ex=False):
        
        def mock_delete(self, path):
            
            if (ex):
                raise Error('Delete file error')  
            
        if (not self._client._secured):
            o_method = FTP.delete
            try:
                FTP.delete = mock_delete
                return self._client.delete_file(path)
            finally:
                FTP.delete = o_method
        else:
            o_method = FTP_TLS.delete
            try:
                FTP_TLS.delete = mock_delete
                return self._client.delete_file(path)
            finally:
                FTP_TLS.delete = o_method                      
                
    def make_dir(self, path, ex=False):
        
        def mock_mkd(self, path):
            
            if (ex):
                raise Error('Make dir error')  
            
        if (not self._client._secured):
            o_method = FTP.mkd
            try:
                FTP.mkd = mock_mkd
                return self._client.make_dir(path)
            finally:
                FTP.mkd = o_method
        else:
            o_method = FTP_TLS.mkd
            try:
                FTP_TLS.mkd = mock_mkd
                return self._client.make_dir(path)
            finally:
                FTP_TLS.mkd = o_method  
                
    def remove_dir(self, path, ex=False):
        
        def mock_rmd(self, path):
            
            if (ex):
                raise Error('Remove dir error')  
            
        if (not self._client._secured):
            o_method = FTP.rmd
            try:
                FTP.rmd = mock_rmd
                return self._client.remove_dir(path)
            finally:
                FTP.rmd = o_method
        else:
            o_method = FTP_TLS.rmd
            try:
                FTP_TLS.rmd = mock_rmd
                return self._client.remove_dir(path)
            finally:
                FTP_TLS.rmd = o_method                                                          