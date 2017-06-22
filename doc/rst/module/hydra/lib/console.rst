.. _module_hydra_lib_console:

console
=======

This sections contains module documentation of console modules.

cmdoptparser
^^^^^^^^^^^^

Module provides class CmdOptParser inherited from argparse.ArgumentParser.
Unit tests available at hydratk/lib/console/cmdoptparser/01_methods_ut.jedi

**Attributes** :

* _silent
* _set_opts
* _unreg_opts
* _opt_group - default option group
* _options - dictionary of options which belong to option group

**Methods** :

* error

Method raises CmdOptParserError

* set_default_opt_group

Method sets _opt_group if configured in options. Otherwise it raises CmdOptParserUndefined.

* add_opt_group

Method sets new option group (new key in _options).

  .. code-block:: python
  
     from hydratk.lib.console.cmdoptparser import CmdOptParser
     
     op = CmdOptParser()
     group = 'test'
     op.add_opt_group(group)

* _add_opt

Methods sets new option for given group (automatically created if not set). If option already exists CmdOptParserError is raised.
Method can set single option or list. Option supports several configuration parameters.

d_option is target option (multiple option aliases can point to same target, can be used for short and long options).
has_value is used for options with expected value (False by default used for switches). allow_multiple is used for options
that can have multiple values (False by default for options with single value).

When you want to set list options you must specify the configuration [{'option':option, 'dest':d_option, 'action':action}].
action can be store_true (switches), store (single value), append (multiple values).

  .. code-block:: python
  
     # single option without value
     group, opt = 'test', '-x'
     res = op._add_opt(opt, opt_group=group)
     
     # single option with value
     d_opt, has_value, allow_multiple = 'x', True, False
     res = op._add_opt(opt, d_opt, has_value, allow_multiple, group)
     
     # option with multiples value
     allow_multiple = True
     res = op._add_opt(opt, d_opt, has_value, allow_multiple, group)
     
     # multiple options
     opt = []
     opt[0] = {'option': options[0], 'dest': 'x', 'action': 'store'}
     opt[1] = {'option': options[1], 'dest': 'y', 'action': 'store'}
     res = op._add_opt(opt, opt_group=group)  
     
* add_opt

Method is simplified interface for method _add_opt.
                 
commandlinetool
^^^^^^^^^^^^^^^

Module provides class CommandlineTool with static methods for operation with command line.
Unit tests available at hydratk/lib/console/commandlinetool/01_methods_ut.jedi                 

**Attributes** :

* _title - help title
* _cp_string - copyright
* _commands - list of commands
* _long_opt - list of long options
* _short_opt - list of short options
* _cmd_text - help for commands
* _opt_text - help for options
* _trn - reference to Translator
* _parser

**Methods** :

* set_translator

Method sets _trn, reference to Translator.

* set_possible_commands

Method sets _commands.

* set_possible_options

Method sets _long_opt, _short_opt.

* set_help

Method sets attributes for help (_title, _cp_string, _cmd_text, _opt_text).

* print_short_help

Method prints help in short form using method create_short_help.

* print_help

Method prints help in long form using method create_help.

* get_command_options_desc

Method returns options description for given command.

* get_input_command

Method checks if passed command (in sys.argv) is registered in _commands.

* create_short_help

Method prepares help in short form (default output when no command is provided).

* create_help

Method prepares in help in long form (output for command help). list of commands and their options including description.

* parse_shell_text

Method formats text to be printed. Special characters {h}, {u}, {e} are replaced by console highlighting.

shellexec
^^^^^^^^^

**Methods** :

* shell_exec

Method executes shell command and returns output.