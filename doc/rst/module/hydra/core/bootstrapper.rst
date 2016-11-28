.. _module_hydra_core_bootstrapper:

bootstrapper
============

This sections contains module documentation of bootstrapper module.

bootstrapper
^^^^^^^^^^^^

Module provides bootstrapper for htk command (i.e. installed to /usr/local/bin/htk). 
Unit tests available at hydratk/core/bootstrapper/01_methods_ut.jedi

**Methods** :

* _check_dependencies

Method checks if all required modules are installed.

* run_app

Method handles command htk. It checks dependencies, creates MasterHead instance and runs h_bootstrap hook.

* run_app_prof

Method handles command htk-prof and runs hydratk in profiling mode (planned for future).