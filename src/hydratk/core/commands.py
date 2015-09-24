'''
Created on 3.11.2009

@author: CzadernaP
'''
commands          = [
                    'create-config-db', 
                    'start',
                    'stop',
                    'help',
                    'list-extensions' 
                    ];
                    
long_opts         = [
                     'debug',
                     'config',
                     'config-db-file',
                     'force',
                     'language',
                     'cluster',
                     'cluster-node-type'
                    ];
short_opts        = 'dclxt';

getopt_long_opts  = [
                     'config=',
                     'config-db-file=',
                     'debug=',
                     'force',
                     'language=',
                     'cluster',
                     'cluster-node-type='
                    ];
getopt_short_opts = 'c:d:fl:t:x';                    