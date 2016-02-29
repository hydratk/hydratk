# -*- coding: utf-8 -*-
"""This code is part of Hydra Toolkit library

.. module:: hydratk.lib.network.ldap.client
   :platform: Unix
   :synopsis: LDAP client unit tests library
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core.masterhead import MasterHead
from hydratk.lib.network.ldap.client import LDAPClient
import ldap
from ldap import LDAPError, ldapobject

class TestLDAPClient():

    def __init__(self, verbose=False):
        
        hook = [
                {'event' : 'ldap_before_connect', 'callback' : self.handle_event },
                {'event' : 'ldap_after_connect', 'callback' : self.handle_event },
                {'event' : 'ldap_before_read', 'callback' : self.handle_event },
                {'event' : 'ldap_after_read', 'callback' : self.handle_event },        
                {'event' : 'ldap_before_create', 'callback' : self.handle_event },
                {'event' : 'ldap_after_create', 'callback' : self.handle_event },  
                {'event' : 'ldap_before_update', 'callback' : self.handle_event },
                {'event' : 'ldap_after_update', 'callback' : self.handle_event },  
                {'event' : 'ldap_before_delete', 'callback' : self.handle_event },
                {'event' : 'ldap_after_delete', 'callback' : self.handle_event }                                                                   
               ]
        self._mh = MasterHead.get_head()
        self._mh.register_event_hook(hook)
        self._events = []
        
        self._client = LDAPClient(verbose)
        
    def handle_event(self, ev):
        
        self._events.append(ev._id)

    def connect(self, host, base_dn, port=None, secured=False, user=None, passw=None, ex=False):   
        
        def mock_initialize(self, uri):
            
            pass                       
            
        def mock_simple_bind_s(self, user, passw):
            
            if (ex):                
                raise LDAPError('Connect error')
        
        o_methods = [ldap.initialize, ldapobject.LDAPObject.simple_bind_s]
        try:
            ldap.initialize = mock_initialize
            ldapobject.LDAPObject.simple_bind_s = mock_simple_bind_s
            return self._client.connect(host, base_dn, port, secured, user, passw)
        finally:
            ldap.initialize = o_methods[0]
            ldapobject.LDAPObject.simple_bind_s = o_methods[1]
            
    def disconnect(self, ex=False):
        
        def mock_unbind(self):
            
            if (ex):
                raise LDAPError('Disconnect error')
        
        o_method = ldapobject.LDAPObject.unbind     
        try:
            ldapobject.LDAPObject.unbind = mock_unbind
            return self._client.disconnect()
        finally:
            ldapobject.LDAPObject.unbind = o_method  
            
    def read(self, rdn=None, filter='objectClass=*', attrs=[], fetch_one=False, get_child=True,
             cn_only=False, attrs_only=False, ex=False):
        
        def mock_search_s(self, base, scope, filterstr, attrlist):
            
            if (ex):
                raise LDAPError('Read error')
        
            base_dn = 'dc=test,dc=com'            
            if (rdn == 'ou=users' and filter == 'objectClass=*'):
                records = [('ou=users', {})]
                records.append(('cn=bowman,{0},{1}'.format(rdn, base_dn), {'sn':'Bowman', 'givenName':'Charlie'})) 
                records.append(('cn=neil,{0},{1}'.format(rdn, base_dn), {'sn':'Neil', 'givenName':'Vince'}))
            elif (rdn == 'cn=bowman,ou=users' or (rdn == 'ou=users' and filter == 'cn=bowman')):
                records = [('{0},{1}'.format(rdn, base_dn), {'sn':'Bowman', 'givenName':'Charlie'})]           
                
            if (not get_child):
                records = [records[0]]
            if (attrs == ['sn']):
                records_new = []
                for record in records:
                    records_new.append((record[0], {'sn':record[1]['sn']}))
                records = records_new   
                
            return records
        
        o_method = ldapobject.LDAPObject.search_s
        try:
            ldapobject.LDAPObject.search_s = mock_search_s
            return self._client.read(rdn, filter, attrs, fetch_one, get_child, cn_only, attrs_only)
        finally:
            ldapobject.LDAPObject.search_s = o_method            
            
    def create(self, rdn, attrs={}, ex=False):
        
        def mock_add_s(self, dn, ldif):
            
            if (ex):
                raise LDAPError('Create error')
        
        o_method = ldapobject.LDAPObject.add_s
        try:
            ldapobject.LDAPObject.add_s = mock_add_s
            return self._client.create(rdn, attrs)
        finally:
            ldapobject.LDAPObject.add_s = o_method        
            
    def update(self, rdn, attrs, ex=False):
        
        def mock_modify_s(self, dn, ldif):
            
            pass
        
        def mock_modrdn_s(self, dn, rdn_new):
            
            if (ex):
                raise LDAPError('Update error')
        
        o_methods = [ldapobject.LDAPObject.modify_s, ldapobject.LDAPObject.modrdn_s]
        try:
            ldapobject.LDAPObject.modify_s = mock_modify_s
            ldapobject.LDAPObject.modrdn_s = mock_modrdn_s
            return self._client.update(rdn, attrs)
        finally:
            ldapobject.LDAPObject.modify_s = o_methods[0]  
            ldapobject.LDAPObject.modrdn_s = o_methods[1]  
            
    def delete(self, rdn, ex=False):
        
        def mock_delete_s(self, dn):
            
            if (ex):
                raise LDAPError('Delete error')
        
        o_method = ldapobject.LDAPObject.delete_s
        try:
            ldapobject.LDAPObject.delete_s = mock_delete_s
            return self._client.delete(rdn)
        finally:
            ldapobject.LDAPObject.delete_s = o_method                                         