# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit

.. module:: lib.data.shmm
   :platform: Unix
   :synopsis: Module with shared memory tools and managers for parallel data processing and synchronization
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
try:
    import cPickle as pickle
except:
    import pickle  

def get_ctype_char_array(int_keys, lock = True):
    from multiprocessing  import Array
    from ctypes import c_char_p
    return Array(c_char_p, int_keys, lock = lock)


    
    
