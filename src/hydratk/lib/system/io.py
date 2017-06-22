# -*- coding: utf-8 -*-
"""Useful module for controlled input output

.. module:: lib.system.io
   :platform: Unix
   :synopsis: Useful module for controlled input output
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
import sys


stdout_flush = True
emulate_print = True


def cprint(data):
    """Methods sends data as debug message

    Args:
       data (str): message

    Returns:
       void

    """
    from hydratk.core.masterhead import MasterHead  

    _mh = MasterHead.get_head()
    _mh.dmsg('htk_on_cprint', data)


def rprint(*args):
    """Methods writes raw data to the stdio

    Args:
       *args (str): data

    Returns:
       void

    """
    
    sys.stdout.write(*args)
    sys.stdout.flush()
