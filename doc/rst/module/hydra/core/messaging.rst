.. _module_hydra_core_messaging:

messaging
=========

This sections contains module documentation of messaging modules.

message
^^^^^^^

Module provides class FnCallBackMsg
Unit tests available at hydratk/core/message/01_methods_ut.jedi

**Attributes** :

* _type - callback message type (FN_CALLBACK = 1)
* _callback - callback method
* _args - passed to callback as args
* _kwargs - passed to callback as kwargs

**Methods** :

* __init__

Method sets callback method and arguments.

* set_callback

Method sets _callback.

* set_args

Method sets _args, _kwargs.

* run

Method executes callback with given arguments.

messagehead
^^^^^^^^^^^

Module provides class MessageHead.
Unit tests available at hydratk/core/messagehead/01_methods_ut.jedi

**Attributes** :

* _async_ticket_seq - sequence start point
* _async_ticket_seq_max - sequence end point
* _current_async_ticket_id - current sequence id

**Methods** :

* _new_async_ticket_id

Method prepares id for new ticket from sequence. It resets sequence if end point reached.

* _new_async_ticket

Method stores ticket to _async_fn_tickets.

* _delete_async_ticket

Method deletes ticket from _async_fn_tickets.

* _reset_async_ticket_seq

Method resets sequence.

* _reg_msg_handlers

Method registers hooks for functionality hooks (cmsg_async_fn_ex, cmsg_async_fn, cmsg_async_ext_fn).

* _process_cmsg

Method decodes binary message, parses it and executes stored functionality hook.

* _send_msg

Method sends message to ZeroMQ.

* _msg_async_ext_fn

Method extracts extension and method from message. It finds ticket in _async_fn_tickets, executes callback and marks ticket as finished.

messagerouter
^^^^^^^^^^^^^

Module provides class MessageRouter.
Unit tests available at hydratk/core/messagerouter/01_methods_ut.jedi

**Attributes** :

* _service_list - list of registered services
* _id - router identifier
* _trn - reference to Translator

**Methods** :

* __init__

Method sets _id, _trn.

* register_service

Method adds new service to _service_list if not registered with given configuration.

* get_service_address

Methods gets address of given service from configuration.