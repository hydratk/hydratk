# -*- coding: utf-8 -*-
"""HydraTK signals

.. module:: core.signal
   :platform: Unix
   :synopsis: HydraTK signals
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import signal

sig2event = {
  signal.SIGTERM  : 'htk_on_sigterm',
  signal.SIGINT   : 'htk_on_sigint',
  signal.SIGPIPE  : 'htk_on_sigpipe',
  signal.SIGALRM  : 'htk_on_sigalarm'
}

sigint2string = {
  signal.SIGTERM : 'SIGTERM',
  signal.SIGINT  : 'SIGINT',
  signal.SIGALRM : 'SIGALARM',
  signal.SIGPIPE : 'SIGPIPE'
}