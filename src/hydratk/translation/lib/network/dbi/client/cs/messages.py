# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.network.dbi.client.cs.messages
   :platform: Unix
   :synopsis: Czech language translation for DB client messages
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
    'htk_dbi_unknown_engine'  : "Neznámý engine: '%s'",
    'htk_dbi_unknown_method'  : "Neznámá methoda pro engine: '%s'",
    'htk_dbi_unknown_type'    : "Neznámý typ procedury: '%s'",       
    'htk_dbi_connecting'      : "Připojuji se na server: '%s'",
    'htk_dbi_connected'       : "Spojení se serverem bylo úspěšné",
    'htk_dbi_disconnected'    : "Spojení se serverem bylo ukončeno",
    'htk_dbi_executing_query' : "Vykonávám dotaz: '%s'",
    'htk_dbi_query_executed'  : "Vykonávání dotazu ukončeno",
    'htk_dbi_calling_proc'    : "Volám proceduru: '%s'",
    'htk_dbi_proc_called'     : "Volání procedury ukončeno" 
}