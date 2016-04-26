# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit

.. module:: core.servicebus
   :platform: Unix
   :synopsis: HydraTK core services
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

class ServiceHead(object):
    
    def srv_async_cb(self, cbo): #CallBack object
        
        msg = {
               'type' : "async_fn",
               'from' : 'htk_obsrv@core.raptor',
               'to'   : 'any@core.raptor',
               'data' : {
                         'fn_id'  : cbo.fn_id,
                         'args'   : cbo.args,
                         'kwargs' : cbo.kwargs
                        }
              }
        self.send_msg(msg)  
