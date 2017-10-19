# -*- coding: utf-8 -*-
"""Benchmark tests focused on event processing

.. module:: benchmark.tests.event
   :platform: Unix
   :synopsis: Benchmark tests focused on event processing.
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from random import randint

tests = [
    'throughput'
]

def throughput(n=10000):
    """Method tests event throughput

    Args:
        n (int): count of events

    Returns:
        void

    """

    def _event_cb(ev):

        ev.get_data('random')
        return True
    
    mh = MasterHead.get_head()
    hook = {'event': 'benchmark_test_event1',
            'callback': _event_cb, 'unpack_args': True}
    mh.register_event_hook(hook)

    for i in range(n):
        ev = event.Event('benchmark_test_event1')
        num = randint(0, 9)
        ev.set_data('random', ('%s' % str(num)) * 1024)
        mh.fire_event(ev)
