.. _module_hydra_core_events:

events
======

This sections contains module documentation of events modules.

event
^^^^^

Module provides class Event as base event class.
Unit tests available at hydratk/core/event/01_methods_ut.jedi

**Attributes** :

* _id - event id
* _args - tuple content
* _data - dictionary content
* _propagate - bool, propagate event
* _run_default - standard event processing
* _skip_before_hook - skip ^event (generated before main event)
* _skip_after_hook - skip $event (generated after main event)

**Properties (Getters)** :

* skip_before_hook - returns _skip_before_hook
* skip_after_hook - returns _skip_after_hook

**Methods** :

* __init__

Method sets event content (_id, args to _args, kwargs to _data).

* id

Method returns _id.

* argc

Method returns count of args.

* args

Method returns _args.

* get_all_data

Methods returns _data.

* get_data

Methods returns given _data item.

* set_data

Method sets given _data item.

* argv

Method returns _args item for given index.

* set_argv

Method sets _args item for given index.

* stop_propagation

Method sets _propagate to False.

* prevent_default

Method sets _run_default to False.

* will_run_default

Method returns _run_default. 

* propagate

Method returns _propagate.

eventhandler
^^^^^^^^^^^^

Module provides class EventHandler which implements handler for various events.
Handler doesn't implement any business logic, just point to another method.
Unit tests available at hydratk/core/eventhandler/01_methods_ut.jedi

**Methods** :

* _ec_check_co_privmsg - calls _check_co_privmsg
* _ec_check_cw_privmsg - calls _check_cw_privmsg
* _ec_stop_app - calls _stop_app
* _eh_htk_on_got_cmd_options - call apply_command_options
* _eh_htk_on_debug_info - calls dout
* _eh_htk_on_warning - calls wout if printing enabled by configuration
* _eh_htk_on_extension_warning - calls wout
* _eh_htk_on_error - calls errout
* _eh_htk_on_exception - calls exout
* _eh_htk_on_extension_error - calls errout
* _eh_htk_on_cprint - calls spout
* _ec_sig_handler - calls dmsg, signal id is translated to name

events
^^^^^^

Module provides list of hydratk core events.

hsignal
^^^^^^^

Signal id translation to name, event.