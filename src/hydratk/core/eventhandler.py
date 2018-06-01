# -*- coding: utf-8 -*-
"""HydraTK core event handling implementation class

.. module:: core.eventhandler
   :platform: Unix
   :synopsis: HydraTK core event handling implementation class
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

from hydratk.core import hsignal


class EventHandler(object):
    """Class EventHandler
    """

    def _ec_check_co_privmsg(self, oevent):
        """Method handles observer message event

        Args:
           oevent (obj): event object

        Returns:
           void

        """

        self._check_co_privmsg()

    def _ec_check_cw_privmsg(self, oevent):
        """Method handles worker message event

        Args:
           oevent (obj): event object

        Returns:
           void

        """

        self._check_cw_privmsg()

    def _ec_stop_app(self, oevent, *args):
        """Method handles stop event

        Args:
           oevent (obj): event object
           args (list): arguments

        Returns:
           void

        """

        self._stop_app(*args)

    def _eh_htk_on_got_cmd_options(self, oevent):
        """Method handles command options event

        Args:
           oevent (obj): event object

        Returns:
           void

        """

        self.apply_command_options()

    def _eh_htk_on_debug_info(self, oevent, *args):
        """Method handles debug

        Args:
           oevent (obj): event object
           args (list): arguments

        Returns:
           void

        """

        self.dout(*args)

    def _eh_htk_on_warning(self, oevent, *args):
        """Method handles warning event

        Args:
           oevent (obj): event object
           args (list): arguments

        Returns:
           void

        """

        if int(self.cfg['System']['Warnings']['enabled']) == 1:
            self.wout(*args)

    def _eh_htk_on_extension_warning(self, oevent, *args):
        """Method handles extension warning event

        Args:
           oevent (obj): event object
           args (list): arguments

        Returns:
           void

        """

        self.wout(*args)

    def _eh_htk_on_error(self, oevent, *args):
        """Method handles error event

        Args:
           oevent (obj): event object
           args (list): arguments

        Returns:
           void

        """



    def _eh_htk_on_exception(self, oevent, *args):
        """Method handles exception event

        Args:
           oevent (obj): event object
           args (list): arguments

        Returns:
           void

        """

        self.exout(*args)

    def _eh_htk_on_extension_error(self, oevent, *args):
        """Method handles extension error event

        Args:
           oevent (obj): event object
           args (list): arguments

        Returns:
           void

        """

        self.errout(*args)

    def _eh_htk_on_cprint(self, oevent, *args):
        """Method handles print event

        Args:
           oevent (obj): event object
           args (list): arguments

        Returns:
           void

        """

        self.spout(*args)

    def _ec_sig_handler(self, oevent, signum):
        """Method handles signal event

        Args:
           oevent (obj): event object
           signum (int): signal number

        Returns:
           void

        """

        signal = hsignal.sigint2string[
            signum] if signum in hsignal.sigint2string else signum
        self.demsg('htk_on_debug_info', self._trn.msg(
            'htk_sig_recv', signal), self.fromhere())
