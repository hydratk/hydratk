.. _tutor_hydra_tut1_cfg:

Tutorial 2: Configuration
=========================

Configuration file is stored in ``/etc/hydratk/hydratk.conf``.
It uses YAML hierarchical format which is friendly to read and change.

Some of configuration options will be show in examples.

  .. note::
 
     To get more info about remaining options check other tutorials and documentation.
     It is recommended to keep some options (especially Core) in default state without changing them.


Macros
^^^^^^

Configuration can be enhanced by implementation of simple macro strings, 
which can be used for dynamic data access and processing

* Basic syntax

Default implementation allows you to use following syntaxes:
 
Variable or function without parameters: ``$(var_name)``
Function with parameters: ``$(fn_name('param1','param2'...))``
 
There's also useful customization which implements dynamic access to the configuration structure
using ``$(GroupName.ItemName.option)``

  .. code-block:: yaml
  
     System:
       Language:
         id: en       

For example: the language id from the above example can accessed using ``$(System.Language.id)``

* Custom macros

Default macros are configured in the dictionary ``hydratk.core.confighooks.hook_list``

* Nested macros

Macro nesting is possible

For example: $(colorize('MY TEXT',$(rgb(248,248,248)))  


* Limitations

There're several limitations of this system, which you have to understand before you start using it, 
the reason behind is simple: lightweight and speed

 

1. There's no complex logic behind the parser for taking care about syntactical problems, 
   in general it means, if you create wrong macro, parser will not let you now.
   Same for the escaping function parameters and data types handling

2. Everything is string, it means that you have to take care about the macro input/output data types.
   If the callback function hidden behind the macro definition expects any other data type than string, you need to do 
   the conversion by yourself 

3. In current implementation you can't use as input/output in function parameter following characters: 
   left round bracket - (
   right round bracket - ( 
   If you need to use them, combine macros with string templates {}

Example:
  Not working:  $(colorize('DEBUG(1):','#808000')) 
  
  Working:      "$(colorize('DEBUG{lrb}1{rrb}:','#808000'))".format(lrb='(',rrb=')') 
     
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

Supported logging types are: Debug, Error, Warning, Exception

* Global configuration

Global configuration of logging types is defined in section ``System`` where you can turn it on/off

  .. code-block:: yaml
  
     Debug:
       enabled: 0
       level: 5
  
     Errors:
       enabled: 1

     Warnings:
       enabled: 1
   
     Exceptions:
       enabled: 1


* Logger
       
More specific logging of messages is covered by Logger feature in section ``Logger``.

By default there're pre-configured profiles for each logging type, each profile if bound to the specified output handler
with customized options, these options will override global configuration definitions

Profile basic options: 
  enabled: [0/1] disabled/enabled
  log_type: [debug,error,warning,exception]
  output_handler: [screen,logfile]
  format: "message format"
  format_cache: [0/1] disabled/enabled - if the format definition contains config macros which returns static data, then is reasonable to turn it on 

You can use log type specific default string format variables and of course your own variables can be added by accessing ``dbg_msg_format_vars`` dict property 
Message format can be also mixed with config macros defined in ``hydratk.core.confighooks.hook_list``

Available basic format string vars:  
  log_type: all     {lrb}       : '('                                 
  log_type: all     {rrb}       : ')'
  log_type: all     {timestamp} : date format "%d/%m/%Y %H:%M:%S,ms"
  log_type: all     {shorttime} : date format "%H:%M:%S,ms"
  log_type: debug   {level}     : debug level,
  log_type: all     {file}      : code location file
  log_type: all     {line}      : code location line
  log_type: all     {module}    : code location module
  log_type: all     {callpath}  : code location call path
  log_type: all     {func}      : code location func - Class.method name if class is available otherwise function name
  log_type: all     {thrid}     : code location process/thread id
  log_type: all     {msg}       : message content
  log_type: debug   {channel}   : debug channel
  log_type: exception {extype}  : exception type	   
  log_type: exception {trace}   : exception traceback

Log type ``debug`` profile options:                 
  level: [number] debug level
  channel: [int,'str'...] defined list of custom numeric or string filters
       
Log output handler ``logfile`` profile options:
  missing_dir: [autocreate/manual] if the missing log directory structure can be handled by logger
  log_file: "log file path" 
                           
                                 
Currently there two native output handlers: ``screen and logfile`` for logging to the screen and log files

  .. code-block:: yaml
  
     Debug_Console:
       enabled: 1
       log_type: debug
	   level: 5
	   channel: [] 
	   output_handler: screen
	   format: "$(colorize('{timestamp}','#d7afaf')) $(colorize('DEBUG{lrb}{level}{rrb}:','#808000')) $(colorize('{callpath}.{func}:[{thrid}]:','#CC6600')) $(colorize('{msg}','#ffaf87'))"
	   format_cache: 1 #we can cache term colors from macros
  
	 Debug_LogFile:
	   enabled: 0
       log_type: debug
	   level: 5
	   channel: []       
	   output_handler: logfile
	   format: "{timestamp} DEBUG{lrb}{level}{rrb}: {callpath}.{func}:[{thrid}]: {msg}\n"
	   format_cache: 0  #nothing to cache
	   missing_dir: autocreate    
	   log_file: $(ConfigVariables.logs.debug_log) 
    
     Error_Console:
       enabled: 1
       log_type: error
       output_handler: screen     
       format: "$(colorize('{timestamp}','#d75f5f')) $(colorize('ERROR:','#af0000')) $(colorize('{callpath}:{func}:{thrid}:','#d70000')) $(colorize('{msg}','#ff5f87'))"
       format_cache: 1 #we can cache term colors from macros
    
     Error_LogFile:
       enabled: 0
       log_type: error
       output_handler: logfile     
       format: "{timestamp} ERROR: {callpath}:{func}:{thrid}: {msg}\n"
       format_cache: 0  #nothing to cache
       missing_dir: autocreate
       log_file: $(ConfigVariables.logs.error_log)  
    
     Exception_Console:
       enabled: 1
       log_type: exception
       output_handler: screen     
       format: "$(colorize('{timestamp}','#d7afd7')) $(colorize('EXCEPTION:','#8700af')) $(colorize('{extype}:[{thrid}]:','#800080')) $(colorize('{msg}','#af87d7'))\n$(colorize('{trace}','#d787ff'))"
       format_cache: 1 #we can cache term colors from macros
    
     Exception_LogFile:
       enabled: 0
       log_type: exception
       output_handler: logfile     
       format: "{timestamp} EXCEPTION: {extype}:[{thrid}]: {msg}\n{trace}"
       format_cache: 0  #nothing to cache
       missing_dir: autocreate
       log_file: $(ConfigVariables.logs.exception_log)   
     

     Warning_Console:
       enabled: 1
       log_type: warning
       output_handler: screen     
       format: "$(colorize('{timestamp}','#ffffaf')) $(colorize('WARNING:','#ffff00')) $(colorize('{callpath}:{func}:{thrid}:','#ffff5f')) $(colorize('{msg}','#ffff87'))"
       format_cache: 1 #we can cache term colors from macros
    
     Warning_LogFile:
       enabled: 0
       log_type: warning
       output_handler: logfile     
       format: "{timestamp} WARNING: {callpath}:{func}:{thrid}: {msg}\n"
       format_cache: 0  #nothing to cache
       missing_dir: autocreate
       log_file: $(ConfigVariables.logs.warning_log)

 

By default log messages are printed to console output using *_Console profiles 

 
* Debug

By default debugging is disabled (debug messages are not printed), set ``System.Debug.enabled: 1`` to turn it on, 
then custom profiles explained above will be used

Another possible option is to override configuration by command option ``-d <level>``.
  

         
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