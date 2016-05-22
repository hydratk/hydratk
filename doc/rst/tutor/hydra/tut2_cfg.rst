.. _tutor_hydra_tut1_cfg:

Tutorial 2: Configuration
=========================

Configuration file is stored in ``/etc/hydratk/hydratk.conf``.
It uses YAML hierarchical format which is friendly to read and change.

Some of configuration options will be show in examples.

  .. note::
 
     To get more info about remaining options check other tutorials and documentation.
     It is recommended to keep some options (especially Core) in default state without changing them.
     
Language
^^^^^^^^

Language is configured in section ``System``.
Currently two languages are supported: ``en`` (English as default), ``cs`` (Czech).
The settings is used as default but it can be overriden by command option ``-l <id>``.

  .. code-block:: yaml
  
     System:
       Language:
         id: en     
        
Logging
^^^^^^^

Log messages are configured in section ``System``.

By default log messages are printed to console output. 
It is possible to use also file output, configure directory (/var/log/hydratk by default)

  .. code-block:: yaml
  
     System:
       Logging:
         log_dir: /var/log/hydratk
         
There are four types of log message with separate but similar configuration section.      
    
* Debug

It is disabled (debug messages are not printed) by default, set ``enabled: 1`` to turn it on.
Output stream is configured by option ``output``, console output ``screen`` is used by default.
Other possible values are ``file`` (file output), ``both`` (console and file), ``none`` (no output).
Option ``level`` specifies debug level, 1 is minimum level. It is used as default but it can be 
overriden by command option ``-d <level>``.
  
  .. note::
  
     It is recommended to keep options ``channel``, ``format`` (message format), ``term_color``, log_file`` (filename) default. 

  .. code-block:: yaml
  
     System:
       Debug:
         enabled: 0
         output: screen 
         level: 1
         channel: [] 
         format: '{timestamp}Debug({level}): {callpath}:{func}:{thrid}: {msg}'
         term_color: '#CC6600'
         log_file: '{log_dir}/{environment_name}-debug.log'

* Error

Error messages are printed by default to console. Configuration is similar to debug messages.

  .. code-block:: yaml
  
     System:
       Errors:
         enabled: 1
         output: screen 
         term_color: '#FF0000'
         log_file: '{log_dir}/{environment_name}-error.log'

* Warning

Warning messages are printed by default to console. Configuration is similar to debug messages.

  .. code-block:: yaml
  
     System:
       Warnings:
         enabled: 1
         output: screen 
         term_color: '#FFFF00'
         log_file: '{log_dir}/{environment_name}-warning.log'
   
* Standard  

Standard messages are printed by default to console. Configuration is similar to debug messages. 
   
  .. code-block:: yaml 
   
     System:   
       ControlledOutput:
         enabled: 1
         output: screen 
         term_color: '#FFFFFF'
         log_file: '{log_dir}/{environment_name}:{thrid}-stdout.log'
         
Extensions
^^^^^^^^^^

Section ``Extensions`` is used to configure bundled extensions which are distributed together with HydraTK.
Custom extensions have own configuration file.

You can enable or disable extension here. To disable it set ``enabled: 0``. 

  .. code-block:: yaml
  
     Extensions:
       BenchMark:
         package: hydratk.extensions.benchmark
         module: benchmark
         enabled: 1               
         
  .. note::
  
     Remaining options are specified by developer and must be kept to load extension correctly.                    