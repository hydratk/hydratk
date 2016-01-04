# -*- coding: utf-8 -*-
"""This code is part of Hydra Toolkit library

.. module:: network.email.imap_client
   :platform: Unix
   :synopsis: IMAP email client
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
email_before_connect
email_after_connect
email_before_receive_email
email_after_receive_email

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from imaplib import IMAP4, IMAP4_SSL
from string import replace

class EmailClient:
    
    _mh = None
    _client = None
    _host = None    
    _port = None
    _user = None
    _passw = None
    _verbose = None
    
    def __init__(self, secured=False, verbose=False):
        """Class constructor
           
        Called when the object is initialized 
        
        Args:
           secured (bool): secured POP  
           verbose (bool): verbose mode     
           
        """         
        
        self._mh = MasterHead.get_head()
        self._secured = secured 
        self._verbose = verbose   
            
    @property
    def client(self):
        
        return self._client
    
    @property
    def host(self):
        
        return self._host
    
    @property
    def port(self):
        
        return self._port
    
    @property
    def user(self):
        
        return self._user
    
    @property
    def passw(self):
        
        return self._passw
    
    @property
    def verbose(self):
        
        return self._verbose                    
                
    def connect(self, host, port=None, user=None, passw=None):
        """Method connects to server
        
        Args:
           host (str): server host
           port (str): server port, default protocol port
           user (str): username
           passw (str): password

        Returns:
           bool: result         
             
        Raises:
           event: email_before_connect
           event: email_after_connect     
                
        """                  
        
        try:
            
            if (port == None):
                port = 143 if (not self._secured) else 993
                
            message = '{0}/{1}@{2}:{3}'.format(user, passw, host, port)                            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_connecting', message), self._mh.fromhere())
            
            ev = event.Event('email_before_connect', host, self.port, user, passw)
            if (self._mh.fire_event(ev) > 0):
                host = ev.argv(0)
                port = ev.argv(1)
                user = ev.argv(2)
                passw = ev.argv(3)               
            
            self._host = host
            self._port = port
            self._user = user
            self._passw = passw
            
            if (ev.will_run_default()):  
                                
                if (not self._secured):
                    self._client = IMAP4(self.host, self.port) 
                else:
                    self._client = IMAP4_SSL(self.host, self.port) 
                           
                if (self.verbose):
                    self._client.debug = 4                                       
                    
                if (self.user != None):
                    self._client.login(self.user, self.passw)                       
                
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_connected'), self._mh.fromhere()) 
            ev = event.Event('email_after_connect')
            self._mh.fire_event(ev)   
                                                   
            return True
        
        except IMAP4.error, ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False            
                   
    def disconnect(self):
        """Method disconnects from server
           
        Returns:
           bool: result         
                
        """           
         
        try:                                                 
                
            self._client.shutdown()               
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_disconnected'), self._mh.fromhere())  
            return True  
    
        except IMAP4.error, ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False    
        
    def email_count(self):
        """Method gets email count        
           
        Returns: 
           int: count       
                
        """         
                
        try:
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_counting'), self._mh.fromhere())              
            count = int(self._client.select()[1][0])        
              
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_count', count), self._mh.fromhere())      
            return count              
            
        except IMAP4.error, ex: 
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return None      
        
    def list_emails(self):
        """Method gets email list
           
        Returns: 
           list: email ids       
                
        """         
                
        try:
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_listing'), self._mh.fromhere())          
            
            msg_list = self._client.search(None, 'ALL')[1][0]
            emails = msg_list.split(' ')                                                                                                   
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_listed'), self._mh.fromhere())         
            return emails
            
        except IMAP4.error, ex: 
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return None  
        
    def receive_email(self, msg_id):  
        """Method receives email
           
        Args:
           msg_id (str) - email id 
           
        Returns: 
           tuple: sender (str), recipients (list), cc (list), subject (str), message (str)     
           
        Raises:
           event: email_before_receive_email
           event: email_after_receive_email   
                
        """         
                
        try:
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_receiving', msg_id), self._mh.fromhere())  
            
            ev = event.Event('email_before_receive_email', msg_id)
            if (self._mh.fire_event(ev) > 0):
                msg_id = ev.argv(0)          
            
            if (ev.will_run_default()):                        
                msg = self._client.fetch(msg_id, '(RFC822)')[1][0][1]
                msg = msg.split('\r\n')                                                                                                                                      
                
            msg_found = False
            message = ''
            for line in msg:
                if (not msg_found):
                    if ('From: ' in line):
                        sender = replace(line, ('From: '), '')
                    elif ('To: ' in line):
                        recipients = replace(line, ('To: '), '') 
                    elif ('CC: ' in line):
                        cc = replace(line, ('CC: '), '')  
                    elif ('Subject: ' in line):
                        subject = replace(line, ('Subject: '), '')
                    elif ('Inbound message' in line):
                        msg_found = True
                else:
                        message += line + '\r\n'                
                
            ev = event.Event('email_after_receive_email')
            self._mh.fire_event(ev)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_received'), self._mh.fromhere())  

            return [sender, recipients, cc, subject, message]                                                       
            
        except IMAP4.error, ex: 
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return None                                                                            