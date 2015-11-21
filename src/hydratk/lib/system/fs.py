# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit library

.. module:: lib.system.fs
   :platform: Unix
   :synopsis: Module for operation with file system
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import os

def rmkdir(path):
    result = False;
    if path != '' and not os.path.exists(path):
        try:
            os.makedirs(path)
            return True
        except Exception as ex:
            raise ex;
    return result

def file_get_contents(filename):
    with open(filename) as f:
        return f.read()

def file_put_contents(filename, data):    
    f = open(filename, 'w')
    f.write(data)
    f.close()