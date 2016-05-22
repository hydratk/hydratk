.. _tutor_hydra_tut1_cli:

Tutorial 1: Command line
========================

HydraTK provides command line interface. 
After installation new command ``htk`` appears on path (i.e. /usr/local/bin/htk)

Short help
^^^^^^^^^^

Type ``htk`` and short help is displayed.
 
  .. code-block:: bash

     $ htk
   
     HydraTK v0.3.0
     (c) 2009 - 2016 Petr Czaderna <pc@hydratk.org>, HydraTK Team
     Usage: /usr/local/bin/htk [options] command
     For list of the all available commands and options type /usr/local/bin/htk help 
   
Detailed help
^^^^^^^^^^^^^   
   
Execute command ``help`` and detailed help is displayed.
You see all available commands and options. Some of them will be shown in examples.

  .. code-block:: bash

     $ htk help
   
     HydraTK v0.3.0
     (c) 2009 - 2016 Petr Czaderna <pc@hydratk.org>, HydraTK Team
     Usage: /usr/local/bin/htk [options] command

     Commands:
        create-config-db - creates configuration database
           Options:
              --config-db-file <file> - optional, database file path

        create-ext-skel - creates project skeleton for HydraTK extension development
           Options:
              --ext-skel-path <path> - optional, directory path where HydraTK extension skeleton will be created

        create-lib-skel - creates project skeleton for HydraTK library development
           Options:
              --lib-skel-path <path> - optional, directory path where HydraTK library skeleton will be created

        help - prints help
        list-extensions - displays list of loaded extensions
        start - starts the application
        stop - stops the application

     Global Options:
        -c, --config <file> - reads the alternate configuration file
        -d, --debug <level> - debug turned on with specified level > 0
        -e, --debug-channel <channel number, ..> - debug channel filter turned on
        -f, --force - enforces command
        -i, --interactive - turns on interactive mode
        -l, --language <language> - sets the text output language, the list of available languages is specified in the docs
        -m, --run-mode <mode> - sets the running mode, the list of available languages is specified in the docs   
      
  .. note::
 
     To get more info about remaining commands and options check other tutorials and documentation.
      
Extensions
^^^^^^^^^^
 
Execute command ``list-extensions`` to see all installed extensions.
 
  .. code-block:: bash
  
     $ htk list-extensions
    
     BenchMark: BenchMark v0.1.0 (c) [2013 Petr Czaderna <pc@hydratk.org>]
    
BenchMark extension is distributed together with HydraTK. Other extensions need to be installed separately.

For example if you install TrackApps extension, 2 extensions will be shown.

  .. code-block:: bash

     $ htk list-extensions
   
     TrackApps: TrackApps v0.1.0 (c) [2016 Petr Rašek <bowman@hydratk.org>]
     BenchMark: BenchMark v0.1.0 (c) [2013 Petr Czaderna <pc@hydratk.org>]
     
If extension provides own commands, they are listed in detailed help.

  .. code-block:: bash
  
     $ htk help
     
     HydraTK v0.3.0
     (c) 2009 - 2016 Petr Czaderna <pc@hydratk.org>, HydraTK Team
     Usage: /usr/local/bin/htk [options] command

     Commands:
        start-benchmark - starts benchmark
           Options:
              --details - displays detailed information about tests
     
Startup and shutdown
^^^^^^^^^^^^^^^^^^^^

