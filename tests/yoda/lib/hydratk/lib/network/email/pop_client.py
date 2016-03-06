# -*- coding: utf-8 -*-
"""This code is part of Hydra Toolkit library

.. module:: hydratk.lib.network.email.pop_client
   :platform: Unix
   :synopsis: POP client unit tests library
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core.masterhead import MasterHead
from hydratk.lib.network.email.client import EmailClient
from poplib import POP3, POP3_SSL, error_proto

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
        
        self._client = EmailClient('POP', secured, verbose)        
        
    def handle_event(self, ev):
        
        self._events.append(ev._id)
        
    def mock_init(self, host, port=None):
        
        pass

    def connect(self, host, port=None, user=None, passw=None, ex=False):                   
        
        def mock_set_debuglevel(self, level):
            
            pass
        
        def mock_user(self, user):
            
            pass
        
        def mock_pass_(self, passw):
            
            if (ex):
                raise error_proto('Connect error')                
        
        if (not self._client._secured):
            o_methods = [POP3.__init__, POP3.set_debuglevel, POP3.user, POP3.pass_]
            try:
                POP3.__init__ = self.mock_init      
                POP3.set_debug_level = mock_set_debuglevel
                POP3.user = mock_user
                POP3.pass_ = mock_pass_          
                return self._client.connect(host, port, user, passw)
            finally:
                POP3.__init__ = o_methods[0]
                POP3.set_debug_level = o_methods[1]
                POP3.user = o_methods[2]
                POP3.pass_ = o_methods[3]
        else:
            o_methods = [POP3_SSL.__init__, POP3_SSL.set_debuglevel, POP3_SSL.user, POP3_SSL.pass_]
            try:
                POP3_SSL.__init__ = self.mock_init
                POP3_SSL.set_debuglevel = mock_set_debuglevel
                POP3_SSL.user = mock_user
                POP3_SSL.pass_ = mock_pass_
                return self._client.connect(host, port, user, passw)
            finally:
                POP3_SSL.__init__ = o_methods[0] 
                POP3_SSL.set_debug_level = o_methods[1]
                POP3_SSL.user = o_methods[2]
                POP3_SSL.pass_ = o_methods[3] 
                
    def disconnect(self, ex=False):   
        
        def mock_quit(self):
            
            if (ex):
                raise error_proto('Disconnect error')
        
        if (not self._client._secured):
            
            o_methods = [POP3.__init__, POP3.quit]
            try:
                POP3.__init__ = self.mock_init
                POP3.quit = mock_quit
                self._client._client = POP3(None)
                return self._client.disconnect()
            finally:
                POP3.__init__ = o_methods[0]
                POP3.quit = o_methods[1]
        else:
            o_methods = [POP3_SSL.__init__, POP3_SSL.quit]
            try:
                POP3_SSL.__init__ = self.mock_init
                POP3_SSL.quit = mock_quit
                self._client._client = POP3_SSL(None)
                return self._client.disconnect()
            finally:
                POP3_SSL.__init__ = o_methods[0]
                POP3_SSL.quit = o_methods[1]           
                
    def email_count(self, ex=False):      
        
        def mock_stat(self):
            
            if (ex):
                raise error_proto('Email count error')
            
            return [10]   
        
        if (not self._client._secured):
            o_methods = [POP3.__init__, POP3.stat]
            try:
                POP3.__init__ = self.mock_init
                POP3.stat = mock_stat
                self._client._client = POP3(None)
                return self._client.email_count()
            finally:
                POP3.__init__ = o_methods[0]
                POP3.stat = o_methods[1]
        else:
            o_methods = [POP3_SSL.__init__, POP3_SSL.stat]
            try:
                POP3_SSL.__init__ = self.mock_init
                POP3_SSL.stat = mock_stat
                self._client._client = POP3_SSL(None)
                return self._client.email_count()
            finally:
                POP3_SSL.__init__ = o_methods[0]
                POP3_SSL.stat = o_methods[1]      
                
    def list_emails(self, ex=False):        
        
        def mock_list(self):   
            
            if (ex):
                raise error_proto('List emails error')
            
            emails = ['return', ['1 email1', '2 email2', '3 email3']]
            return emails  
        
        if (not self._client._secured):
            o_methods = [POP3.__init__, POP3.list]
            try:
                POP3.__init__ = self.mock_init
                POP3.list = mock_list
                self._client._client = POP3(None)
                return self._client.list_emails()
            finally:
                POP3.__init__ = o_methods[0]
                POP3.list = o_methods[1]
        else:
            o_methods = [POP3_SSL.__init__, POP3_SSL.list]
            try:
                POP3_SSL.__init__ = self.mock_init
                POP3_SSL.list = mock_list
                self._client._client = POP3_SSL(None)
                return self._client.list_emails()
            finally:
                POP3_SSL.__init__ = o_methods[0]
                POP3_SSL.list = o_methods[1]             
        
    def receive_email(self, msg_id, ex=False):

        def mock_retr(self, msg_id):
            
            if (ex):
                raise error_proto('Receive email error')
            
            email = (
                     'Header',
                     [
                      'From: hydra@hydratk.org',
                      'To: hydra2@hydratk.org,hydra3@hydratk.org',
                      'CC: hydra4@hydratk.org,hydra5@hydratk.org',
                      'Subject: Test email',
                      'Inbound message',
                      'Line 1',
                      'Line 2',
                      'Line 3'
                     ]
                    )
            return email
            
        if (not self._client._secured):
            o_methods = [POP3.__init__, POP3.retr]
            try:
                POP3.__init__ = self.mock_init
                POP3.retr = mock_retr
                self._client._client = POP3(None)
                return self._client.receive_email(msg_id)
            finally:
                POP3.__init__ = o_methods[0]
                POP3.retr = o_methods[1]
        else:
            o_methods = [POP3_SSL.__init__, POP3_SSL.retr]
            try:
                POP3_SSL.__init__ = self.mock_init
                POP3_SSL.retr = mock_retr
                self._client._client = POP3_SSL(None)
                return self._client.receive_email(msg_id)
            finally:
                POP3_SSL.__init__ = o_methods[0]
                POP3_SSL.retr = o_methods[1]              