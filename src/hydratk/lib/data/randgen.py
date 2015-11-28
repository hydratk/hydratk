# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit library

.. module:: lib.data.gen
   :platform: Unix
   :synopsis: Module for random data generation
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

import time;
import random;

def gen_systimestamp():
    
    return time.strftime('%Y-%m-%dT%H:%M:%S');

def gen_sysdate():
    
    return time.strftime('%Y-%m-%d');

def gen_message_id():
    
    return 'hydratk-{0}-{1}'.format(time.time(), gen_id(3));

def gen_id(n=10):
    
    return str(random.randint(10**(n-1), 10**n-1));