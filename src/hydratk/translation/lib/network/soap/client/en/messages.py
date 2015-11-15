# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.network.soap.client.en.messages
   :platform: Unix
   :synopsis: English language translation for SOAP client messages
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
    'htk_soap_loading_wsdl' : "Loading WSDL from location: '%s', user: '%s', password: '%s', " + \
                              "endpoint: '%s', headers: '%s'",
    'htk_soap_wsdl_loaded'  : "WSDL loaded",
    'htk_soap_request'      : "Sending request to server, operation: '%s', body:'%s', headers:'%s'",
    'htk_soap_response'     : "Received response from server: '%s'" 
}
