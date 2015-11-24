# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.network.jms.client.cs.messages
   :platform: Unix
   :synopsis: Czech language translation for JMS client messages
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

language = {
  'name' : 'Čeština',
  'ISO-639-1' : 'cs'
}

from hydratk.core import const

HIGHLIGHT_START = chr(27)+chr(91)+"1m"
HIGHLIGHT_US    = chr(27)+chr(91)+"4m"
HIGHLIGHT_END   = chr(27)+chr(91)+"0m"

msg = {
    'htk_jms_connecting'    : "Připojuji se na JMS provider s parametry: '%s'",
    'htk_jms_connected'     : "Spojení s providerem bylo úspěšné",
    'htk_jms_disconnecting' : "Ukončuji spojení s providerem",
    'htk_jms_disconnected'  : "Spojení s providerem bylo ukončeno",
    'htk_jms_sending_msg'   : "Odesílám zprávu s parametry: '%s'",
    'htk_jms_msg_sent'      : "Zpráva odeslána" 
}
