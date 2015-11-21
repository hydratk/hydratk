# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit library

.. module:: lib.messaging.native.queue
   :platform: Unix
   :synopsis: A Python native multiprocessing Managed queue driver
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

from pyx.messaging import queue
from multiprocessing import Queue
from multiprocessing.managers import SyncManager

class Queue():
    __type    = None
    __manager = None
    __address = None
    __authkey = None
    
    
    def __init__(self, qtype, address, authkey = ''):
        if type in (queue.QUEUE_TYPE_SERVER,queue.QUEUE_TYPE_CLIENT):
            self.__type = qtype
        else: raise ValueError('Invalid Queue type')
        
        ''' Checking for address format AF_INET '''
        if address.find(':') > 0: 
            address = address.split(':')
                    
        self.__address = address
        self.__authkey = authkey 
        
    
    def create(self):
        if self.__type != queue.QUEUE_TYPE_SERVER:
            raise ValueError('This operation cannot be done on this queue type')
        
        q = Queue()
        SyncManager.register('get_queue', callable = lambda: q)
        self.__manager = SyncManager(self.__address, self.__authkey)        
        self.__manager.start()
            
    def destroy(self):
        self.__manager.shutdown()
        
    def connect(self):
        if self.__type != queue.QUEUE_TYPE_CLIENT:
            raise ValueError('This operation cannot be done on this queue type')
        
        q = Queue()
        SyncManager.register('get_queue', callable = lambda: q)
        self.__manager = SyncManager(self.__address, self.__authkey)
        self.__manager.connect()
            