# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.cs.messages
   :platform: Unix
   :synopsis: Czech language translation for global library messages
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

language = {
    'name': 'Čeština',
    'ISO-639-1': 'cs'
}

msg = {
    'htk_lib_undefined_group': ["Nedefinovaná skupina {0}"],
    'htk_lib_duplicate_option': ["Duplicitní volba {0}"],
    'htk_lib_commandline_not_parsed': ["Commandline musí být nejprve parsován"],
    'htk_lib_short_help': ["Pro dostupné příkazy a volby spusť"],
    'htk_lib_pocket_content': ["Položky v pocketu: {0}"],
    'htk_lib_pocket_empty': ["Pocket je prízdný"],
    'htk_lib_undefined_hook': ["Nedefinovaný hook"],
    'htk_lib_queue_not_supported': ["{0} fronta není dostupná, module {1} musí být nejprve nahrán"],
    'htk_lib_queue_not_loaded': ["Fronta: {0} není podporovaná"],
    'htk_lib_queue_invalid_type': ["Neplatný typ fronty"],
    'htk_lib_queue_invalid_operation': ["Fronta nepodporuje tuto operaci"],
    'htk_lib_cb_handler_not_set': ["{0} callback handler není nastaven, callback nebude zpracován"],
    'htk_lib_nothing_to_process': ["Nic ke zpracování"],
    'htk_lib_undefined_fn': ["{0} není definováno"],
    'htk_lib_undefined_callback': ["Nedefinovaný callback s id: {0}"],
    'htk_lib_running_request': ["{0}: spuštím požadavek {1}"],
    'htk_lib_unknown_driver': ["Neexistující driver: {0}"],
    'htk_lib_not_installed': ["Knihovna {0} není nainstalována"],
    'htk_lib_db_dsn_error': ["Nebylo možné inicializovat databázový driver, chyba při parsování dsn{0}"],
    'htk_lib_db_not_connected': ["Spojení nebylo navázáno"]
}
