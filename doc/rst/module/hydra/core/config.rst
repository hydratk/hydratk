.. _module_hydra_core_config:

config
======

This sections contains module documentation of configuration module.

commandopt
^^^^^^^^^^

Configuration of commands and options.

* cmd - list of commands for htk group (create-config-db, create-ext-skel, create-lib-skel, start, stop, help, list-extensions)
* long_opt - list of long options for htk group
* short_opt - list of short options for htk group
* d_opt - target options for htk group (debug, config, config-db-file, debug-channel, ext-skel-path, force, interactive, language, lib-skel-path, run-mode)
* opt - configuration of short and long options for htk group (parameters d_opt, has_value, allow_multiple) 

commands
^^^^^^^^

Legacy configuration of commands, not used anymore.

const
^^^^^

Configuration of various constants used in application.

* metadata - name, version, year, authors
* default settings - configuration file, language, debug level
* run modes - list (single application, parallel)
* thread - list of statuses, time intervals
* run levels - list of run hierarchy levels
