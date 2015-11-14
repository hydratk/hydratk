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
    'htk_rest_request'  : "Sending request na server: '%s', user:'%s', passw:'%s', method:'%s', " + \
                          "headers: '%s', body: '%s', params:'%s'",
    'htk_rest_response' : "Received response from server: '%s'" 
}
