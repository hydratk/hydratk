# -*- coding: utf-8 -*-
"""HydraTK Macro parser config hooks

.. module:: core.confighooks
   :platform: Unix
   :synopsis: HydraTK core module
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

from xtermcolor import colorize
from hydratk.lib.system import config
from datetime import datetime

config_var_regexp = {                       
                      'config_var_struct' : r'\$\(([^\x28-\x29]+)\.([^\x28-\x29]+)\.([^\x28-\x29]+)\)'
                    }
    
class ConfigHooks:

    @staticmethod
    def colorize(text,color):                
        rgb_color = color.replace('#', '')
        return colorize(text, int(rgb_color, 16))



hook_list = {
    'date'        : datetime.now().strftime,    
   'colorize'     : ConfigHooks.colorize,
   'htk_root_dir' : config.HTK_ROOT_DIR,
   'htk_etc_dir'  : config.HTK_ETC_DIR,
   'htk_var_dir'  : config.HTK_VAR_DIR,
   'htk_log_dir'  : config.HTK_LOG_DIR,
   'htk_usr_dir'  : config.HTK_USR_DIR       
}