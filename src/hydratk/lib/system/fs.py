# -*- coding: utf-8 -*-
"""Module for operation with file system

.. module:: lib.system.fs
   :platform: Unix
   :synopsis: Module for operation with file system
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import os
import uuid
import time


def rmkdir(path):
    """Method creates directory

    Args:
       path (str): directory path

    Returns:
       bool: result

    Raises:
       exeception: Exception

    """

    result = False
    if path != '' and not os.path.exists(path):
        try:
            os.makedirs(path)
            return True
        except OSError as ex:
            raise ex
    return result


def file_get_contents(filename, mode='r', acquire_lock=False, wait_lock_timeout=5):
    """Methods reads file content

    Args:
       filename (str): filename including path
       mode (str): file mode
       acquire_lock (bool): request file lock
       wait_lock_timeout (int): time wait for lock to be obtained

    Returns:
       str: content

    """

    with open(filename, mode) as f:
        return f.read()


def file_put_contents(filename, data, mode='w'):
    """Methods writes content to file

    Args:
       filename (str): filename including path
       data (str): content
       mode (str): file mode
                             
    Returns:
       void

    """

    f = open(filename, mode)        
    f.write(data)
    f.close()
