# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.network.jms.client.en.messages
   :platform: Unix
   :synopsis: English language translation for JMS client messages
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

language = {
  'name' : 'English',
  'ISO-639-1' : 'en'
}

from hydratk.core import const

HIGHLIGHT_START = chr(27)+chr(91)+"1m"
HIGHLIGHT_US    = chr(27)+chr(91)+"4m"
HIGHLIGHT_END   = chr(27)+chr(91)+"0m"

msg = {
    'htk_jms_connecting'    : ["Connecting to JMS provider with params: '{0}'"],
    'htk_jms_connected'     : ["Connected to JMS provider"],
    'htk_jms_disconnecting' : ["Disconnecting from JMS provider"],
    'htk_jms_disconnected'  : ["Disconnected from JMS provider"],
    'htk_jms_sending_msg'   : ["Sending message with params: '{0}'"],
    'htk_jms_msg_sent'      : ["Message sent"] 
}
