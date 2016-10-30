.. _module_hydra_lib_translation:

translation
===========

This sections contains module documentation of translation modules.

translator
^^^^^^^^^^

Module provides class Translator.
Unit tests available at hydratk/lib/translation/translator/01_methods_ut.jedi

**Attributes** :

* _msg_mod
* _help_mod
* _language - cs, en
* _messages - langtexts dictionary
* _debug_level - debug level (default 1)

**Properties (Getters)** :

* msg_mod - returns _msg_mod
* help_mod - returns _help_mod

**Properties (Setters)** :

* msg_mod - sets _msg_mod
* help_mod - sets _help_mod

**Methods** :

* __init__

Method sets _messages.

* set_help_mod

Method sets _help_mod.

* register_messages

Method sets _messages.

* set_debug_level

Method sets _debug_level.

* set_language

Method sets _language.

* get_language

Method gets _language.

* lmsg

Method translates langtext to message.

* msg

Method translates langtext to message with given debug level.

* add_msg

Method sets langtexts for language.

* add_help

Method sets application help (commands, options) 

* lang_add_msg

Method add new langtext for given language.