Execute command ``start`` to initialize Hydra process.
Switch ``-d 1`` turns on debugging, otherwise no output is printed.

  .. code-block:: bash
  
     $ htk -d 1 start
     
     [13/05/2016 17:29:12.748] Debug(1): hydratk.core.masterhead:check_debug:0: Debug level set to 1
     [13/05/2016 17:29:12.749] Debug(1): hydratk.core.corehead:_apply_config:0: Language set to 'English'
     [13/05/2016 17:29:12.749] Debug(1): hydratk.core.corehead:_import_global_messages:0: Trying to to load global messages for language 'en', package 'hydratk.translation.core.en.messages'
     [13/05/2016 17:29:12.749] Debug(1): hydratk.core.corehead:_import_global_messages:0: Global messages for language en, loaded successfully
     [13/05/2016 17:29:12.749] Debug(1): hydratk.core.corehead:_import_global_messages:0: Trying to to load global help for language en, package 'hydratk.translation.core.en.help'
     [13/05/2016 17:29:12.750] Debug(1): hydratk.core.corehead:_import_global_messages:0: Global help for language en, loaded successfully
     [13/05/2016 17:29:12.750] Debug(1): hydratk.core.corehead:_apply_config:0: Run mode set to '1 (CORE_RUN_MODE_SINGLE_APP)'
     [13/05/2016 17:29:12.750] Debug(1): hydratk.core.corehead:_import_global_messages:0: Trying to to load global messages for language 'en', package 'hydratk.translation.core.en.messages'
     [13/05/2016 17:29:12.751] Debug(1): hydratk.core.corehead:_import_global_messages:0: Global messages for language en, loaded successfully
     [13/05/2016 17:29:12.751] Debug(1): hydratk.core.corehead:_import_global_messages:0: Trying to to load global help for language en, package 'hydratk.translation.core.en.help'
     [13/05/2016 17:29:12.751] Debug(1): hydratk.core.corehead:_import_global_messages:0: Global help for language en, loaded successfully
     [13/05/2016 17:29:12.751] Debug(1): hydratk.core.corehead:_apply_config:0: Main message router id set to 'raptor01'
     [13/05/2016 17:29:12.752] Debug(1): hydratk.core.corehead:_apply_config:0: Number of core workers set to: 4
     [13/05/2016 17:29:12.752] Debug(1): hydratk.core.corehead:_load_extension:0: Loading internal extension: 'BenchMark'
     [13/05/2016 17:29:12.754] Debug(1): hydratk.core.corehead:_import_extension_messages:0: Trying to to load extension messages for language en, package 'hydratk.extensions.benchmark.translation.en.messages'
     [13/05/2016 17:29:12.756] Debug(1): hydratk.core.corehead:_import_extension_messages:0: Extensions messages for language en, loaded successfully
     [13/05/2016 17:29:12.756] Debug(1): hydratk.core.corehead:_import_extension_messages:0: Trying to to load extension help for language en, package 'hydratk.extensions.benchmark.translation.en.help'
     [13/05/2016 17:29:12.757] Debug(1): hydratk.core.corehead:_load_extension:0: Internal extension: 'BenchMark v0.1.0 (c) [2013 Petr Czaderna <pc@hydratk.org>]' loaded successfully
     [13/05/2016 17:29:12.757] Debug(1): hydratk.core.corehead:_load_extensions:0: Finished loading internal extensions
     [13/05/2016 17:29:12.758] Debug(1): hydratk.core.corehead:_start_app:0: Starting application
     [13/05/2016 17:29:12.758] Debug(1): hydratk.core.corehead:_init_message_router:0: Message Router 'raptor01' initialized successfully
     [13/05/2016 17:29:12.758] Debug(1): hydratk.core.corehead:_c_observer:0: Core message service 'c01' registered successfully
     [13/05/2016 17:29:12.760] Debug(1): hydratk.core.corehead:_c_observer:0: Core message queue '/tmp/hydratk/core.socket' initialized successfully
     [13/05/2016 17:29:12.761] Debug(1): hydratk.core.corehead:_c_observer:0: Starting to observe
     [13/05/2016 17:29:12.761] Debug(1): hydratk.core.corehead:_c_observer:0: Saving PID 3597 to file: /tmp/hydratk/hydra.pid
     [13/05/2016 17:29:12.768] Debug(1): hydratk.core.masterhead:add_core_thread:0: Initializing core thread id: 1
     [13/05/2016 17:29:12.769] Debug(1): hydratk.core.masterhead:add_core_thread:0: Initializing core thread id: 2
     [13/05/2016 17:29:12.771] Debug(1): hydratk.core.masterhead:add_core_thread:0: Initializing core thread id: 3
     [13/05/2016 17:29:12.776] Debug(1): hydratk.core.masterhead:add_core_thread:0: Initializing core thread id: 4
     [13/05/2016 17:29:12.777] Debug(1): hydratk.core.corehead:_start_app:0: Starting application
     [13/05/2016 17:29:12.777] Debug(1): hydratk.core.corehead:_init_message_router:0: Message Router 'raptor01' initialized successfully
     [13/05/2016 17:29:12.781] Debug(1): hydratk.core.corehead:_c_worker:2: Core message queue '/tmp/hydratk/core.socket' connected successfully
     [13/05/2016 17:29:12.787] Debug(1): hydratk.core.corehead:_c_worker:1: Core message queue '/tmp/hydratk/core.socket' connected successfully
     [13/05/2016 17:29:12.788] Debug(1): hydratk.core.corehead:_c_worker:3: Core message queue '/tmp/hydratk/core.socket' connected successfully
     [13/05/2016 17:29:12.789] Debug(1): hydratk.core.corehead:_c_worker:3: Starting to work
     [13/05/2016 17:29:12.789] Debug(1): hydratk.core.corehead:_c_worker:1: Starting to work
     [13/05/2016 17:29:12.790] Debug(1): hydratk.core.corehead:_c_worker:2: Starting to work
     [13/05/2016 17:29:12.790] Debug(1): hydratk.core.corehead:_c_observer:0: Core message service 'c01' registered successfully
     [13/05/2016 17:29:12.791] Debug(1): hydratk.core.corehead:_c_worker:4: Core message queue '/tmp/hydratk/core.socket' connected successfully
     [13/05/2016 17:29:12.792] Debug(1): hydratk.core.corehead:_c_worker:4: Starting to work
     [13/05/2016 17:29:12.792] Debug(1): hydratk.core.corehead:_c_observer:0: Core message queue '/tmp/hydratk/core.socket' initialized successfully
     [13/05/2016 17:29:12.793] Debug(1): hydratk.core.corehead:_c_observer:0: Starting to observe     

  .. note::
  
     The processes only notify themselves without any useful actions.
     HydraTK is general toolkit and specific actions are implemented in extensions and libraries. 
     
