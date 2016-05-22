# -*- coding: utf-8 -*-
"""A Python native multiprocessing Managed queue driver

.. module:: lib.messaging.native.queue
   :platform: Unix
   :synopsis: A Python native multiprocessing Managed queue driver
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

from pyx.messaging import queue
from multiprocessing import Queue
from multiprocessing.managers import SyncManager

class Queue():
    """Class Queue
    """
    
    __type    = None
    __manager = None
    __address = None
    __authkey = None
    
    
    def __init__(self, qtype, address, authkey=''):
        """Class constructor
        
        Called when object is initialized

        Args:
           qtype (int): queue type, server|client
           address (str): queue address
           authkey (str): authentication key
           
        Raises:
           error: ValueError
    
        """
                
        if type in (queue.QUEUE_TYPE_SERVER,queue.QUEUE_TYPE_CLIENT):
            self.__type = qtype
        else: raise ValueError('Invalid Queue type')
        
        ''' Checking for address format AF_INET '''
        if address.find(':') > 0: 
            address = address.split(':')
                    
        self.__address = address
        self.__authkey = authkey 
        
    
    def create(self):
        """Methods creates queue server

        Args:
           none

        Returns:
           void
    
        Raises:
           error: ValueError
    
        """
                
        if self.__type != queue.QUEUE_TYPE_SERVER:
            raise ValueError('This operation cannot be done on this queue type')
        
        q = Queue()
        SyncManager.register('get_queue', callable = lambda: q)
        self.__manager = SyncManager(self.__address, self.__authkey)        
        self.__manager.start()
            
    def destroy(self):
        """Methods destroys queue

        Args:
           none

        Returns:
           void
    
        """
                
        self.__manager.shutdown()
        
    def connect(self):
        """Methods connects to queue

        Args:
           none

        Returns:
           void
           
        Raises:
           error: ValueError
    
        """
                
        if self.__type != queue.QUEUE_TYPE_CLIENT:
            raise ValueError('This operation cannot be done on this queue type')
        
        q = Queue()
        SyncManager.register('get_queue', callable = lambda: q)
        self.__manager = SyncManager(self.__address, self.__authkey)
        self.__manager.connect()
            