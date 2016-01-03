# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.network.dbi.client.en.messages
   :platform: Unix
   :synopsis: English language translation for DB client messages
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
    'htk_dbi_unknown_type'       : "Unknown procedure type: '%s'",
    'htk_dbi_connecting'         : "Connecting to server: '%s'",
    'htk_dbi_connected'          : "Connected successfully",
    'htk_dbi_connecting_error'   : "Error occured during connecting to server",
    'htk_dbi_disconnecting'      : "Disconnecting from server",
    'htk_dbi_disconnected'       : "Disconnected from server",
    'htk_dbi_disconnecting_error': "Error occured during disconnecting from server",
    'htk_dbi_executing_query'    : "Executing query: '%s'",
    'htk_dbi_query_executed'     : "Query executed",
    'htk_dbi_query_error'        : "Error occured during query execution",
    'htk_dbi_calling_proc'       : "Calling procedure: '%s'",
    'htk_dbi_proc_called'        : "Procedure called" 
}