You can check running processes. According to debug output, 5 processes were created (1 observer and 4 workers).

  .. code-block:: bash
  
     $ ps -aux | grep hydratk
     
     root      4243 25.5  1.4 1171148 29528 pts/2   Rl+  17:35   0:01 hydratk/c_observer                      
     root      4248  0.0  0.7 183448 14592 pts/2    Sl+  17:35   0:00 hydratk/core:1                          
     root      4249  0.0  0.7 183460 14604 pts/2    Sl+  17:35   0:00 hydratk/core:2                          
     root      4250  0.0  0.7 183472 14620 pts/2    Sl+  17:35   0:00 hydratk/core:3                          
     root      4255  0.0  0.7 183484 14648 pts/2    Sl+  17:35   0:00 hydratk/core:4              
     
Execute command ``stop`` to shutdown Hydra processes. 
It must be executed from second shell because the first one is blocked by running process.
 
  .. code-block:: bash
    
     $ htk stop
       
     [13/05/2016 17:29:16.798] Debug(1): hydratk.core.eventhandler:_ec_sig_handler:0: Retrived signal: SIGTERM
     [13/05/2016 17:29:17.191] Debug(1): hydratk.core.corehead:_stop_app:0: Stopping application

Debug
^^^^^

Commands can be executed in debug mode too see more info.
Use option ``-d <level>`` with required level, the minimum level is 1.

  .. note::
  
     Check documentation for different debug levels. 
     
Language
^^^^^^^^

HydraTK supports multiple language versions.
Use option ``-l <lang>`` with required language code.
Currently two languages are distributed: ``en`` (English as default), ``cs`` (Czech)

  .. code-block:: bash
  
     $ htk -l cs
     
     HydraTK v0.3.0
     (c) 2009 - 2016 Petr Czaderna <pc@hydratk.org>, HydraTK Team
     Použití: /usr/local/bin/htk [možnosti..] příkaz
     Pro zobrazení seznamu všech dostupných příkazů a možností zadej /usr/local/bin/htk help
     
     
  .. note::   
  
     Czech is core developers' native langugage :). 