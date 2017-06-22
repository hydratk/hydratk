.. _module_hydra_lib_debugging:

debugging
=========

This sections contains module documentation of debugging modules.

simpledebug
^^^^^^^^^^^

Module provides debugging methods.
Unit tests available at hydratk/lib/debugging/simpledebug/01_methods_ut.jedi

* dmsg

Method prints debug message. The text is automatically translated and filled with dynamical parameters.

* wmsg 

Method writes warning message.

firepot
^^^^^^^

Modules provides class FirePot which implements FireLogger protocol.
Unit tests available at hydratk/lib/debugging/firepot/01_methods_ut.jedi

**Attributes** :

* _items - list of log records
* _enabled - logger state
* _levels
* _name
* _counter
* _style

**Methods** :

All methods are static.

* enable

Methods set _enabled.

* enabled

Method returns _enabled.

* log

Method prepares dictionary of args and stores it to _items.

* flush_items

Method resets _items to empty list.

* get_headers

Method transforms _items to dictionary of headers.