'''
Created on 24.10.2009

@author: CzadernaP
'''
from collections import defaultdict;

class MultiDict(defaultdict):
    def __init__(self):
        defaultdict.__init__(self, MultiDict);
    def __repr__(self):
        return dict.__repr__(self);