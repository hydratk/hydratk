.. _module_hydra_core_corehead:

corehead
========

This sections contains module documentation of corehead module.

corehead
^^^^^^^^

Module provides class CoreHead inherited from MessageHead, EventHandler, Debugger, Profiler, Logger.
Unit tests available at hydratk/core/corehead/01_methods_ut.jedi, 02_methods_ut.jedi, 03_methods_ut.jedi, 04_methods_ut.jedi

**Attributes** :

* _runlevel - default run level
* _config - in-memory configuration
* _language - default language
* _config_file - configuration filename
* _ext_confd - directory for extensions configuration
* _use_extensions - bool, enable extensions
* _ext - list of extensions
* _default_command - short-help
* _help_title - help string
* _cp_string - copyright
* _command - input command
* _opt_profile - htk option profile
* _cmd_option_hooks - list of option hooks
* _event_hooks - list of event hooks
* _cmd_hooks - list of command hooks
* _fn_hooks - list of functionality hooks
* _msg_router_id - default router identifier
* _msg_router - reference to MessageRouter
* _app_status
* _observer_status
* _thr - list of worker threads
* _trn - reference to Translator
* _pid_file - PID filename
* _option
* _option_param
* _app_service
* _run_mode - default run mode
* _fn_callback
* _fn_cb
* _fn_cb_shared
* _async_fn_tickets - tickets storage
* _cbm - reference to CallBackManager
* _async_fn
* _async_fn_ex

**Methods** :

* _bootstrap

Method executes functionality hooks according to run level (h_runlevel_baseinit, h_runlevel_config, h_runlevel_extensions, 
h_runlevel_cli, h_runlevel_core, h_runlevel_appl).

* _create_config_db

Method handles command create-config-db and creates configuration database using method _write_config_db. By default it takes
filename from configuration or from option config-db-file if provided. Database can be recreated using option force.

* _c_observer

Method initialized observer process (marked as hydratk/c_observer). It initializes message router according to configuration 
service c01, IPC transport, address /tmp/hydratk/core.socket). Router currently supports only ZeroMQ, observer process is queue sender. 
Method creates PID file (/tmp/hydratk/hydratk.pid, observer process id).

Then method initializes worker processes (4 by default) and registers signal hooks (INT, TERM, PIPE). Then it runs in infinite loop
till the processing is allowed by process status. It fires event htk_before_cw_activity_check, checks status of worker processes, 
fires event htk_on_cobserver_ctx_switch and goes asleep.

When processing should be stopped it stops services, destroys worker processes and deletes PID file.

* _c_worker

Method initializes worker process (marked as hydratk/core:num). First it fires event htk_on_cworker_init and registers signal hooks.
It connects to message queue as receiver. Then it runs in infinite loop till the processing is allowed by process status.
It checks incoming messages, processes them and goes asleep.

* _check_co_privmsg

Method checks incoming messages from worker processes (observer as receiver) via pipe connection. It processes the messages.

* _write_config_db

Method writes in-memory configuration to database.

* _dopoll

Method receives messages from pipe.

* _check_core_msg_queue

Method receives messages from queue and fires event.

* _check_cw_privmsg

Method checks incoming messages from observer process (worker as receiver) via pipe connection. It processes the messages.

* _check_cw_activity

Method checks activity of worker processes using. The check time is regularly updated and observer can determine workers which
are not responding.

* _do_command_action

Method executes hook for input command. By default it executes short-help if command is not registered.

* _load_db_config

Method loads configuration from database (filename is configured) to memory (it updates _config).

* _process_extension_configs

Method searches directory _ext_confd for extension configuration files. It fires event htk_before_append_extension_config_file
and loads configuration to memory.

* _append_extension_config_from_file

Method parses extension configuration file and merges it with current in-memory configuration.

* _merge_base_config

Method adds new configuration items to current configuration.

* _load_base_config

Method parses htk configuration and sets _config_file.

