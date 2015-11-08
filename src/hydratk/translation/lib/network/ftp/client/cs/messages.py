# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.network.ftp.client.cs.messages
   :platform: Unix
   :synopsis: Czech language translation for FTP client messages
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
    'htk_ftp_unknown_protocol' : "Neznámý protokol: '%s'",
    'htk_ftp_connecting'       : "Připojuji se na server: '%s'",
    'htk_ftp_connected'        : "Spojení se serverem bylo úspěšné",
    'htk_ftp_unknown_method'   : "Neznámá metoda pro protokol: '%s'",
    'htk_ftp_disconnected'     : "Spojení se serverem bylo ukončeno",
    'htk_ftp_list_dir'         : "Vypisuji obsah adresáře: '%s'",
    'htk_ftp_change_dir'       : "Měním pracovní adresář: '%s'",
    'htk_ftp_cur_dir'          : "Pracovní adresář: '%s'",
    'htk_ftp_downloading_file' : "Stahuji soubor: '%s'",
    'htk_ftp_unknown_dir'      : "Neznámý adresář: '%s'",
    'htk_ftp_file_downloaded'  : "Stahování souboru dokončeno",
    'htk_ftp_uploading_file'   : "Nahrávám soubor: '%s'",
    'htk_ftp_unknown_file'     : "Neznámý soubor: '%s'",
    'htk_ftp_file_uploaded'    : "Nahrávání souboru dokončeno",  
    'htk_ftp_deleting_file'    : "Mažu soubor: '%s'",
    'htp_ftp_file_deleted'     : "Soubor smazán",
    'htk_ftp_making_dir'       : "Vytvářím adresář: '%s'",
    'htk_ftp_dir_made'         : "Adresář vytvořen",
    'htk_ftp_removing_dir'     : "Mažu adresář: '%s'",
    'htk_ftp_dir_removed'      : "Adresář smazán"  
}