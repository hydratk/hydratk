# -*- coding: utf-8 -*-
"""This code is part of Hydra Toolkit library

.. module:: network.email.smtp_client
   :platform: Unix
   :synopsis: SMTP email client
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
email_before_connect
email_after_connect
email_before_send_email
email_after_send_email

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from smtplib import SMTP, SMTP_SSL, SMTPException

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
           secured (bool): secured SMTP        
           verbose (bool): verbose mode
           
        """         
        
        self._mh = MasterHead.get_head() 
         
        self._secured = secured     
        if (not self._secured):            
            self._client = SMTP()
        else:
            self._client = SMTP_SSL()   
                         
        self._verbose = verbose 
        if (self.verbose):              
            self._client.set_debuglevel(2)
            
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
                port = 25 if (not self._secured) else 465
                
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
                self._client.connect(self.host, self.port)                      
                    
                if (self.user != None):
                    self._client.login(self.user, self.passw)                         
                
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_connected'), self._mh.fromhere()) 
            ev = event.Event('email_after_connect')
            self._mh.fire_event(ev)   
                                                   
            return True
        
        except SMTPException, ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False            
                   
    def disconnect(self):
        """Method disconnects from server
           
        Returns:
           bool: result         
                
        """           
         
        try:                                                 
                
            self._client.quit()                
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_disconnected'), self._mh.fromhere())  
            return True  
    
        except SMTPException, ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False  
        
    def send_email(self, subject, message, sender='hydra@hydratk.org', recipients=['hydra@hydratk.org'],
                   cc=[], bcc=[]):   
        """Method sends email
        
        Args:
           subject (str): email subject
           message (str): email content, string, mandatory
           sender (str): from email address 
           recipients (list): to email addresses   
           cc (list): carbon copy email addresses
           bcc (list): blind carbon copy email addresses  
           
        Returns:
           bool: result       
           
        Raises:
           event: email_before_send_email
           event: email_after_send_email
                
        """  
        
        try:
            
            msg = 'From:{0}, To:{1}, CC:{2}, BCC:{3}, Subject:{4}'.format(sender, recipients, cc, bcc, subject)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_sending', msg), self._mh.fromhere())
            
            ev = event.Event('email_before_send_email', subject, message, sender, recipients, cc, bcc)
            if (self._mh.fire_event(ev) > 0):
                subject = ev.argv(0)
                message = ev.argv(1)
                sender = ev.argv(2)
                recipients = ev.argv(3)
                cc = ev.argv(4)
                bcc = ev.argv(5)
                
            if (ev.will_run_default()):
                msg = 'From: {0}\r\n'.format(sender) + \
                      'To: {0}\r\n'.format(','.join(recipients)) + \
                      'CC: {0}\r\n'.format(','.join(cc)) + \
                      'Subject: {0}\r\n'.format(subject) + \
                      '\r\n{0}'.format(message)
                self._client.sendmail(sender, recipients+cc+bcc, msg)
                
            ev = event.Event('email_after_send_email')
            self._mh.fire_event(ev)                   
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_sent'), self._mh.fromhere())
            
            return True
            
        except SMTPException, ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False 
                                                              