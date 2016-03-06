# -*- coding: utf-8 -*-
"""This code is part of Hydra Toolkit library

.. module:: hydratk.lib.network.email.imap_client
   :platform: Unix
   :synopsis: IMAP client unit tests library
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core.masterhead import MasterHead
from hydratk.lib.network.email.client import EmailClient
from imaplib import IMAP4, IMAP4_SSL

class TestEmailClient():

    def __init__(self, secured=False, verbose=False):
        
        hook = [
                {'event' : 'email_before_connect', 'callback' : self.handle_event },
                {'event' : 'email_after_connect', 'callback' : self.handle_event },
                {'event' : 'email_before_receive_email', 'callback' : self.handle_event },
                {'event' : 'email_after_receive_email', 'callback' : self.handle_event }                 
               ]
        self._mh = MasterHead.get_head()
        self._mh.register_event_hook(hook)
        self._events = []
        
        self._client = EmailClient('IMAP', secured, verbose)        
        
    def handle_event(self, ev):
        
        self._events.append(ev._id)
        
    def mock_init(self, host, port=None):
        
        pass

    def connect(self, host, port=None, user=None, passw=None, ex=False):                           
        
        def mock_login(self, user, passw):
            
            if (ex):
                raise IMAP4.error('Connect error')                
        
        if (not self._client._secured):
            o_methods = [IMAP4.__init__, IMAP4.login]
            try:
                IMAP4.__init__ = self.mock_init      
                IMAP4.login = mock_login       
                return self._client.connect(host, port, user, passw)
            finally:
                IMAP4.__init__ = o_methods[0]
                IMAP4.login = o_methods[1]
        else:
            o_methods = [IMAP4_SSL.__init__, IMAP4_SSL.login]
            try:
                IMAP4_SSL.__init__ = self.mock_init
                IMAP4_SSL.login = mock_login
                return self._client.connect(host, port, user, passw)
            finally:
                IMAP4_SSL.__init__ = o_methods[0] 
                IMAP4_SSL.login = o_methods[1]
                
    def disconnect(self, ex=False):   
        
        def mock_shutdown(self):
            
            if (ex):
                raise IMAP4.error('Disconnect error')
        
        if (not self._client._secured):
            
            o_methods = [IMAP4.__init__, IMAP4.shutdown]
            try:
                IMAP4.__init__ = self.mock_init
                IMAP4.shutdown = mock_shutdown
                self._client._client = IMAP4(None)
                return self._client.disconnect()
            finally:
                IMAP4.__init__ = o_methods[0]
                IMAP4.quit = o_methods[1]
        else:
            o_methods = [IMAP4_SSL.__init__, IMAP4_SSL.shutdown]
            try:
                IMAP4_SSL.__init__ = self.mock_init
                IMAP4_SSL.shutdown = mock_shutdown
                self._client._client = IMAP4_SSL(None)
                return self._client.disconnect()
            finally:
                IMAP4_SSL.__init__ = o_methods[0]
                IMAP4_SSL.quit = o_methods[1]           
                
    def email_count(self, ex=False):      
        
        def mock_select(self):
            
            if (ex):
                raise IMAP4.error('Email count error')
            
            return ['return', ('10', 'xx')]   
        
        if (not self._client._secured):
            o_methods = [IMAP4.__init__, IMAP4.select]
            try:
                IMAP4.__init__ = self.mock_init
                IMAP4.select = mock_select
                self._client._client = IMAP4(None)
                return self._client.email_count()
            finally:
                IMAP4.__init__ = o_methods[0]
                IMAP4.select = o_methods[1]
        else:
            o_methods = [IMAP4_SSL.__init__, IMAP4_SSL.select]
            try:
                IMAP4_SSL.__init__ = self.mock_init
                IMAP4_SSL.select = mock_select
                self._client._client = IMAP4_SSL(None)
                return self._client.email_count()
            finally:
                IMAP4_SSL.__init__ = o_methods[0]
                IMAP4_SSL.select = o_methods[1]      
                
    def list_emails(self, ex=False):        
        
        def mock_search(self, dummy, filter):   
            
            if (ex):
                raise IMAP4.error('List emails error')
            
            emails = ['return', (['1 2 3'])]
            return emails  
        
        if (not self._client._secured):
            o_methods = [IMAP4.__init__, IMAP4.search]
            try:
                IMAP4.__init__ = self.mock_init
                IMAP4.search = mock_search
                self._client._client = IMAP4(None)
                return self._client.list_emails()
            finally:
                IMAP4.__init__ = o_methods[0]
                IMAP4.search = o_methods[1]
        else:
            o_methods = [IMAP4_SSL.__init__, IMAP4_SSL.search]
            try:
                IMAP4_SSL.__init__ = self.mock_init
                IMAP4_SSL.search = mock_search
                self._client._client = IMAP4_SSL(None)
                return self._client.list_emails()
            finally:
                IMAP4_SSL.__init__ = o_methods[0]
                IMAP4_SSL.search = o_methods[1]             
        
    def receive_email(self, msg_id, ex=False):

        def mock_fetch(self, msg_id, rfc):
            
            if (ex):
                raise IMAP4.error('Receive email error')
            
            email = (
                     'Header 1',
                     (
                      (
                      'Header 2',
                      '\r\n'.join(
                      [
                      'From: hydra@hydratk.org',
                      'To: hydra2@hydratk.org,hydra3@hydratk.org',
                      'CC: hydra4@hydratk.org,hydra5@hydratk.org',
                      'Subject: Test email',
                      'Inbound message',
                      'Line 1',
                      'Line 2',
                      'Line 3'
                      ])
                      ),
                      ''
                     )
                    )
            
            return email
            
        if (not self._client._secured):
            o_methods = [IMAP4.__init__, IMAP4.fetch]
            try:
                IMAP4.__init__ = self.mock_init
                IMAP4.fetch = mock_fetch
                self._client._client = IMAP4(None)
                return self._client.receive_email(msg_id)
            finally:
                IMAP4.__init__ = o_methods[0]
                IMAP4.retr = o_methods[1]
        else:
            o_methods = [IMAP4_SSL.__init__, IMAP4_SSL.fetch]
            try:
                IMAP4_SSL.__init__ = self.mock_init
                IMAP4_SSL.fetch = mock_fetch
                self._client._client = IMAP4_SSL(None)
                return self._client.receive_email(msg_id)
            finally:
                IMAP4_SSL.__init__ = o_methods[0]
                IMAP4_SSL.retr = o_methods[1]              