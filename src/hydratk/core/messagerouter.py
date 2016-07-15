# -*- coding: utf-8 -*-
"""HydraTK message router

.. module:: core.messagerouter
   :platform: Unix
   :synopsis: HydraTK message router
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import os
from hydratk.core import const, message
from hydratk.lib.exceptions.inputerror import InputError
import zmq

ERROR_ROUTER_ID_EXISTS               = 1  # An existing router id
ERROR_SERVICE_ID_EXISTS              = 10 # An existing service id 
ERROR_SERVICE_INVALID_TRANSPORT_TYPE = 11 # Invalid transport type
SERVICE_TRANSPORT_TYPE_ZMQ_IPC       = 1  # ZeroMQ IPC
SERVICE_TRANSPORT_TYPE_ZMQ_TCP       = 2  # ZeroMQ TCP

MESSAGE_QUEUE_ACTION_BIND            = 1
MESSAGE_QUEUE_ACTION_CONNECT         = 2 

class MessageRouter():
    """Class MessageRoute
    """
   
    _service_list = {}    
    _id           = ''
    _trn          = None
 
    def __init__(self, id):
        """Class constructor
        
        Called when object is initialized
        
        Args:
           id (str): message router id
        
        Returns:            
           void
           
        Raises:
           error: TypeError
           
        """        
 
        from hydratk.core.masterhead import MasterHead
        self._id = id
        self._trn = MasterHead.get_head().get_translator()    
            
    def register_service(self, id, transport_type, options):
        """Method will add router service identificator using specified parameters
        
        Args:
           id (str): service identifier
           transport_type (int): supported transport type, currently only IPC and TCP is supported
           options (dict): transport_type supported options
        
        Returns:            
           bool: True
           
        Raises:
           error: InputError
           
        """
                
        if id != '' and id not in self._service_list.keys():
            service = {}
            if (transport_type in (SERVICE_TRANSPORT_TYPE_ZMQ_IPC, SERVICE_TRANSPORT_TYPE_ZMQ_TCP)):
                service['transport_type'] = transport_type
                service['active'] = False                
                service['options'] = options 
                self._service_list[id] = service
            else:
                raise InputError(ERROR_SERVICE_INVALID_TRANSPORT_TYPE, id, self._trn.msg('htk_mrouter_sid_invalid_tt', transport_type))            
                                             
        else:
            raise InputError(ERROR_SERVICE_ID_EXISTS, id, self._trn.msg('htk_mrouter_sid_exists', id))
           
        return True
        
    def get_queue(self, service_id, action, options = {}):
        """Method will return a new instance of queue object for specified service_id
        
        Args:
           service_id (str): service identifier
           options (dict): queue type optional settings
        
        Returns:            
           obj: socket

        """
                
        from hydratk.lib.debugging.simpledebug import dmsg
        q = False
        if service_id != '' and service_id in self._service_list:
            service = self._service_list[service_id]
            service_options = service['options']                                      
                        
            addr_prefix = 'ipc://' if (service['transport_type'] == SERVICE_TRANSPORT_TYPE_ZMQ_IPC) else 'tcp://'            
            context = zmq.Context()            
            q = context.socket(options['socket_type'])
            
            if (action == MESSAGE_QUEUE_ACTION_BIND):
                if (service['active'] == False):
                    if (service['transport_type'] == SERVICE_TRANSPORT_TYPE_ZMQ_IPC):                        
                        file_path = os.path.dirname(service_options['address'])
                        if (not os.path.exists(file_path)):                                                
                            os.makedirs(file_path)
                            ''' TODO set optimal default directory permission '''
                    dmsg("Binding to message queue {0} : socket type {1}".format(addr_prefix + service_options['address'],options['socket_type']))          
                    q.bind(addr_prefix + service_options['address'])
                    service['active'] = True
                    self._service_list[service_id] = service
                else:
                    raise Exception("Service queue is active use MESSAGE_QUEUE_ACTION_CONNECT instead")
            elif (action == MESSAGE_QUEUE_ACTION_CONNECT):
                q.connect(addr_prefix + service_options['address'])
                dmsg("Connecting to message queue {0} : socket type {1}".format(addr_prefix + service_options['address'],options['socket_type']))
                
             
            else:
                pass 
            ''' TODO invalid action '''
                                                     
        return q
    
    def get_service_address(self, service_id):
        """Method gets service address
        
        Args:
           service_id (str): service identifier
        
        Returns:            
           str: address

        """
                
        service = self._service_list[service_id]
        service_options = service['options']
        return service_options['address']  