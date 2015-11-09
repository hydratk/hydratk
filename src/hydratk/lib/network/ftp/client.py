# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit

.. module:: hydratk.lib.network.ftp.client
   :platform: Unix
   :synopsis: Generic FTP client for protocols: FTP, FTPS, SFTP, TFTP
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
ftp_before_connect
ftp_after_connect
ftp_before_change_dir
ftp_before_download_file
ftp_after_download_file
ftp_before_upload_file
ftp_after_upload_file
ftp_before_delete_file
ftp_before_make_dir
ftp_before_remove_dir

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
import ftplib
import paramiko
import tftpy
import os
import logging

default_ports = {
                  'FTP' : 21,
                  'FTPS': 21,
                  'SFTP': 22,
                  'TFTP': 69
                }

class FTPClient:
    
    _mh = None
    _client = None
    _output = None
    protocol = None
    url = None
    port = None
    path = '/'
    verbose = None
    
    def __init__(self, protocol='FTP', verbose=False):
        
        self._mh = MasterHead.get_head()
        self.protocol = protocol.upper()        
        if (self.protocol == 'FTP'):            
            self._client = ftplib.FTP()
        elif (self.protocol == 'FTPS'):
            self._client = ftplib.FTP_TLS()              
        elif (self.protocol not in ('SFTP', 'TFTP')):
            self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_ftp_unknown_protocol', self.protocol), self._mh.fromhere())
            return None
                         
        self.verbose = verbose 
        if (self.verbose):
            if (self.protocol in ('FTP', 'FTPS')):  
                self._client.set_debuglevel(2) 
            elif (self.protocol == 'SFTP'):                
                logging.getLogger('paramiko').setLevel(logging.DEBUG)
            elif (self.protocol == 'TFTP'):
                tftpy.TftpShared.setLogLevel(2)            
        
    def connect(self, host, port=None, user=None, passw=None, path='/'):
        """Method connects to server
        
        Args:
           host - server host, string, mandatory
           port - server port, int, optional, default protocol port
           user - username, string, optional
           passw - password, string, optional
           path - server path, string, optional, default /
           
        Returns:
           result - bool         
                
        """          
        
        try:            
            
            self.port = port if (port != None) else default_ports[self.protocol]                
            message = '{0}/{1}@{2}:{3}{4}'.format(user, passw, host, port, path)                            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_connecting', message), self._mh.fromhere())
            
            ev = event.Event('ftp_before_connect', host, port, user, passw, path)
            if (self._mh.fire_event(ev) > 0):
                host = ev.argv(0)
                self.port = ev.argv(1)
                user = ev.argv(2)
                passw = ev.argv(3)
                path = ev.argv(4)                        
            
            if (ev.will_run_default()):    
                if (self.protocol in ('FTP', 'FTPS')):
                    self._client.connect(host, self.port)
                elif (self.protocol == 'SFTP'):                
                    t = paramiko.Transport((host, self.port))                                 
                elif (self.protocol == 'TFTP'):
                    self._client = tftpy.TftpClient(host, self.port)                  
            
                if (user != None):
                    if (self.protocol in ('FTP', 'FTPS')):
                        self._client.login(user, passw)
                    elif (self.protocol == 'SFTP'):
                        t.connect(username=user, password=passw)
                        self._client = paramiko.SFTPClient.from_transport(t)         
                    
                if (self.protocol == 'FTPS'):
                    self._client.prot_p()               
                
                self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_connected'), self._mh.fromhere())        
                if (path != None and self.protocol in ('FTP', 'FTPS', 'SFTP')):
                    self.change_dir(path)
                                            
            ev = event.Event('ftp_after_connect')
            self._mh.fire_event(ev)   
                                    
            return True
        
        except ftplib.all_errors, ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False
        
    def disconnect(self):
        """Method disconnects from server
           Supported only for FTP, FTPS, SFTP
           
        Returns:
           result - bool         
                
        """           
         
        try:
                                             
            if (self.protocol in ('FTP', 'FTPS')):                                 
                self._client.quit()
            elif (self.protocol == 'SFTP'):
                self._client.close()
            else:
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_ftp_unknown_method', self.protocol), self._mh.fromhere())
                return False
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_disconnected'), self._mh.fromhere())  
            return True
            
        except ftplib.all_errors, ex: 
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())       
            return False 
        
    def list_dir(self):
        """Method list remote working directory
           Supported only for FTP, FTPS, SFTP
           
        Returns:
           names - list of string         
                
        """           
        
        try: 
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_list_dir', self.path), self._mh.fromhere())
        
            if (self.protocol in ('FTP', 'FTPS')):
                names = self._client.nlst()
                if ('.' in names): names.remove('.')
                if ('..' in names): names.remove('..')            
            elif (self.protocol == 'SFTP'):
                names = self._client.listdir()
            else:
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('htp_ftp_unknown_method', self.protocol), self._mh.fromhere())
                return None            
                    
            return names  
    
        except ftplib.all_errors, ex: 
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())       
            return None       
        
    def change_dir(self, path):
        """Method changes remote working directory
           Supported only for FTP, FTPS, SFTP
        
        Args:
           path - new remote path, string, mandatory
           
        Returns:
           result - bool         
                
        """           
        
        try:
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_change_dir', path), self._mh.fromhere())
            
            ev = event.Event('ftp_before_change_dir', path)
            if (self._mh.fire_event(ev) > 0):
                path = ev.argv(0)             
            
            if (ev.will_run_default()):
                if (self.protocol in ('FTP', 'FTPS')):
                    self._client.cwd(path)
                    cur_dir = self._client.pwd()
                elif (self.protocol == 'SFTP'):
                    self._client.chdir(path)
                    cur_dir = self._client.getcwd()
                else:
                    self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_ftp_unknown_method', self.protocol), self._mh.fromhere())
                    return False                
            
            self.path = cur_dir
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_cur_dir', self.path), self._mh.fromhere())  
            return True
         
        except ftplib.all_errors, ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())        
            return False  
        
    def download_file(self, remote_path, local_path=None):
        """Method downloads file from server
        
        Args:
           remote_path - remote path, string, mandatory
           local_path - local path, string, optional, default ./filename
           
        Returns:
           result - bool         
                
        """           
        
        try:
            
            self._mh.dmsg('htk_on_debug_info',self._mh._trn.msg('htk_ftp_downloading_file', remote_path), self._mh.fromhere())
            
            ev = event.Event('ftp_before_download_file', remote_path, local_path)
            if (self._mh.fire_event(ev) > 0):
                remote_path = ev.argv(0)  
                local_path = ev.argv(1)                        
            
            if (local_path != None and not os.path.exists(local_path)):
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_ftp_unknown_dir', local_path), self._mh.fromhere())  
                return False            
            
            filename = remote_path.split('/')[-1]
            path = filename if (local_path == None) else os.path.join(local_path, filename)
              
            if (ev.will_run_default()):
                if (self.protocol in ('FTP', 'FTPS')):                       
                    with open(path, 'wb') as f:                   
                        self._client.retrbinary('RETR ' + remote_path, f.write) 
                elif (self.protocol == 'SFTP'):                
                    self._client.get(remote_path, path)
                elif (self.protocol == 'TFTP'):
                    self._client.download(filename, path)
             
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_file_downloaded'), self._mh.fromhere()) 
            ev = event.Event('ftp_after_download_file')
            self._mh.fire_event(ev)   
              
            return True
 
        except (ftplib.all_errors, tftpy.TftpShared.TftpException), ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            if (os.path.exists(path)):
                os.remove(path)                     
            return False  
        
    def upload_file(self, local_path, remote_path=None):
        """Method uploads file to server
        
        Args:
           local_path - local path, string, mandatory
           remote_path - remote path, string, optional, default ./filename
           
        Returns:
           result - bool         
                
        """           
        
        try:
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_uploading_file', local_path), self._mh.fromhere())
            
            ev = event.Event('ftp_before_upload_file', local_path, remote_path)
            if (self._mh.fire_event(ev) > 0):
                local_path = ev.argv(0)
                remote_path = ev.argv(1)  
            
            if (not(os.path.exists(local_path) or os.path.exists(os.path.relpath(local_path)))):
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_ftp_unknown_file', local_path), self._mh.fromhere())  
                return False
            
            filename = local_path.split('/')[-1]
            path = filename if (remote_path == None) else os.path.join(remote_path, filename)            
            
            if (ev.will_run_default()):
                if (self.protocol in ('FTP', 'FTPS')):
                    with open(local_path, 'r') as f:                   
                        self._client.storbinary('STOR ' + path, f)   
                elif (self.protocol == 'SFTP'):
                    self._client.put(local_path, path)              
                elif (self.protocol == 'TFTP'):
                    self._client.upload(path, local_path)
 
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_file_uploaded'), self._mh.fromhere()) 
            ev = event.Event('ftp_after_upload_file')   
            self._mh.fire_event(ev) 
            
            return True
 
        except (ftplib.all_errors, tftpy.TftpShared.TftpException), ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())                    
            return False  
        
    def delete_file(self, path):  
        """Method deletes file from server
        
        Args:
           path - remote path, string, mandatory
           
        Returns:
           result - bool         
                
        """             
        
        try:

            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_deleting_file', path), self._mh.fromhere())
            
            ev = event.Event('ftp_before_delete_file', path)
            if (self._mh.fire_event(ev) > 0):
                path = ev.argv(0)            
            
            if (ev.will_run_default()):
                if (self.protocol in ('FTP', 'FTPS')):
                    self._client.delete(path) 
                elif (self.protocol == 'SFTP'):
                    self._client.remove(path)
                else:
                    self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_ftp_unknown_method', self.protocol), self._mh.fromhere())
                    return False                
             
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_file_deleted'), self._mh.fromhere())        
            return True              
            
        except ftplib.all_errors, ex:     
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex[1]), self._mh.fromhere())                             
            return False   
        
    def make_dir(self, path): 
        """Method makes directory on server
        
        Args:
           path - remote path, string, mandatory
           
        Returns:
           result - bool         
                
        """              
        
        try:
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_making_dir', path), self._mh.fromhere())
            
            ev = event.Event('ftp_before_make_dir', path)
            if (self._mh.fire_event(ev) > 0):
                path = ev.argv(0)            
            
            if (ev.will_run_default()):
                if (self.protocol in ('FTP', 'FTPS')):
                    self._client.mkd(path)
                elif (self.protocol == 'SFTP'):
                    self._client.mkdir(path)
                else:
                    self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_ftp_unknown_method', self.protocol), self._mh.fromhere())
                    return False                
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_dir_made'), self._mh.fromhere())    
            return True
                      
        except ftplib.all_errors, ex:     
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex[1]), self._mh.fromhere())                             
            return False              
        
    def remove_dir(self, path): 
        """Method removes directory from server
        
        Args:
           path - remote path, string, mandatory
           
        Returns:
           result - bool         
                
        """                 
        
        try:
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_removing_dir', path), self._mh.fromhere())  
            
            ev = event.Event('ftp_before_remove_file', path)
            if (self._mh.fire_event(ev) > 0):
                path = ev.argv(0)                     
            
            if (ev.will_run_default()):
                if (self.protocol in ('FTP', 'FTPS')):
                    self._client.rmd(path)
                elif (self.protocol == 'SFTP'):
                    self._client.rmdir(path)
                else:
                    self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_ftp_unknown_method', self.protocol), self._mh.fromhere())
                    return False                
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_ftp_dir_removed'), self._mh.fromhere())     
            return True
                      
        except ftplib.all_errors, ex:     
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex[1]), self._mh.fromhere())                             
            return False                                    