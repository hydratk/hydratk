.. _module_hydra_core_debugger:

debugger
========

This sections contains module documentation of debugger module.

debugger
^^^^^^^^

Module provides class Debugger.
Unit tests available at hydratk/core/debugger/01_methods_ut.jedi

**Attributes** :

* _debug - bool, debugging enabled
* _debug_level - number, level
* _debug_channel - list of channels
* _debug_channel_map - debug levels mapped to channels

**Methods** :

* fromhere

Method returns location of executed code (file, module, function, line, call path).

* function

Method returns name of executed function.

* file

Method returns name of executed file.

* line

Method returns name of executed line.

* module

Method returns name of executed module.

* errmsg

Method prints error message.

* dmsg

Method fires debug event.

* match_channel

Method checks if given channel is registered in _debug_channels.

* dout

Method prints debug message if message level is at least less or equal to debug level and debug channel is registered.
Method also supports metadata to localize executed code.

* wout

Method prints warning message.

* errout

Method prints error message.

* exout

Method prints exception traceback.