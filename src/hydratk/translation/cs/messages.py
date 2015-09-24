# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.cs.messages
   :platform: Unix
   :synopsis: Czech language translation for global messages
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

language = {
  'name' : 'Čeština',
  'ISO-639-1' : 'cs'
}

from hydratk.core import const;

HIGHLIGHT_START = chr(27)+chr(91)+"1m";
HIGHLIGHT_US    = chr(27)+chr(91)+"4m";
HIGHLIGHT_END   = chr(27)+chr(91)+"0m";

msg = {      
    'htk_print_short_desc' : HIGHLIGHT_START + const.APP_NAME +" v"+ const.APP_VERSION + const.APP_REVISION + HIGHLIGHT_END + " pro Unixové operační systémy",
    'htk_print_cp_string'  : "(c) " + const.APP_AUTHORS + " " + "(" + const.APP_DEVEL_YEAR + ")",
    'htk_unknown_command'  : "Neznámý příkaz: " + HIGHLIGHT_START +"%s" + HIGHLIGHT_END +", pro nápovědu zadej příkaz " + HIGHLIGHT_START + "help" + HIGHLIGHT_END,
    'htk_help_syntax'      : "Použití: " + HIGHLIGHT_START + "%s [možnosti..] příkaz" + HIGHLIGHT_END,
    'htk_help_commands'    : HIGHLIGHT_US + 'Příkazy:' + HIGHLIGHT_END,
    'htk_help_command'     : HIGHLIGHT_US + 'Příkaz:' + HIGHLIGHT_END,
    'htk_help_options'     : HIGHLIGHT_US + 'Možnosti:' + HIGHLIGHT_END,
    'htk_help_option'      : HIGHLIGHT_US + 'Možnost:' + HIGHLIGHT_END,
    'htk_help_glob_options'  : HIGHLIGHT_US + 'Globální Možnosti:' + HIGHLIGHT_END,
    'htk_invalid_cmd'        : "Špatný příkaz: %s",
    'htk_undetected_cmd'     : "Vstupní příkaz nebyl rozpoznán",
    'htk_app_start'          : "Startuji aplikaci",
    'htk_app_stop'           : "Zastavuji aplikaci",
    'htk_app_exit'           : "Ukončuji aplikaci",
    'htk_conf_not_exists'    : "Konfigurační soubor '%s' neexistuje",
    'htk_opt_set'            : "Možnost '%s' nastavena na: '%s'",
    'htk_unrecognized_opt'   : "Možnost '%s' nebyla rozpoznána",
    'htk_opt_ignore'         : "Nastavení možnosti '%s' bylo ignorováno, protože má nesprávnou hodnotu: '%s'",
    'htk_conf_opt_missing'   : "Chyba konfigurace, sekce: '%s', možnost: '%s' není definována",
    'htk_conf_opt_val_err'   : "Chyba konfigurace, sekce: '%s', možnost: '%s' obsahuje špatnou hodnotu",
    'htk_debug_enabled'      : "Spouštím aplikaci v režimu ladění programu",
    'htk_lang_set'           : "Jazyk nastaven na '%s'", 
    'htk_invalid_lang_set'   : "Jazyk '%s' není podporován",
    'htk_debug_level_set'    : "Úroveň režimu ladění programu nastavena na %d",
    'htk_msg_router_id_set'  : "Id pro hlavní router zpráv nastaveno na '%s'",
    'htk_msg_router_init_ok' : "Router zpráv '%s' úspěšně inicializován",
    'htk_core_msg_service_add_ok' : "Fronta zpráv jádra '%s' úspěšně zaregistrována",
    'htk_core_msgq_init_ok'       : "Fronta zpráv jádra '%s' úspěšně inicializována",
    'htk_core_msgq_connect_ok'    : "Fronta zpráv jádra '%s' úspěšně připojena", 
    'htk_load_int_ext'            : "Nahrávám interní rozšíření: '%s'",
    'htk_load_int_ext_success'    : "Interní rozšíření: '%s' úspěšně nahráno",
    'htk_load_ext_ext'            : "Nahrávám externí rozšíření: '%s'",
    'htk_load_ext_ext_success'    : "Externi rozšíření: '%s' úspěšně nahráno",
    'htk_load_ext_msg'            : "Načítám zprávy rozšíření pro jazyk %s, package '%s'",
    'htk_load_ext_msg_success'    : "Zprávy rozšíření pro jazyk %s, úspěšně načteny",
    'htk_load_ext_msg_failed'     : "Nepodařilo se načíst zprávy rozšíření pro jazyk %s, důvod: %s",
    'htk_load_ext_help'           : "Načítám napovědu rozšíření pro jazyk %s, package '%s'",
    'htk_load_ext_help_failed'    : "Nepodařilo se načíst nápovědu rozšíření pro jazyk %s, důvod: %s",
    'htk_load_global_msg'         : "Načítám globální zprávy pro jazyk %s, package '%s'",
    'htk_load_global_msg_success' : "Globální zprávy pro jazyk %s, načteny úspěšně",
    'htk_load_global_msg_failed'  : "Nepodařilo se načíst globální zprávy pro jazyk %s, důvod: %s",
    'htk_load_global_help'        : "Načítám globální nápovědu pro jazyk %s, package '%s'",
    'htk_load_global_help_success' : "Globální nápověda pro jazyk %s, načtena úspěšně",
    'htk_load_global_help_failed'  : "Nepodařilo se načíst globální nápovědu %s, důvod: %s",
    'htk_ext_ext_dir_not_exists'  : "Adresář externích rozšíření '%s' je definován v konfiguraci, ale neexistuje",
    'htk_fin_load_int_ext'        : "Dokončeno nahrávání interních rozšíření",
    'htk_fin_load_ext_ext'        : "Dokončeno nahrávání externích rozšíření",
    'htk_fail_load_int_ext'       : "Nahravani interniho rozsireni: '%s' skoncilo s chybou: %s",
    'htk_fail_init_int_ext'       : "Inicializace interniho rozsireni: '%s' skoncila s chybou: %s", 
    'htk_fail_load_ext_ext'       : "Nahravani externiho rozsireni: '%s' skoncilo s chybou: %s",
    'htk_fail_to_create_obj'      : "Nepodarilo se vytvorit object",
    'htk_cthread_init'            : "Inicializuji vlakno jadra id: %s",
    'htk_cworker_init'            : "Zacinam pracovat",
    'htk_cworker_term'            : "Ukoncuji praci",
    'htk_cthread_destroy'         : "Ukoncuji vlakno jadra id: %s",
    'htk_cthread_sleep'           : "Usinam...",
    'htk_cthread_awake'           : "Probuzen",
    'htk_core_workers_num_set'    : "Pocet workeru jadra nastaven na: %s",
    'htk_pid_file_set'            : "Ukladam PID %s do souboru: %s",
    'htk_pid_file_delete'         : "Smazan PID soubor: %s",    
    'htk_app_not_running'         : "Aplikace neni spustena, nebyl nalezen PID",
    'htk_app_stopped'             : "Aplikace byla ukoncena", 
    'htk_app_not_running_except'  : "Aplikace neni spustena, behem pozadavku na ukonceni vznikla vyjimka",
    'htk_app_running_with_pid'    : "Aplikace je spustena, hlavni PID je %s",
    'htk_app_not_running_with_pid' : "Aplikace neni spustena, byl nalezen PID %s predchoziho spusteni",
    'htk_app_stop_request_soft'    : "Posilam pozadavek na ukonceni aplikace (soft)",
    'htk_int_msgq_init'            : "Inicializuji vnitrni globalni frontu zprav, qid: %s",
    'htk_oint_msgq_init'           : "Inicializuji privatni frontu zprav dozorce",
    'htk_observer_init'            : "Zacinam dohlizet",
    'htk_observer_term'            : "Ukoncuji dozor",
    'htk_observer_sleep'           : "Usinam...",
    'htk_observer_awake'           : "Probuzen",
    'htk_sig_recv'                 : "Zachycen signal: %s",
    'htk_htk_reg_int_srv_msgq'         : "Registruji vnitrni frontu zprav id: %s pro sluzbu: %s",
    'htk_app_service_reg_ok'       : "Registrovana aplikacni sluzba %s - %s",
    'htk_app_service_start_ok'     : "Aplikacni sluzba %s byla uspesne spustena",
    'htk_app_service_stop'         : "Zastavuji aplikacni sluzbu %s (soft)",
    'htk_app_service_stop_failed'  : "Nepodrarilo se ukoncit aplikacni sluzbu %s ve stanovenem case",
    'htk_app_service_stop_hard'    : "Zastavuji aplikacni sluzbu %s (hard)",
    'htk_app_service_inactive_skip' : "Vynechavam neaktivni aplikacni sluzbu %s",
    'htk_app_service_already_running' : "Aplikacni sluzba %s je jiz spustena" 
}