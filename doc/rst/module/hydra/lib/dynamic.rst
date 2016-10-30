.. _module_hydra_lib_dynamic:

dynamic
=======

This sections contains module documentation of dynamic modules.
Module callback provides several classes for management of callbacks.
Unit tests available at hydratk/lib/dynamic/callback/01_methods_ut.jedi

Class CallBack
^^^^^^^^^^^^^^

**Attributes** :

* _shared - bool, shared callback
* _async - bool, aynchronous callback
* _fn_id - functionality id
* _fn - functionality name
* _obj - binary object
* _args - callback args
* _kwargs - callback kwargs

**Properties (Getters)** :

* args - returns _args
* kwargs - returns _kwargs
* fn_id - returns _fn_id
* fn - returns _fn
* obj - returns _obj
* shared - returns _shared
* async - returns _async

**Properties (Setters)** :

* args - sets _args
* kwargs - sets _kwargs
* shared - sets _shared
* async - sets _async

**Methods** :

* __init__

Method sets callback attributes (_fn_id, _fn, _obj).

* set_fn

Method sets _fn.

* set_obj

Method sets _obj (pickled to binary).

Class CallBackManager
^^^^^^^^^^^^^^^^^^^^^

**Attributes** :

* _cb_dict - dictionary of callbacks
* _cb_dproxy - proxy dictionary of callbacks
* _cbm_proc - reference to CallBackProcessor
* _async_handler - reference to AsyncCallBackHandler
* _sync_handler - reference to SyncCallBackHandler

**Properties (Getters)** :

* sync_handler - returns _sync_handler
* async_handler - returns _async_handler
* run - returns _cbm_proc

**Methods** :

* __init__

Method sets _cb_dict, _cb_dproxy, _cbm_proc, _sync_handler.

* set_sync_handler

Method sets _sync_handler.

* set_async_handler

Method sets _async_handler.

* set_db_dict

Method sets _cb_dict.

* set_cb_dproxy

Method sets _cb_dproxy.

* create_db_dproxy

Method initializes _cb_dproxy.

* get_cb

Method gets callback from _cb_dict or _cb_dproxy.

* reg_cb

Method registers callback for functionality in _cb_dict (shared) or _cb_dproxy (not shared).

* update_cb

Method updates functionality callback in _cb_dict or _cb_dproxy.

Class CallBackProcessor
^^^^^^^^^^^^^^^^^^^^^^^

**Attributes** :

* _cbm - reference to CallBackManager
* _cb_dict - dictionary of callbacks
* _cb_dproxy - proxy dictionary of callbacks
* _current_cb - reference to current callback

**Methods** :

* __init__

Method sets _cbm, _cb_dict, _cb_dproxy.

* _wrap_fn

Method executes callback using synchronous or asynchronous handler.

* _wrap_fn_dproxy

Method executes callback using asynchronous handler.