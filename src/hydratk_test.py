# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit

.. module:: hydra
   :platform: Unix
   :synopsis: For sandbox testing.
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import sys
from hydratk.core import test_ootstrapper

PYTHON_MAJOR_VERSION = sys.version_info[0]
if PYTHON_MAJOR_VERSION == 2:
    reload(sys)
    sys.setdefaultencoding('UTF8')
    

               
if __name__ == '__main__':
    test_bootstrapper.run_app()