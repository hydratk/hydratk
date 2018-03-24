# -*- coding: utf-8 -*-
"""Message queue general factory class

.. module:: lib.messaging.queue
   :platform: Unix
   :synopsis: Message queue general factory class
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

from pyx.system.utils import Utils
from hydratk.core.masterhead import MasterHead

QUEUE_TYPE_SERVER = 1
QUEUE_TYPE_CLIENT = 2

mh = MasterHead.get_head()

class Queue():
    """Class Queue
    """

    __impl_q = {
        'native': 'multiprocessing',
        'zmq': 'zmq'
    }
    __qobj = None
    __qdriver = None

    def __init__(self, qdriver, *args):
        """Class constructor

        Called when object is initialized

        Args:
           qdriver (str): queue driver
           args (args): arguments

        Raises:
           error: ValueError

        """

        self._mh = MasterHead.get_head()

        if Queue.is_available(qdriver):
            drv_call = 'pyx.messaging.' + qdriver + 'queue.Queue(*args)'
            q = None
            estr = 'q = ' + drv_call
            exec estr
            self.__qdriver = qdriver
            self.__qobj = q
        else:
            raise ValueError(mh._trn.msg('htk_lib_queue_not_loaded', qdriver, Queue.__impl_q[qdriver]))

    @staticmethod
    def is_available(qdriver):
        """Methods checks if queue driver is available

        Args:
           qdriver (str): queue driver module

        Returns:
           bool: result

        Raises:
           error: ValueError

        """

        if qdriver in Queue.__impl_q:
            result = True if Utils.module_loaded(
                Queue.__impl_q[qdriver]) else False
        else:
            raise ValueError(mh._trn.msg('htk_lib_queue_not_supported', qdriver))
        return result
