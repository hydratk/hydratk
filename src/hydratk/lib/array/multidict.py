# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit library

.. module:: lib.array.multidict
   :platform: Unix
   :synopsis: Multi-level dictionary
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

from collections import defaultdict

class MultiDict(defaultdict):
    def __init__(self):
        defaultdict.__init__(self, MultiDict)
    def __repr__(self):
        return dict.__repr__(self)