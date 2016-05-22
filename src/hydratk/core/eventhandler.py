# -*- coding: utf-8 -*-
"""HydraTK core event handling implementation class

.. module:: core.eventhandler
   :platform: Unix
   :synopsis: HydraTK core event handling implementation class
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

from hydratk.core import hsignal

class EventHandler:
    """Class EventHandler
    """
    
    def _ec_check_co_privmsg(self, oevent):
        self._check_co_privmsg()    

    def _ec_check_cw_privmsg(self, oevent):
        self._check_cw_privmsg() 
        
    def _ec_stop_app(self, oevent, *args):
        self._stop_app(*args)

    def _eh_htk_on_got_cmd_options(self, oevent):
        self.apply_command_options() 
    
    def _eh_htk_on_debug_info(self, oevent, *args):
        self.dout(*args)       
    
    def _eh_htk_on_warning(self, oevent, *args):
        if int(self.cfg['System']['Warnings']['enabled']) == 1:
            self.wout(*args)
    
    def _eh_htk_on_extension_warning(self, oevent, *args):
        self.wout(*args) 
        
    def _eh_htk_on_error(self, oevent, *args):
        self.errout(*args)
        
    def _eh_htk_on_exception(self, oevent, *args):
        self.exout(*args)
    
    def _eh_htk_on_extension_error(self, oevent, *args):
        self.errout(*args)
    
    def _eh_htk_on_cprint(self, oevent, *args):        
        self.spout(*args)
                
    def _ec_sig_handler(self, oevent, signum):
        signal = hsignal.sigint2string[signum] if signum in hsignal.sigint2string else signum 
        self.dmsg('htk_on_debug_info', self._trn.msg('htk_sig_recv', signal), self.fromhere())    
