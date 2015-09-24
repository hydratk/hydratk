#!/usr/bin/env pypy

"""This code is a part of Hydra framework

.. module:: hydra
   :platform: Unix
   :synopsis: For sandbox testing.
.. moduleauthor:: Petr Czaderna <pc@headz.cz>

"""

import sys;
from hydratk.core import bootstrapper

PYTHON_MAJOR_VERSION = sys.version_info[0];
if PYTHON_MAJOR_VERSION == 2:
    reload(sys);
    sys.setdefaultencoding('UTF8');
    

               
if __name__ == '__main__':
    bootstrapper.run_app();