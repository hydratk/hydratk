# -*- coding: utf-8 -*-
"""Simplified core debugger functionality 

.. module:: lib.debugging.simpledebug
   :platform: Unix
   :synopsis: Simplified core debugger functionality 
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

from hydratk.core import const
from hydratk.core import event


def dmsg(msg, level=1, channel=const.DEBUG_CHANNEL):
    """Function writes debug message

    Args:   
       msg (str): message
       level (int): debug level
       channel (list): debug channel

    Returns:
       void

    """

    from hydratk.core.masterhead import htk
    if htk.debug is True:
        if htk.debug_level is not None and level > htk.debug_level:                 
            return False
        if len(htk.debug_channel) > 0 and htk.match_channel(channel) == False:        
            return False
        
        if type(msg).__name__ == 'tuple' and len(msg) > 0:
            msg_key = msg[0]
            msg_params = ()
            if len(msg) > 1:
                msg_params = msg[1:]
                msg = htk._trn.msg(msg_key, *msg_params)
            else:
                msg = htk._trn.msg(msg_key)

        htk.fire_event(event.Event('htk_on_debug_info', msg, htk.fromhere(2), level, channel))


def wmsg(msg):
    """Function writes warning message

    Args:   
       msg (str): message

    Returns:
       void

    """

    from hydratk.core.masterhead import MasterHead
    _mh = MasterHead.get_head()
    _mh.fire_event(event.Event('htk_on_warning', msg, _mh.fromhere(2)))
