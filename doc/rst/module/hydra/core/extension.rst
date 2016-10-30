.. _module_hydra_core_extension:

extension
=========

This sections contains module documentation of extension module.

extension
^^^^^^^^^

Method provides class Extension as base extension class.
Unit tests available at hydratk/core/extension/01_methods_ut.jedi

**Attributes** :

* _ext_id
* _ext_name
* _ext_version
* _ext_author
* _ext_year
* _mh - reference to MasterHead

**Methods** :

* __init__

Method sets extension using method _init_extension.
There are three optional method which are executed if extension class implements them (_check_dependencies, _do_imports, _register_actions).

* get_ext_name

Method returns _ext_name.

* get_ext_version

Method returns _ext_version.

* get_ext_author

Method returns _ext_author.

* get_ext_info

Method returns summary info about extension (name, version, year, author).