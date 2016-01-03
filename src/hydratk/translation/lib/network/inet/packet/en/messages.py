# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.network.inet.packet.en.messages
   :platform: Unix
   :synopsis: English language translation for INET packet messages
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
    'htk_inet_sending_packet'      : "Sending packet, iface: '%s'",   
    'htk_inet_packet_sent'         : "Packet sent", 
    'htk_inet_sending_recv_packet' : "Sending and receiving packets, iface: '%s', retry: '%s', timeout: '%s'",   
    'htk_inet_packet_sent'         : "Packets sent and received",
    'htk_inet_ping'                : "Ping to destination: '%s', protocol: '%s', port: '%s'",
    'htk_inet_ping_ok'             : "Ping was successful",
    'htk_inet_ping_nok'            : "Ping was not successful",
    'htk_inet_traceroute'          : "Traceroute to destination: '%s', protocol: '%s', port: '%s', max_hops: '%s'",
    'htk_inet_traceroute_ok'       : "Traceroute was successful",
    'htk_inet_traceroute_nok'      : "Traceroute was not successful",
    'htk_inet_sniffer_started'     : "Starting sniffer output: '%s', iface: '%s', filter: '%s', timeout: '%s'",
    'htk_inet_sniffer_stopped'     : "Sniffed was stopped"      
}
