# -*- coding: utf-8 -*-
"""This code is part of Hydra Toolkit library

.. module:: hydratk.lib.network.email.smtp_client
   :platform: Unix
   :synopsis: SMTP client unit tests library
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core.masterhead import MasterHead
from hydratk.lib.network.email.client import EmailClient
from smtplib import SMTP, SMTP_SSL, SMTPException

class TestEmailClient():

    def __init__(self, secured=False, verbose=False):
        
        hook = [
                {'event' : 'email_before_connect', 'callback' : self.handle_event },
                {'event' : 'email_after_connect', 'callback' : self.handle_event },
                {'event' : 'email_before_send_email', 'callback' : self.handle_event },
                {'event' : 'email_after_send_email', 'callback' : self.handle_event }                 
               ]
        self._mh = MasterHead.get_head()
        self._mh.register_event_hook(hook)
        self._events = []
        
        self._client = EmailClient('SMTP', secured, verbose)
        
    def handle_event(self, ev):
        
        self._events.append(ev._id)

    def connect(self, host, port=None, user=None, passw=None, ex=False):           
        
        def mock_connect(self, host, port):
            
            pass
        
        def mock_login(self, user, passw):
            
            if (ex):
                raise SMTPException('Connect error')
        
        if (not self._client._secured):
            o_methods = [SMTP.connect, SMTP.login]
            try:
                SMTP.connect = mock_connect
                SMTP.login = mock_login
                return self._client.connect(host, port, user, passw)
            finally:
                SMTP.connect = o_methods[0]
                SMTP.login = o_methods[1] 
        else:
            o_methods = [SMTP_SSL.connect, SMTP_SSL.login]
            try:
                SMTP_SSL.connect = mock_connect
                SMTP_SSL.login = mock_login
                return self._client.connect(host, port, user, passw)
            finally:
                SMTP_SSL.connect = o_methods[0]
                SMTP_SSL.login = o_methods[1]                
            
    def disconnect(self, ex=False):   
        
        def mock_quit(self):
            
            if (ex):
                raise SMTPException('Disconnect error')
        
        if (not self._client._secured):
            o_method = SMTP.quit
            try:
                SMTP.quit = mock_quit
                return self._client.disconnect()
            finally:
                SMTP.quit = o_method
        else:
            o_method = SMTP_SSL.quit
            try:
                SMTP_SSL.quit = mock_quit
                return self._client.disconnect()
            finally:
                SMTP_SSL.quit = o_method
            
    def send_email(self, subject, message, sender='hydra@hydratk.org', recipients=['hydra@hydratk.org'],
                   cc=[], bcc=[], ex=False):
        
        def mock_sendmail(self, sender, recipients, msg):
            
            if (ex):
                raise SMTPException('Send email error')
        
        if (not self._client._secured):
            o_method = SMTP.sendmail
            try:
                SMTP.sendmail = mock_sendmail
                return self._client.send_email(subject, message, sender, recipients, cc, bcc)
            finally:
                SMTP.sendmail = o_method
        else:
            o_method = SMTP_SSL.sendmail
            try:
                SMTP_SSL.sendmail = mock_sendmail
                return self._client.send_email(subject, message, sender, recipients, cc, bcc)
            finally:
                SMTP_SSL.sendmail = o_method      