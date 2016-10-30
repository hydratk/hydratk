.. _module_hydra_core_masterhead:

masterhead
==========

This sections contains module documentation of masterhead module.

masterhead
^^^^^^^^^^

Module provides class MasterHead inherited from PropertyHead, ServiceHead, CoreHead, ModuleLoader.
Unit tests available at hydratk/core/masterhead/01_methods_ut.jedi, 02_methods_ut.jedi, 03_methods_ut.jedi, 04_methods_ut.jedi, 05_methods_ut.jedi

**Attributes** :

* _instance - MasterHead reference
* _instance_created - bool

**Methods** :

* __init__

Method prevents to create MasterHead instance using constructor (Singleton pattern). It can be created using method get_head.
It registers functionality hooks and overrides standard exception handler sys.excepthook.

* exception_handler

Method fires event htk_on_uncaught_exception with traceback content.

* get_translator

Method returns _trn.

* get_head

Method returns MasterHead reference and creates it when not initialized. It is static method because __init__usage  is not allowed.

* get_config

Method returns _config.

* check_run_mode

Method sets _run_mode according to option run-mode.

* check_language

Method sets _language according to option language.

* check_config

Method sets _config_file according to option config.

* check_profile

Method enables profiler if option profile is provided.

* Method sets _debug, _debug_level according to option debug.

* check_debug_channel

Method sets _debug_channel according to option debug-channel.

* match_short_option

Method registers short command option or list for given group (including has_value, d_opt, allow_multiple).

* match_long_option

Method registers long command option or list for given group (including has_value, d_opt, allow_multiple).

* match_cli_option

Method registers both long and short command option. It can be used to create option aliases for one target option.

* match_cli_command

Method registers command for given group.

* set_cli_cmdopt_profile

Method sets new option profile. The profile is empty and options must be registered separately.

* set_cli_appl_title

Method sets _help_title, _cp_string.

* register_fn_hook

Method registers functionality hook in _fn_hooks with given callback.

  .. code-block:: python  
     
     mh.register_fn_hook('mh_bootstrap', my_bootstrapper)   

* run_fn_hook

Method executes functionality hook callback if registered. Parameters are passed as args, kwargs.

* dummy_fn_hook

Dummy callback returning allways True.

* start_pp_app

Method calls _start_app, used in parallel mode.

* stop_pp_app

Method calls _stop_app, used in parallel mode.

* register_command_hook

Method registers command hook in _cmd_hooks with given callback.

  .. code-block:: python
  
     mh.register_command_hook('mycommand4', fc_command_handler)

* register_command_option_hook

Method registers option hook in _cmd_option_hooks with given callback.

* register_event_hook

Method registers event hook in _event_hooks with given callback. The event can have priority for processing order.

  .. code-block:: python
  
     hook = [
             {'event' : 'htk_on_error', 'callback' : self.my_error_handler, 'unpack_args' : True, 'priority' : const.EVENT_HOOK_PRIORITY - 1}, # will be prioritized        
             {'event' : 'htk_on_warning', 'callback' : self.my_warning_handler, 'unpack_args' : False}
            ]            
                      
     mh.register_event_hook(hook)  
     
* unregister_event_hook

Method removes given event from _event_hooks.

* replace_event_hook

Method replaces event hook configuration.

* fire_event

Method fires requested event. By default it fires also events ^event, $event (before and after).
If event is registered in hooks method automatically executes callback.

* apply_command_options

Method sets _debug, _debug_level, _language according to options debug, language.

* get_language

Method returns _language.

* have_command_action

Method checks if _command is set.

* get_command_action

Method returns _command.

* service_registered

Method checks if service is register in _app_service.

* register_service

Method registers new service if not already registered and initializes service process.

* start_service

Method starts process for given service if not running.

* stop_services

Method sends INT signal to all running service processes. If service not stopped method sends KILL signal.

* init_core_threads

Method initializes worker process pool (by default 4 processes).

* destroy_core_threads

Method terminates worker processes in pool using status.

* add_core_thread

Method initializes and starts worker process. It is connected with observer process via pipe.

* get_thrid

Method returns process name (0 is main process).

* create_ext_skel

Method handles command create-ext-skel and creates extension skeleton in directory ~/hydratk by default.
The path can be specified in option ext-skel-path. It creates all directories and files configured in module template (including file content).
Method supports interactive mode it prompts for metadata (installation directory, extension name, description, author, email, license).     

* create_lib_skel

Method handles command create-lib-skel and creates libraru skeleton in directory ~/hydratk by default.
The path can be specified in option lib-skel-path. It creates all directories and files configured in module template (including file content).
Method supports interactive mode it prompts for metadata (installation directory, library name, description, author, email, license).

* async_fn_ex

Method sends message with asynchronous functionality hook.

* send_msg

Method sends message to queue.

* async_ext_fn

Method sends message with asynchronous extension hook.

* get_async_ticket_content

Method gets given ticket from storage.

* async_ticket_completed

Method checks if given ticket is completed (already processed).

* delete_async_ticket

Method deletes given ticket from storage.

* register_async_fn_ex

Method registers asynchronous functionality hook in _async_fn_ex with given callback.

* reg_fn_cb

Method registers functionality callback in _fn_callback.

* register_async_fn

Method registers asynchronous functionality hook in _async_fn.

* get_ext

Method returns returns reference to given extension. 