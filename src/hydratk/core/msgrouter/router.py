# -*- coding: utf-8 -*-
"""HydraTK message router module

.. module:: core.msgrouter.router
   :platform: Unix
   :synopsis: HydraTK message router module
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

MSG_QUEUE_DRIVERS = {
    'zmq': 'hydratk.core.msgrouter.drivers.zmq',
}

class MessageRouter(object):
    """Class MessageRouter
    """
    _router_id        = 'HTKRouter'
    _msgq_driver      = None
    _msgq_driver_name = None

    def __init__(self, router_id):
        """ Class constructor"""
        if router_id not in ('', None) and type(router_id).__name__ == 'str':
            self._router_id = id
    
    
    def register_message_queue(self, driver_name, *args, **kwargs):
        """ Class constructor

        Called when object is initialized

        Args: 
           driver_name (str): available driver name
           *args (mixed): driver arguments
           **kwargs (mixed): driver arguments            

        Returns:
           MessageRouter: object on success 

        Raises:
           exception: MessageRouterException

        """
        
        if driver_name in MSG_QUEUE_DRIVERS:          
            self._q_driver_name = driver_name
            msgq_driver_mod_str = '{0}.driver'.format(MSG_QUEUE_DRIVERS[driver_name])
            msgq_driver_mod = self._import_msgq_driver(msgq_driver_mod_str)

        else:
            raise MessageRouterException('Not existing driver: {0}'.format(driver_name))

        try:
            self._msgq_driver = msgq_driver_mod.MessageQueDriver(*args,**kwargs)
                
        except Exception as e:
            print(e)

    @property
    def msgq_driver_name(self):
        """ driver_name property getter """

        return self._msgq_driver_name

    def _import_msgq_driver(self, msgq_driver):
        """Method import MessageQueDriver driver

        Args:   
           msgq_driver (str): MessageQueDriver driver

        Returns:
           obj: module   

        """

        return importlib.import_module(msgq_driver)


    def get_available_drivers(self):
        return MSG_QUEUE_DRIVERS

    def __getattr__(self, name):
        """Method gets attribute

        Args:   
           name (str): attribute name

        Returns:
           obj: attribute value

        """      

        return getattr(self._dbo_driver, name)

    def __getitem__(self, name):
        """Method gets item

        Args:   
           name (str): item name

        Returns:
           obj: item value

        """

        return getattr(self._dbo_driver, name)
    
    
class MessageRouterException(Exception):
    """Class MessageRouterException
    """

    _error_info = {}
    _code = None
    _message = None
    _code = None
    _file = None
    _line = None      