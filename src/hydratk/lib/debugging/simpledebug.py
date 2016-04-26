# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit library

.. module:: lib.debugging.simpledebug
   :platform: Unix
   :synopsis: Simplified core debugger functionality 
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

from hydratk.core import const

def dmsg(msg, level = 1, channel  = const.DEBUG_CHANNEL):
    from hydratk.core.masterhead import MasterHead
    _mh = MasterHead.get_head()
    if _mh.debug is True and level <= _mh.debug_level:
        if type(msg).__name__ == 'tuple' and len(msg) > 0:            
            msg_key = msg[0]
            msg_params = ()
            if len(msg) > 1:
                msg_params = msg[1:]
                msg = _mh._trn.msg(msg_key,*msg_params)
            else:
                msg = _mh._trn.msg(msg_key)
            
        _mh.dmsg('htk_on_debug_info',msg, _mh.fromhere(2), level, channel)
          
        
    
