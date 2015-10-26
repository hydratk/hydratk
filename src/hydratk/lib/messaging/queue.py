"""This code is a part of Pyx application framework

.. module:: messaging.queue
   :platform: Unix
   :synopsis: A Message queue general factory class.
.. moduleauthor:: Petr Czaderna <pc@headz.cz>

"""

from pyx.system.utils import Utils

QUEUE_TYPE_SERVER=1
QUEUE_TYPE_CLIENT=2

class Queue():
    __impl_q = {
                'native' : 'multiprocessing',
                'zmq'    : 'zmq'
                }
    __qobj   = None
    __qdriver  = None


    def __init__(self, qdriver, *args):
        if Queue.is_available(qdriver):
            drv_call = 'pyx.messaging.'+qdriver+'queue.Queue(*args)'
            q = None        
            estr = 'q = ' + drv_call
            exec estr
            self.__qdriver = qdriver                        
            self.__qobj = q
        else:
            raise ValueError(qdriver + ' queue is not available, it requires module '+ Queue.__impl_q[qdriver] + ' to be loaded first')
    
    @staticmethod
    def is_available(qdriver):        
        if qdriver in Queue.__impl_q:
            result = True if Utils.module_loaded(Queue.__impl_q[qdriver]) else False
        else:
            raise ValueError('Queue type: '+qdriver+ ' is not supported')
        return result     