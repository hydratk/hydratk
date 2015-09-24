'''
Created on 3.12.2009

@author: CzadernaP
'''
import signal;

sig2event = {
  signal.SIGTERM  : 'htk_on_sigterm',
  signal.SIGINT   : 'htk_on_sigint',
  signal.SIGPIPE  : 'htk_on_sigpipe',
  signal.SIGALRM  : 'htk_on_sigalarm'
};

sigint2string = {
  signal.SIGTERM : 'SIGTERM',
  signal.SIGINT  : 'SIGINT',
  signal.SIGALRM : 'SIGALARM',
  signal.SIGPIPE : 'SIGPIPE'
};