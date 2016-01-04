# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.network.rest.client.en.messages
   :platform: Unix
   :synopsis: English language translation for REST client messages
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
    'htk_rest_request'  : ["Sending request na server: '{0}', user:'{1}', passw:'', method:'{2}', " + \
                          "headers: '{3}', body: '{4}', params:'{5}'"],
    'htk_rest_response' : ["Received response from server: '{0}'"] 
}
