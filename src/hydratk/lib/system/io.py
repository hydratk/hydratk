# -*- coding: utf-8 -*-
"""Useful module for controlled input output

.. module:: lib.system.io
   :platform: Unix
   :synopsis: Useful module for controlled input output
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
import sys
from hydratk.core.masterhead import MasterHead
from hydratk.core import const
_mh = MasterHead.get_head()

stdout_flush  = True
emulate_print = True

def cprint(data):
    """Methods sends data as debug message

    Args:
       data (str): message

    Returns:
       void
    
    """
        
    _mh.dmsg('htk_on_cprint',data)    
