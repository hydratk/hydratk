# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.en.messages
   :platform: Unix
   :synopsis: English language translation for global messages
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

language = {
  'name' : 'English',
  'ISO-639-1' : 'en'
}

from hydratk.core import const;

HIGHLIGHT_START = chr(27)+chr(91)+"1m";
HIGHLIGHT_US    = chr(27)+chr(91)+"4m";
HIGHLIGHT_END   = chr(27)+chr(91)+"0m";

msg = {
    'htk_print_short_desc' : HIGHLIGHT_START + const.APP_NAME +" v"+ const.APP_VERSION + const.APP_REVISION + HIGHLIGHT_END + " for Unix operating systems",
    'htk_print_cp_string'  : "(c) " + const.APP_AUTHORS + " " + "(" + const.APP_DEVEL_YEAR + ")",
    'htk_unknown_command'  : "Unknown command: " + HIGHLIGHT_START +"%s" + HIGHLIGHT_END +", for help type command " + HIGHLIGHT_START + "help" + HIGHLIGHT_END,
    'htk_help_syntax'      : "Usage: " + HIGHLIGHT_START + "%s [options] command" + HIGHLIGHT_END,
    'htk_help_commands'    : HIGHLIGHT_US + 'Commands:' + HIGHLIGHT_END,
    'htk_help_command'     : HIGHLIGHT_US + 'Command:' + HIGHLIGHT_END,
    'htk_help_options'     : HIGHLIGHT_US + 'Options:' + HIGHLIGHT_END,
    'htk_help_option'      : HIGHLIGHT_US + 'Option:' + HIGHLIGHT_END,
    'htk_help_glob_options'  : HIGHLIGHT_US + 'Global Options:' + HIGHLIGHT_END, 
    'htk_invalid_cmd'        : "Invalid command: %s",
    'htk_undetected_cmd'     : "Input command was not detected",
    'htk_app_start'          : "Starting application",
    'htk_app_stop'           : "Stopping application",
    'htk_app_exit'           : "Application exit",
    'htk_conf_not_exists'    : "Config file '%s' doesn't exists",
    'htk_opt_set'            : "Option '%s' set to: '%s'",
    'htk_unrecognized_opt'   : "Option '%s' is not recognized",
    'htk_opt_ignore'         : "Option setting '%s' was ignored, because of invalid value: '%s'",
    'htk_conf_opt_missing'   : "Config error, section: '%s', option: '%s' is not defined",
    'htk_conf_opt_val_err'   : "Config error, section: '%s', option: '%s' incorrect value",
    'htk_debug_enabled'      : "Starting application in debug mode", 
    'htk_lang_set'           : "Language set to '%s'",
    'htk_invalid_lang_set'   : "Language '%s' is not supported",
    'htk_debug_level_set'    : "Debug level set to %d",
    'htk_msg_router_id_set'  : "Main message router id set to '%s'",
    'htk_msg_router_init_ok' : "Message Router '%s' initialized successfully",
    'htk_core_msg_service_add_ok' : "Core message service '%s' registered successfully",
    'htk_core_msgq_init_ok'       : "Core message queue '%s' initialized successfully",
    'htk_core_msgq_connect_ok'    : "Core message queue '%s' connected successfully",
    'htk_load_int_ext'            : "Loading internal extension: '%s'",
    'htk_load_int_ext_success'    : "Internal extension: '%s' loaded successfully", 
    'htk_load_ext_ext'            : "Loading external extension: '%s'",
    'htk_load_ext_msg'            : "Trying to to load extension messages for language %s, package '%s'",
    'htk_load_ext_msg_success'    : "Extensions messages for language %s, loaded successfully",
    'htk_load_ext_msg_failed'     : "Failed to load extension messages for language %s, reason: %s",
    'htk_load_ext_help'           : "Trying to to load extension help for language %s, package '%s'",
    'htk_load_ext_help_failed'    : "Failed to load extension help for language %s, reason: %s",
    'htk_load_global_msg'         : "Trying to to load global messages for language '%s', package '%s'",
    'htk_load_global_msg_success' : "Global messages for language %s, loaded successfully",
    'htk_load_global_msg_failed'  : "Failed to load global messages for language %s, reason: %s",
    'htk_load_global_help'        : "Trying to to load global help for language %s, package '%s'",
    'htk_load_global_help_success' : "Global help for language %s, loaded successfully",
    'htk_load_global_help_failed'  : "Failed to load global help for language %s, reason: %s",
    'htk_ext_ext_dir_not_exists'  : "External extension directory '%s' configured, but doesn't exists",
    'htk_fin_load_int_ext'        : "Finished loading internal extensions",
    'htk_fin_load_ext_ext'        : "Finished loading external extensions",
    'htk_load_ext_ext_success'    : "External extension: '%s' loaded successfully", 
    'htk_fail_load_int_ext'       : "Loading internal extension: '%s' failed with error: %s",
    'htk_fail_init_int_ext'       : "Initialization of internal extension: '%s' failed with error: %s", 
    'htk_fail_load_ext_ext'       : "Loading external extension: '%s' failed with error: %s",  
    'htk_fail_to_create_obj'      : "Creating object failed",
    'htk_cthread_init'            : "Initializing core thread id: %s",
    'htk_cworker_init'            : "Starting to work",
    'htk_cworker_term'            : "Terminating work",
    'htk_cthread_destroy'         : "Destroying core thread id: %s",
    'htk_cthread_sleep'           : "Sleeping...",
    'htk_cthread_awake'           : "Awake",
    'htk_core_workers_num_set'    : "Number of core workers set to: %s", 
    'htk_pid_file_set'            : "Saving PID %s to file: %s", 
    'htk_pid_file_delete'         : "PID file deleted: %s",
    'htk_app_not_running'         : "Application is running, PID not found",
    'htk_app_stopped'             : "Application was shuted down",
    'htk_app_not_running_except'  : "Application is running, during the shutdnow request an exception was raised",
    'htk_app_running_with_pid'    : "Application is running, main PID is %s",
    'htk_app_not_running_with_pid' : "Application is not running, found previous run PID %s",
    'htk_app_stop_request_soft'    : "Sending request to shutdown the application (soft)",
    'htk_int_msgq_init'            : "Initializing internal global message queue, qid: %s",
    'htk_oint_msgq_init'           : "Initializing observer's private message queue", 
    'htk_observer_init'            : "Starting to observe",
    'htk_observer_term'            : "Stopping observation",
    'htk_observer_sleep'           : "Sleeping...",
    'htk_observer_awake'           : "Awake",
    'htk_sig_recv'                 : "Retrived signal: %s",
    'htk_reg_int_srv_msgq'         : "Registering internal message queue id: %s for service: %s",
    'htk_app_service_reg_ok'       : "Registered application service %s - %s",
    'htk_app_service_start_ok'     : "Application service %s successfully started",
    'htk_app_service_stop'         : "Stopping application service %s",
    'htk_app_service_stop_failed'  : "Failed to stop applicaton service %s in defined time",
    'htk_app_service_stop_hard'    : "Stopping application service %s (hard)",
    'htk_app_service_inactive_skip' : "Bypassing inactive application service %s",
    'htk_app_service_already_running' : "Application service %s is already running"     
}
