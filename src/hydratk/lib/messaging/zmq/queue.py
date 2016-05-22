# -*- coding: utf-8 -*-
"""A Zeromq queue driver

.. module:: lib.messaging.zmq.queue
   :platform: Unix
   :synopsis: A Zeromq queue driver
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import zmq
from pyx.messaging import queue

class Queue(zmq):
    """Class Queue
    """
    
    __options = {}
    __type    = None
    __queue = None
    __address = None
    __authkey = None
    __socket_type = None
    
    
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
            address = 'tcp://' + address             
        else:
            address = 'ipc://' + address
                        
        self.__address = address
        self.__authkey = authkey 
        
    
    def set_option(self, option, value):
        """Methods sets queue option

        Args:
           option (str): option
           option (str): option value

        Returns:
           void
    
        """
                
        if option != '':
            self.__options[option] = value
            
    def create(self, socket_type=None):
        """Methods creates queue server

        Args:
           socket_type (str): type of socket

        Returns:
           void
    
        Raises:
           error: ValueError
    
        """        
        if self.__type != queue.QUEUE_TYPE_SERVER:
            raise ValueError('This operation cannot be done on this queue type')
        
        socket_type = socket_type if socket_type != None else self.__options['socket_type']
        context = zmq.Context()
        self.__queue = context.socket(socket_type)
        self.__queue.bind("tcp://127.0.0.1:5557")
        
            
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
        