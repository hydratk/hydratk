# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.lib.en.messages
   :platform: Unix
   :synopsis: English language translation for global library messages
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

language = {
    'name': 'English',
    'ISO-639-1': 'en'
}

msg = {
    'htk_lib_undefined_group': ["Undefined group {0}"],
    'htk_lib_duplicate_option': ["Option add duplicate {0}"],
    'htk_lib_commandline_not_parsed': ["Commandline needs to be parsed first"],
    'htk_lib_short_help': ["For list of all available commands and options type"],
    'htk_lib_pocket_content': ["Pocket items: {0}"],
    'htk_lib_pocket_empty': ["Pocket is empty"],
    'htk_lib_undefined_hook': ["Undefined hook"],
    'htk_lib_queue_not_supported': ["{0} queue is not available, it requires module {1} to be loaded first"],
    'htk_lib_queue_not_loaded': ["Queue type: {0} is not supported"],
    'htk_lib_queue_invalid_type': ["Invalid Queue type"],
    'htk_lib_queue_invalid_operation': ["This operation cannot be done on this queue type"],
    'htk_lib_cb_handler_not_set': ["{0} callback handler not set, callback will be not processed"],
    'htk_lib_nothing_to_process': ["There's nothing to process"],
    'htk_lib_undefined_fn': ["{0} is not defined"],
    'htk_lib_undefined_callback': ["Undefined callback id: {0}"],
    'htk_lib_running_request': ["{0}: running request {1}"],
    'htk_lib_unknown_driver': ["Not existing driver: {0}"],
    'htk_lib_not_installed': ["Library {0} not installed"],
    'htk_lib_db_dsn_error': ["Error initialize database driver, dsn parse {0} error"],
    'htk_lib_db_not_connected': ["Not connected"]
}