* _apply_config

Method sets several attributes according to configuration (_debug, _language including langtext import, _run_mode, 
_msg_router_id, _num_threads).

* _load_extensions

Method imports extension modules (module and package are configured).

* _load_extension

Method import extension module including its langtexts. It sets _ext if extension is enabled.

* _extension_module_import

Method imports extensio module using method __import__.

* _load_module_from_file

Method imports module in file using method load_source (*.py) or load_compiled (*.pyc).

* _import_extension_messages

Method imports extension messages (langtexts and help).

* _import_package_messages

Method import library langtexts.

* _import_global_messages

Method import hydratk messages (langtexts and help).

* _reg_self_command_hooks

Method registers hooks for commands (start, stop, short-help, help, list-extensions, create-config-db, create-ext-skel, create-lib-skel).

* _runlevel_baseinit

Method executes specific processing for runlevel baseinit (initialize translator, import messages, register hooks).

* _runlevel_config

Method executes specific processing for runlevel config (load configuration from several sources - base, extensions, database).

* _runlevel_extensions

Method executes specific processing for runlevel extensions (load extension). It fires events htk_before_load_extensions, htk_after_load_extensions.

* _runlevel_cli

Method executes specific processing for runlevel cli (parse command options).

* _runlevel_core

Method executes specific processing for runlevel core (subscribe managers if running in parallel processing mode).

* _runlevel_app

Method executes specific processing for runlevel appl (process input command).

* _run_command_option_hooks

Method executes callbacks when option hook is registered.

* _run_command_hooks

Method executes callbacks when command hook is registered.

* _set_default_cli_params

Method initializes console help including registered commands and options.

* _set_pid_file

Method creates PID file and stores process id.

* _notify_thread

Method sends PIPE signal to given process.

* _send_ping

Method sends PING message to pipe connection and sends PIPE signal.

* _service_starter

Method initializes service process (marked as hydratk/srv:name), registers signal hooks and executes service callback.

* _sig_retriever

Method handles received signal. It fires event htk_on_signal and special event for given signal (htk_on_sigterm|htk_on_sigint|htk_on_sigpipe|htk_on_sigalamr).

* _reg_service_signal_hooks

Method registers hooks for signal TERM, INT, PIPE.

* _reg_self_fn_hooks

Method registers functionality hooks for bootstrap and all runlevels (h_bootstrap, h_runlevel_baseinit, h_runlevel_config, h_runlevel_extensions,
h_runlevel_cli, h_runlevel_core, h_runlevel_appl).

* _reg_self_event_hooks

Method registers hooks for several events (htk_on_error, htk_on_warning, htk_on_debug_info, htk_on_cprint, htk_on_got_cmd_options, 
htk_on_extensions_error, htk_on_extension_warning, htk_on_uncaught_exception, htk_on_cmsg_recv).

* _parse_cli_args

Method parses input command including options (executes registered hooks). It fires event htk_on_cmd_options.

* _process_cw_msg

Method process PONG message from worker process and updates check time. 

* _trigger_cmsg

Method fires event htk_on_cmsg_recv with given message content.

* _response_ping

Method send PONG message via pipe and sends PIPE signal to observer process.

* _process_privmsg

Method fires event h_privmsg_recv and processes received message. It replies with PONG message when receives PING.

* _remove_pid_file

Method deletes PID file.

* _reg_self_signal_hooks

Method registers event hooks for signals (htk_on_sigint, htk_on_sigterm, htk_on_sigpipe).
Observer process is authorized to stop application, worker process can't stop it.

* _start_app

Method fires event htk_on_start and initializes observer process.

* _stop_app

Method fires event htk_on_stop and notifies observer process to terminate processing (via process status).

* _stop_app_command

Method sends TERM signal and waits for process termination in infinite loop.

* _init_message_router

Method sets _msg_router.

* _list_extensions

Method prints info about all extensions loaded in _ext.