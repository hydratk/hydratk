.. _module_hydra_core_elogger:

logger
======

This sections contains module documentation of logger module.

logger
^^^^^^

Module provides class Logger.
Unit tests available at hydratk/core/logger/01_methods_ut.jedi

**Attributes** :

* _emulate_print - print line break

**Methods** :

* spout

Method prints message including line break if enabled.

* _log_init_handlers

Method initialize default Logger output handlers.

* _log_init_msg_formaters

Method initialize default Logger output formaters.

* _log_init_profiles

Method loads active Logger profiles from config.

* _log_event

Method is transforming event data through the Logger profiles.

* _log_screen_handler

Method is default screen output handler implementation.

* _log_file_handler

Method is default logfile output handler implementation.

* log_rotate

Method rotates logfile to compressed archive.