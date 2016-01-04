# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.network.inet.client.cs.messages
   :platform: Unix
   :synopsis: Czech language translation for INET packet messages
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
    'htk_inet_sending_packet'      : "Odesílám packet, iface: '%s'",   
    'htk_inet_packet_sent'         : "Packet odeslán", 
    'htk_inet_sending_recv_packet' : "Odesílám a příjímám packety, iface: '%s', retry: '%s', timeout: '%s'",   
    'htk_inet_packet_sent'         : "Packety odeslány a přijaty",
    'htk_inet_ping'                : "Ping destination: '%s', protocol: '%s', port: '%s'",
    'htk_inet_ping_ok'             : "Ping byl úspěšný",
    'htk_inet_ping_nok'            : "Ping byl neúspěšný",
    'htk_inet_traceroute'          : "Traceroute destination: '%s', protocol: '%s', port: '%s', max_hops: '%s'",
    'htk_inet_traceroute_ok'       : "Traceroute byl úspěšný",
    'htk_inet_traceroute_nok'      : "Traceroute byl neúspěšný",
    'htk_inet_sniffer_started'     : "Spouštím sniffer output: '%s', iface: '%s', filter: '%s', timeout: '%s'",
    'htk_inet_sniffer_stopped'     : "Sniffer byl zastaven"            
}