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

from hydratk.core import const

HIGHLIGHT_START = chr(27)+chr(91)+"1m"
HIGHLIGHT_US    = chr(27)+chr(91)+"4m"
HIGHLIGHT_END   = chr(27)+chr(91)+"0m"

msg = {      
    'htk_print_short_desc'            : [HIGHLIGHT_START + const.APP_NAME +" v"+ const.APP_VERSION + const.APP_REVISION + HIGHLIGHT_END + " pro Unixové operační systémy"],
    'htk_print_cp_string'             : ["(c) " + const.APP_AUTHORS + " " + "(" + const.APP_DEVEL_YEAR + ")"],
    'htk_unknown_command'             : ["Neznámý příkaz: " + HIGHLIGHT_START +"{0}" + HIGHLIGHT_END +", pro nápovědu zadej příkaz " + HIGHLIGHT_START + "help" + HIGHLIGHT_END],
    'htk_help_syntax'                 : ["Použití: " + HIGHLIGHT_START + "{0} [možnosti..] příkaz" + HIGHLIGHT_END],
    'htk_help_commands'               : [HIGHLIGHT_US + 'Příkazy:' + HIGHLIGHT_END],
    'htk_help_command'                : [HIGHLIGHT_US + 'Příkaz:' + HIGHLIGHT_END],
    'htk_help_options'                : [HIGHLIGHT_US + 'Možnosti:' + HIGHLIGHT_END],
    'htk_help_option'                 : [HIGHLIGHT_US + 'Možnost:' + HIGHLIGHT_END],
    'htk_help_glob_options'           : [HIGHLIGHT_US + 'Globální Možnosti:' + HIGHLIGHT_END],
    'htk_help_on_help'                : ["Pro zobrazení seznamu všech dostupných příkazů a možností zadej " + HIGHLIGHT_START + "{0} help" + HIGHLIGHT_END],
    'htk_invalid_cmd'                 : ["Špatný příkaz: {0}"],
    'htk_undetected_cmd'              : ["Vstupní příkaz nebyl rozpoznán"],
    'htk_app_start'                   : ["Startuji aplikaci"],
    'htk_app_stop'                    : ["Zastavuji aplikaci"],
    'htk_app_exit'                    : ["Ukončuji aplikaci"],
    'htk_conf_not_exists'             : ["Konfigurační soubor '{0}' neexistuje"],
    'htk_opt_set'                     : ["Možnost '{0}' nastavena na: '{1}'"],
    'htk_unrecognized_opt'            : ["Možnost '{0}' nebyla rozpoznána"],
    'htk_opt_ignore'                  : ["Nastavení možnosti '{0}' bylo ignorováno, protože má nesprávnou hodnotu: '{1}'"],
    'htk_conf_opt_missing'            : ["Chyba konfigurace, sekce: '{0}', možnost: '{1}' není definována"],
    'htk_conf_opt_val_err'            : ["Chyba konfigurace, sekce: '{0}', možnost: '{1}' obsahuje špatnou hodnotu"],
    'htk_debug_enabled'               : ["Spouštím aplikaci v režimu ladění programu"],
    'htk_lang_set'                    : ["Jazyk nastaven na '{0}'"], 
    'htk_invalid_lang_set'            : ["Jazyk '{0}' není podporován"],
    'htk_run_mode_set'                : ["Režím spuštění nastaven na '{0} ({1})'"], 
    'htk_invalid_run_mode_set'        : ["Režim spuštění '{0}' není podporován"],    
    'htk_debug_level_set'             : ["Úroveň režimu ladění programu nastavena na {0}"],
    'htk_msg_router_id_set'           : ["Id pro hlavní router zpráv nastaveno na '{0}'"],
    'htk_msg_router_init_ok'          : ["Router zpráv '{0}' úspěšně inicializován"],
    'htk_core_msg_service_add_ok'     : ["Fronta zpráv jádra '{0}' úspěšně zaregistrována"],
    'htk_core_msgq_init_ok'           : ["Fronta zpráv jádra '{0}' úspěšně inicializována"],
    'htk_core_msgq_connect_ok'        : ["Fronta zpráv jádra '{0}' úspěšně připojena"], 
    'htk_load_int_ext'                : ["Nahrávám interní rozšíření: '{0}'"],
    'htk_load_int_ext_success'        : ["Interní rozšíření: '{0}' úspěšně nahráno"],
    'htk_load_ext_ext'                : ["Nahrávám externí rozšíření: '{0}'"],
    'htk_load_ext_ext_success'        : ["Externi rozšíření: '{0}' úspěšně nahráno"],
    'htk_load_ext_msg'                : ["Načítám zprávy rozšíření pro jazyk {0}, package '{1}'"],
    'htk_load_ext_msg_success'        : ["Zprávy rozšíření pro jazyk {0}, úspěšně načteny"],
    'htk_load_ext_msg_failed'         : ["Nepodařilo se načíst zprávy rozšíření pro jazyk {0}, důvod: {1}"],
    'htk_load_ext_help'               : ["Načítám napovědu rozšíření pro jazyk {0}, package '{1}'"],
    'htk_load_ext_help_failed'        : ["Nepodařilo se načíst nápovědu rozšíření pro jazyk {0}, důvod: {1}"],
    'htk_load_global_msg'             : ["Načítám globální zprávy pro jazyk {0}, package '{1}'"],
    'htk_load_global_msg_success'     : ["Globální zprávy pro jazyk {0}, načteny úspěšně"],
    'htk_load_global_msg_failed'      : ["Nepodařilo se načíst globální zprávy pro jazyk {0}, důvod: {1}"],
    'htk_load_global_help'            : ["Načítám globální nápovědu pro jazyk {0}, package '{1}'"],
    'htk_load_global_help_success'    : ["Globální nápověda pro jazyk {0}, načtena úspěšně"],
    'htk_load_global_help_failed'     : ["Nepodařilo se načíst globální nápovědu {0}, důvod: {1}"],
    'htk_load_package_msg'            : ["Načítám zprávy knihovny '{0}' pro jazyk {1}"],
    'htk_load_package_msg_success'    : ["Zprávy knihovny {0} pro jazyk {1}, načteny úspěšně"],
    'htk_load_package_msg_failed'     : ["Nepodařilo se načíst zprávy knihovny {0} pro jazyk {1}, důvod: {2}"],
    'htk_ext_ext_dir_not_exists'      : ["Adresář externích rozšíření '{0}' je definován v konfiguraci, ale neexistuje"],
    'htk_fin_load_int_ext'            : ["Dokončeno nahrávání interních rozšíření"],
    'htk_fin_load_ext_ext'            : ["Dokončeno nahrávání externích rozšíření"],
    'htk_fail_load_int_ext'           : ["Nahravání interního rozšíření: '{0}' skonšilo s chybou: {1}"],
    'htk_fail_init_int_ext'           : ["Inicializace interního rozšíření: '{0}' skončila s chybou: {1}"], 
    'htk_fail_load_ext_ext'           : ["Nahrávání externího rozšíření: '{0}' skončilo s chybou: {1}"],
    'htk_fail_to_create_obj'          : ["Nepodařilo se vytvořit objekt"],
    'htk_cthread_init'                : ["Inicializuji vlákno jádra id: {0}"],
    'htk_cworker_init'                : ["Začínám pracovat"],
    'htk_cworker_term'                : ["Ukončuji práci"],
    'htk_cthread_destroy'             : ["Ukončuji vlákno jádra id: {0}"],
    'htk_cthread_sleep'               : ["Usínám..."],
    'htk_cthread_awake'               : ["Probuzen"],
    'htk_core_workers_num_set'        : ["Počet workerů jádra nastaven na: {0}"],
    'htk_pid_file_set'                : ["Ukládám PID {0} do souboru: {1}"],
    'htk_pid_file_delete'             : ["Smazán PID soubor: {0}"],    
    'htk_app_not_running'             : ["Aplikace není spuštěna, nebyl nalezen PID"],
    'htk_app_stopped'                 : ["Aplikace byla ukončena"], 
    'htk_app_not_running_except'      : ["Aplikace není spuštěna, během požadavku na ukončení vznikla výjimka"],
    'htk_app_running_with_pid'        : ["Aplikace je spuštěna, hlavní PID je {0}"],
    'htk_app_not_running_with_pid'    : ["Aplikace není spuštěna, byl nalezen PID {0} předchozího spuštění"],
    'htk_app_stop_request_soft'       : ["Posílám požadavek na ukončeni aplikace (soft)"],
    'htk_int_msgq_init'               : ["Inicializuji vnitřní globální frontu zpráv, qid: {0}"],
    'htk_oint_msgq_init'              : ["Inicializuji privátní frontu zpráv dozorce"],
    'htk_observer_init'               : ["Začínám dohlížet"],
    'htk_observer_term'               : ["Ukončuji dozor"],
    'htk_observer_sleep'              : ["Usínám..."],
    'htk_observer_awake'              : ["Probuzen"],
    'htk_sig_recv'                    : ["Zachycen signál: {0}"],
    'htk_htk_reg_int_srv_msgq'        : ["Registruji vnitřní frontu zpráv id: {0} pro službu: {0}"],
    'htk_app_service_reg_ok'          : ["Registrována aplikační služba {0} - {1}"],
    'htk_app_service_start_ok'        : ["Aplikační služba {0} byla úspěšně spuštěna"],
    'htk_app_service_stop'            : ["Zastavuji aplikační službu {0} (soft)"],
    'htk_app_service_stop_failed'     : ["Nepodařilo se ukončit aplikační službu {1} ve stanoveném čase"],
    'htk_app_service_stop_hard'       : ["Zastavuji aplikační službu {0} (hard)"],
    'htk_app_service_inactive_skip'   : ["Vynechávám neaktivni aplikační službu {0}"],
    'htk_app_service_already_running' : ["Aplikační služba {0} je již spuštěna"],
    'htk_create_cfg_db'               : ["Vytvářím konfigurační databázový soubor: {0}"],
    'htk_remove_cfg_db'               : ["Mažu předchozí konfigurační databázový soubor"],
    'htk_cfg_db_exists'               : ["Již existuje konfigurační databázový soubor, k přepssání použij --force "],
    'htk_create_cfg_db_error'         : ["Konfigurační databázový soubor nelze vytvořit {0}"],
    'htk_cfg_db_not_spec'             : ["Konfigurační databázový soubor není specifikován"],
    'htk_reg_msg_service_failed'      : ["Nepodařilo se zaregistrovat službu message: {0}"],
    'htk_write_cfg_db'                : ["Zapisuji do konfigurační databáze"],
    'htk_cworker_check_priv_msg'      : ["Kontroluji privmsg"],
    'htk_cworker_check_activity'      : ["Kontroluji stav vlákna: {0}, poslední aktivita před: {1}"],
    'htk_loading_ext_cfg'             : ["Načítám konfiguraci rozšíření {0}"],
    'htk_ext_cfg_loaded'              : ["Konfigurace rozšíření načtena {0}"],
    'htk_loading_base_cfg'            : ["Načítám základní konfiguraci {0}"],
    'htk_base_cfg_loaded'             : ["Základní konfigurace načtena {0}"],
    'htk_base_cfg_missing'            : ["Chybí základní konfigurační soubor {0}"],
    'htk_loading_extension'           : ["{0} je archív ... načítám z {1}"],
    'htk_extension_wrong_cfg_file'    : ["Nalezeno nesprávně nakonfigurované rozšíření {0}, soubor {1} je neplatný"],  
    'htk_extension_wrong_cfg'         : ["Nalezeno nesprávně nakonfigurované rozšíření {0}"],
    'htk_help_cmd_def_missing'        : ["Chybějící nápověda příkazu {0}, jatyk {1}"],
    'htk_option_def_missing'          : ["Chybějící definice volby {0}, jazyk {1}"],
    'htk_cworker_process_msg'         : ["PONG od vlákna {0}, rychlost: {1}"],
    'htk_duplicate_extension'         : ["Pokus o načtení duplicitního rozšíření '{0}'"],
    'htk_short_opt_registered'        : ["Krátká volba {0} je již zaregistrována"],
    'htk_short_opt_invalid'           : ["Krátká volba {0} není platný řetězec"],
    'htk_long_opt_registered'         : ["Dlouhá volba {0} je již zaregistrována"],
    'htk_long_opt_invalid'            : ["Dlouhá volba {0} není platný řetězec"],
    'htk_cmd_registered'              : ["Příkaz {0} je již zaregistrován"],
    'htk_cmd_invalid'                 : ["Příkaz {0} není platný řetězec"],
    'htk_fn_hook_invalid'             : ["Neplatný funkční hook, návratová hodnota musí být True"],
    'htk_app_service_invalid'         : ["Název služby musí být platný řetězec, bylo zadáno: {0}"],
    'htk_app_service_registered'      : ["Služba: {0} je již zaregistrována"],
    'htk_app_service_desc_missing'    : ["Není specifikován popis lužby"],
    'htk_cb_not_callable'             : ["Parametr callbacku musí být callable object"],
    'htk_app_service_start_failed'    : ["Nepodařilo se spustit aplikační službu {0}"]                
}