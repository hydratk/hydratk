'''
Created on 31.7.2011

@author: CzadernaP
'''
import os
from hydratk.core import const, message
from hydratk.lib.exceptions.inputerror import InputError
import zmq

'''An existing router id'''
ERROR_ROUTER_ID_EXISTS               = 1 
'''An existing service id'''  
ERROR_SERVICE_ID_EXISTS              = 10
'''Invalid transport type'''  
ERROR_SERVICE_INVALID_TRANSPORT_TYPE = 11  
'''ZeroMQ IPC'''
SERVICE_TRANSPORT_TYPE_ZMQ_IPC       = 1
'''ZeroMQ TCP''' 
SERVICE_TRANSPORT_TYPE_ZMQ_TCP       = 2 

MESSAGE_QUEUE_ACTION_BIND            = 1
MESSAGE_QUEUE_ACTION_CONNECT         = 2 

class MessageRouter():
    '''
    classdocs
    '''
   
    _service_list = {}    
    _id           = ''
    _trn          = None
 
    '''
    Create router using specified parameters
    
    @param id: router identificator
    @param config: global config object  
    '''
    def __init__(self, id):
        '''
        Constructor
        '''
        from hydratk.core.masterhead import MasterHead
        self._id = id
        self._trn = MasterHead.get_head().get_translator()    
            
    '''
    Method will add router service identificator using specified parameters
    
    @param id: service identificator
    @param transport_type: supported transport type, currently only IPC and TCP is supported
    @param options: transport_type supported options
                    ZMQ supported options:
                      socket_type = 
    '''    
    def register_service(self, id, transport_type, options):
        if id != '' and id not in self._service_list.values():
            service = {}
            if (transport_type in (SERVICE_TRANSPORT_TYPE_ZMQ_IPC, SERVICE_TRANSPORT_TYPE_ZMQ_TCP)):
                service['transport_type'] = transport_type
                service['active'] = False                
                service['options'] = options 
                self._service_list[id] = service
            else:
                print('transport type: '+SERVICE_TRANSPORT_TYPE_ZMQ_IPC+ "\n")
                raise InputError(ERROR_SERVICE_INVALID_TRANSPORT_TYPE, id, self._trn.msg('htk_mrouter_sid_invalid_tt', transport_type))            
                                             
        else:
            raise InputError(ERROR_SERVICE_ID_EXISTS, id, self._trn.msg('htk_mrouter_sid_exists', id))
           
        return True
        
    
    '''
    Method will return a new instance of queue object for specified service_id
    
    @param service_id: service identificator
    @param options: queue type optional settings, e.g. zmq socket_type can be passed this way
    @author: Petr Czaderna
    @version: 0.1.0      
    ''' 
    def get_queue(self, service_id, action, options = {}):
        
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
                    q.bind(addr_prefix + service_options['address'])
                    service['active'] = True
                    self._service_list[service_id] = service
                else:
                    pass
            elif (action == MESSAGE_QUEUE_ACTION_CONNECT):
                q.connect(addr_prefix + service_options['address'])
             
            else:
                pass 
            ''' TODO invalid action '''
                                                     
        return q
    
    def get_service_address(self, service_id):
        service = self._service_list[service_id]
        service_options = service['options']
        return service_options['address']  