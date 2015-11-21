# -*- coding: utf-8 -*-
"""This code is part of Hydra Toolkit library

.. module:: network.email.client
   :platform: Unix
   :synopsis: Generic EMAIL client for protocols: SMTP, SMTPS, IMAP, IMAPS, POP, POPS
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
email_before_connect
email_after_connect
email_before_send_email
email_after_send_email
email_before_receive_email
email_after_receive_email

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
import smtplib
import imaplib
import poplib
import string

default_ports = {
  'SMTP'  : 25,
  'SMTPS' : 465,
  'IMAP'  : 143,
  'IMAPS' : 993,
  'POP'   : 110,
  'POPS'  : 995
}

class EmailClient:
    
    _mh = None
    _client = None
    _protocol = None
    _host = None    
    _port = None
    _user = None
    _passw = None
    _verbose = None
    
    def __init__(self, protocol='SMTP', verbose=False):
        """Class constructor
           
        Called when the object is initialized 
        
        Args:
           protocol (str):  EMAIL protocol, SMTP|SMTPS|IMAP|IMAP|POP|POPS          
           verbose (bool): verbose mode
           
        """         
        
        self._mh = MasterHead.get_head()
        self.protocol = protocol.upper()  
              
        if (self.protocol == 'SMTP'):            
            self._client = smtplib.SMTP()
        elif (self.protocol == 'SMTPS'):
            self._client = smtplib.SMTP_SSL()   
        elif (self.protocol not in ('SMTP', 'SMTPS', 'IMAP', 'IMAPS', 'POP', 'POPS')):
            self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_email_unknown_protocol', self.protocol), self._mh.fromhere())
            return None
                         
        self.verbose = verbose 
        if (self.verbose):
            if (self.protocol in('SMTP', 'SMTPS')):                
                self._client.set_debuglevel(2)
                
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
            
            self.port = port if (port != None) else default_ports[self.protocol]
            message = '{0}/{1}@{2}:{3}'.format(user, passw, host, self.port)                            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_connecting', message), self._mh.fromhere())
            
            ev = event.Event('email_before_connect', host, self.port, user, passw)
            if (self._mh.fire_event(ev) > 0):
                host = ev.argv(0)
                self.port = ev.argv(1)
                user = ev.argv(2)
                passw = ev.argv(3)               
            
            self.host = host
            self.user = user
            self.passw = passw
            
            if (ev.will_run_default()):                  
                if (self.protocol in ('SMTP', 'SMTPS')):
                    self._client.connect(self.host, self.port)
                elif (self.protocol == 'IMAP'):
                    self._client = imaplib.IMAP4(self.host, self.port)
                    if (self.verbose):
                        self._client.debug = 2 
                elif (self.protocol == 'IMAPS'):
                    self._client = imaplib.IMAP4_SSL(self.host, self.port)
                    if (self.verbose):
                        self._client.debug = 2                         
                elif (self.protocol == 'POP'):
                    self._client = poplib.POP3(self.host, self.port) 
                    if (self.verbose):
                        self._client.set_debuglevel(2)
                elif (self.protocol == 'POPS'):
                    self._client = poplib.POP3_SSL(self.host, self.port) 
                    if (self.verbose):
                        self._client.set_debuglevel(2)                        
                    
                if (self.user != None):
                    if (self.protocol in ('SMTP', 'SMTPS', 'IMAP', 'IMAPS')):
                        self._client.login(self.user, self.passw) 
                    elif (self.protocol in ('POP', 'POPS')):
                        self._client.user(self.user)
                        self._client.pass_(self.passw)                                
                
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_connected'), self._mh.fromhere()) 
            ev = event.Event('email_after_connect')
            self._mh.fire_event(ev)   
                                                   
            return True
        
        except (smtplib.SMTPException, imaplib.IMAP4.error, poplib.error_proto), ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False            
                   
    def disconnect(self):
        """Method disconnects from server
           
        Returns:
           bool: result         
                
        """           
         
        try:                                                 
                
            if (self.protocol in ('SMTP', 'SMTPS', 'POP', 'POPS')):    
                self._client.quit()
            elif (self.protocol in ('IMAP', 'IMAPS')):
                self._client.shutdown()
                
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_disconnected'), self._mh.fromhere())  
            return True  
    
        except (smtplib.SMTPException, imaplib.IMAP4.error, poplib.error_proto), ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False  
        
    def send_email(self, subject, message, sender='hydra@hydratk.org', recipients=['hydra@hydratk.org'],
                   cc=[], bcc=[]):   
        """Method sends email
        
        Supported for SMTP, SMTPS protocols only
        
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
                if (self.protocol in ('SMTP', 'SMTPS')):
                    msg = 'From: {0}\r\n'.format(sender) + \
                          'To: {0}\r\n'.format(','.join(recipients)) + \
                          'CC: {0}\r\n'.format(','.join(cc)) + \
                          'Subject: {0}\r\n'.format(subject) + \
                          '\r\n{0}'.format(message)
                    self._client.sendmail(sender, recipients+cc+bcc, msg)
                else:
                    self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_email_unknown_method', self.protocol), self._mh.fromhere())
                    return False
                
            ev = event.Event('email_after_send_email')
            self._mh.fire_event(ev)                   
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_sent'), self._mh.fromhere())
            
            return True
            
        except smtplib.SMTPException, ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False 
        
    def email_count(self):
        """Method gets email count
        
        Supported for POP, POPS, IMAP, IMAPS protocols only
           
        Returns: 
           int: count       
                
        """         
                
        try:
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_counting'), self._mh.fromhere())  
            
            if (self.protocol in ('POP', 'POPS')):
                count = self._client.stat()[0]  
            elif (self.protocol in ('IMAP', 'IMAPS')):
                count = int(self._client.select()[1][0])                
            else:
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_email_unknown_method', self.protocol), self._mh.fromhere())
                return None        
              
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_count', count), self._mh.fromhere())      
            return count              
            
        except (imaplib.IMAP4.error, poplib.error_proto), ex: 
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return None      
        
    def list_emails(self):
        """Method gets email list
        
        Supported for POP, POPS, IMAP, IMAPS protocols only
           
        Returns: 
           list: email ids       
                
        """         
                
        try:
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_listing'), self._mh.fromhere())          
            
            if (self.protocol in ('POP', 'POPS')):
                msg_list = self._client.list()[1]                                 
                emails = []
                for msg in msg_list:
                    emails.append(msg.split(' ')[0])                  
            elif (self.protocol in ('IMAP', 'IMAPS')):
                msg_list = self._client.search(None, 'ALL')[1][0]
                emails = msg_list.split(' ')                                          
            else: 
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_email_unknown_method', self.protocol), self._mh.fromhere())
                return None                                                                                     
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_listed'), self._mh.fromhere())         
            return emails
            
        except (imaplib.IMAP4.error, poplib.error_proto), ex: 
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return None  
        
    def receive_email(self, msg_id):  
        """Method receives email
        
        Supported for POP, POPS, IMAP, IMAPS protocols only
           
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
                if (self.protocol in ('POP', 'POPS')):
                    msg = self._client.retr(msg_id)[1]                                                                                                                                      
                elif (self.protocol in ('IMAP', 'IMAPS')):
                    msg = self._client.fetch(msg_id, '(RFC822)')[1][0][1]
                    msg = msg.split('\r\n')
                else: 
                    self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_email_unknown_method', self.protocol), self._mh.fromhere())
                    return None 
                
            msg_found = False
            message = ''
            for line in msg:
                if (not msg_found):
                    if ('From: ' in line):
                        sender = string.replace(line, ('From: '), '')
                    elif ('To: ' in line):
                        recipients = string.replace(line, ('To: '), '') 
                    elif ('CC: ' in line):
                        cc = string.replace(line, ('CC: '), '')  
                    elif ('Subject: ' in line):
                        subject = string.replace(line, ('Subject: '), '')
                    elif ('Inbound message' in line):
                        msg_found = True
                else:
                        message += line + '\r\n'                
                
            ev = event.Event('email_after_receive_email')
            self._mh.fire_event(ev)
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_email_received'), self._mh.fromhere())  

            return [sender, recipients, cc, subject, message]                                                       
            
        except (imaplib.IMAP4.error, poplib.error_proto), ex: 
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return None                                                                                              