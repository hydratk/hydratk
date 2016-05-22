# -*- coding: utf-8 -*-
"""Module for operation with file system

.. module:: lib.system.fs
   :platform: Unix
   :synopsis: Module for operation with file system
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import os

def rmkdir(path):
    """Method creates directory

    Args:
       path (str): directory path

    Returns:
       bool: result
       
    Raises:
       exeception: Exception
    
    """
        
    result = False;
    if path != '' and not os.path.exists(path):
        try:
            os.makedirs(path)
            return True
        except Exception as ex:
            raise ex;
    return result

def file_get_contents(filename):
    """Methods reads file content

    Args:
       filename (str): filename including path

    Returns:
       str: content
    
    """
        
    with open(filename) as f:
        return f.read()

def file_put_contents(filename, data): 
    """Methods writes content to file

    Args:
       filename (str): filename including path
       data (str): content

    Returns:
       void
    
    """
           
    f = open(filename, 'w')
    f.write(data)
    f.close()