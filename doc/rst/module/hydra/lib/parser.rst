.. _module_hydra_lib_parser:

parser
======

This sections contains module documentation of parser modules.

smp
^^^

Module provides class MacroParser.

**Attributes** :

* _mh
* _regexp
* _hooks
* _default_hook

**Methods** :

* __init__

Method sets regexp or default if not provided.

* add_regexp

Method adds regexp matches.

* add_var_hooks

Method registers hooks for macro variables.

* add_var_hook

Method registers hook for macro variable.

* set_default_var_hook

Method sets default hook.

* parse

Method parses macro string.

* _var_processor

Method executes macro string.

* _fn_processor

Method processes macro function.