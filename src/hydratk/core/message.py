'''
Created on 23.10.2009

@author: CzadernaP

Core communication messages definitions
'''

'''request'''
REQUEST          = 1   
'''info'''
RESPONSE         = 2 
'''info'''  
INFO             = 3
'''info'''   
SERVICE_STATUS   = 4
'''request'''   
MONITOR          = 5
'''info'''   
SERVICE_IDENT    = 6
'''info'''   
SERVICES_MAP     = 7
'''info'''   
SERVICE_SHUTDOWN = 8
'''info, new ident alternative'''   
SERVICE_HELLO    = 9
'''request'''   
PING             = 10
'''response'''  
PONG             = 11
'''msg copy for the monitor request'''  
COPY             = 12
'''info'''  
SERVICE_ALERT    = 13
'''info'''  
SERVICE_ERROR    = 99
'''info'''  
SERVICE_DROPPED  = 100
'''info''' 
SERVICE_KILLED   = 101
'''dummy 1st test message''' 
DUMMY_FIRST      = 300
'''dummy test message''' 
DUMMY            = 301
'''dummy test message''' 
DUMMY_LAST       = 302 
''' messages with number < 500 are core reserved numbers''' 

