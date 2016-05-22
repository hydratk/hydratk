# -*- coding: utf-8 -*-
"""HydraTK default events definition

.. module:: core.events
   :platform: Unix
   :synopsis: HydraTK default events definition
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

event = {  
  'htk_on_stop'                 : 'hydratk.core',  '''htk_on_stop'''
  'htk_on_help'                 : 'hydratk.core',  '''htk_on_help: help_commands'''
  'htk_on_cprint'               : 'hydratk.core',  '''htk_on_cprint: message'''
  'htk_on_debug_info'           : 'hydratk.core',  '''htk_on_debug_info: debug_level, channel, msg, location '''
  'htk_on_error'                : 'hydratk.core',  '''htk_on_error: msg, location '''
  'htk_on_warning'              : 'hydratk.core',  '''htk_on_warning: msg, location '''
  'htk_on_uncaught_exception'   : 'hydratk.core',  '''htk_on_exception: msg, location ''' 
  'htk_on_extension_error'      : 'hydratk.core',  '''htk_on_extension_error: msg, location '''
  'htk_on_extension_warning'    : 'hydratk.core',  '''htk_on_extension_warning: msg, location '''
  'htk_on_cmd_options'          : 'hydratk.core',  '''htk_on_got_cmd_options'''
  'htk_on_signal'               : 'hydratk.core',  '''htk_on_signal: sig_num'''
  'htk_on_sigterm'              : 'hydratk.core',  '''htk_on_sigterm'''
  'htk_on_sigint'               : 'hydratk.core',  '''htk_on_sigint'''
  'htk_on_sigpipe'              : 'hydratk.core',  '''htk_on_sigpipe'''
  'htk_on_cmsg_recv'            : 'hydratk.core',  '''htk_on_cmsg_recv: msg'''
  'htk_on_wmsg_recv'            : 'hydratk.core',  '''htk_on_wmsg_recv: msg'''
  'htk_on_privmsg_recv'         : 'hydratk.core',   '''htk_on_privmsg_recv: msg'''
  'htk_on_cobserver_ctx_switch' : 'hydratk.core',
  'htk_on_cobserver_init'       : 'hydratk.core',
  'htk_on_cworker_init'         : 'hydratk.core'
   
}