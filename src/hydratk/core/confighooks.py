# -*- coding: utf-8 -*-
"""HydraTK Macro parser config hooks

.. module:: core.confighooks
   :platform: Unix
   :synopsis: HydraTK core module
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

config_var_regexp = { 
                      'config_var_struct' : r'\$\(([a-z,A-Z,0-9,\-,_,\.].*)\.([a-z,A-Z,0-9,\-,_,\.].*)\.([a-z,A-Z,0-9,\-,_,\.].*)\)'
                    }

class ConfigHooks:
    pass
    #TODO create usefull hooks
