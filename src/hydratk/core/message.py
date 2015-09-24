'''
Created on 23.10.2009

@author: CzadernaP

Core communication messages definitions
'''

REQUEST          = 1;   '''request'''
RESPONSE         = 2;   '''info'''
INFO             = 3;   '''info'''
SERVICE_STATUS   = 4;   '''info'''
MONITOR          = 5;   '''request'''
SERVICE_IDENT    = 6;   '''info'''
SERVICES_MAP     = 7;   '''info'''
SERVICE_SHUTDOWN = 8;   '''info'''
SERVICE_HELLO    = 9;   '''info, new ident alternative'''
PING             = 10;  '''request'''
PONG             = 11;  '''response'''
COPY             = 12;  '''msg copy for the monitor request'''
SERVICE_ALERT    = 13;  '''info'''
SERVICE_ERROR    = 99;  '''info'''
SERVICE_DROPPED  = 100; '''info'''
SERVICE_KILLED   = 101; '''info'''
DUMMY_FIRST      = 300; '''dummy 1st test message'''
DUMMY            = 301; '''dummy test message'''
DUMMY_LAST       = 302; '''dummy test message'''
''' messages with number < 500 are core reserved numbers''' 

