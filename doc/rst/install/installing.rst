.. _install_inst:

Installing
==========

You have 2 options how to install HydraTK.

.. _install_inst_pip:

PIP
^^^

Install it via Python package manager PIP

  .. code-block:: bash
  
     $ sudo pip install hydratk 

.. _install_inst_github:

GitHub
^^^^^^

Download the source code from GitHub and install it manually.

  .. code-block:: bash
  
     $ git clone https://git.hydratk.org/hydratk.git
     $ cd ./hydratk
     $ sudo python setup.py install
     
.. _install_inst_run:

Run
^^^

When installation is finished you can run the application.

Check hydratk module is installed.

  .. code-block:: bash
  
     $ pip list | grep hydratk
     hydratk (0.3.0)

Type command htk and simple info is displayed.

  .. code-block:: bash
  
     $ htk
  
     HydraTK v0.3.0
     (c) 2009 - 2016 Petr Czaderna <pc@hydratk.org>, HydraTK Team
     Usage: /usr/local/bin/htk [options] command
     For list of the all available commands and options type /usr/local/bin/htk help
     
Type command htk help and detailed info is displayed.

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
        start-benchmark - starts benchmark
           Options:
              --details - displays detailed information about tests

        stop - stops the application

     Global Options:
        -c, --config <file> - reads the alternate configuration file
        -d, --debug <level> - debug turned on with specified level > 0
        -e, --debug-channel <channel number, ..> - debug channel filter turned on
        -f, --force - enforces command
        -i, --interactive - turns on interactive mode
        -l, --language <language> - sets the text output language, the list of available languages is specified in the docs
        -m, --run-mode <mode> - sets the running mode, the list of available languages is specified in the docs     
        
Type command htk -d 1 start and see debug log.

  .. code-block:: bash
  
     htk -d 1 start    
     
     [12/05/2016 10:25:01.459] Debug(1): hydratk.core.masterhead:check_debug:0: Debug level set to 1
     [12/05/2016 10:25:01.460] Debug(1): hydratk.core.corehead:_apply_config:0: Language set to 'English'
     [12/05/2016 10:25:01.460] Debug(1): hydratk.core.corehead:_import_global_messages:0: Trying to to load global messages for language 'en', package 'hydratk.translation.core.en.messages'
     [12/05/2016 10:25:01.461] Debug(1): hydratk.core.corehead:_import_global_messages:0: Global messages for language en, loaded successfully
     [12/05/2016 10:25:01.462] Debug(1): hydratk.core.corehead:_import_global_messages:0: Trying to to load global help for language en, package 'hydratk.translation.core.en.help'
     [12/05/2016 10:25:01.462] Debug(1): hydratk.core.corehead:_import_global_messages:0: Global help for language en, loaded successfully
     [12/05/2016 10:25:01.463] Debug(1): hydratk.core.corehead:_apply_config:0: Run mode set to '1 (CORE_RUN_MODE_SINGLE_APP)'
     [12/05/2016 10:25:01.464] Debug(1): hydratk.core.corehead:_import_global_messages:0: Trying to to load global messages for language 'en', package 'hydratk.translation.core.en.messages'
     [12/05/2016 10:25:01.464] Debug(1): hydratk.core.corehead:_import_global_messages:0: Global messages for language en, loaded successfully
     [12/05/2016 10:25:01.465] Debug(1): hydratk.core.corehead:_import_global_messages:0: Trying to to load global help for language en, package 'hydratk.translation.core.en.help'
     [12/05/2016 10:25:01.465] Debug(1): hydratk.core.corehead:_import_global_messages:0: Global help for language en, loaded successfully
     [12/05/2016 10:25:01.466] Debug(1): hydratk.core.corehead:_apply_config:0: Main message router id set to 'raptor01'
     [12/05/2016 10:25:01.467] Debug(1): hydratk.core.corehead:_apply_config:0: Number of core workers set to: 4
     [12/05/2016 10:25:01.535] Debug(1): hydratk.core.corehead:_load_extension:0: Loading internal extension: 'BenchMark'
     [12/05/2016 10:25:01.537] Debug(1): hydratk.core.corehead:_import_extension_messages:0: Trying to to load extension messages for language en, package 'hydratk.extensions.benchmark.translation.en.messages'
     [12/05/2016 10:25:01.538] Debug(1): hydratk.core.corehead:_import_extension_messages:0: Extensions messages for language en, loaded successfully
     [12/05/2016 10:25:01.539] Debug(1): hydratk.core.corehead:_import_extension_messages:0: Trying to to load extension help for language en, package 'hydratk.extensions.benchmark.translation.en.help'
     [12/05/2016 10:25:01.540] Debug(1): hydratk.core.corehead:_load_extension:0: Internal extension: 'BenchMark v0.1.0 (c) [2013 Petr Czaderna <pc@hydratk.org>]' loaded successfully
     [12/05/2016 10:25:01.575] Debug(1): hydratk.core.corehead:_start_app:0: Starting application
     [12/05/2016 10:25:01.576] Debug(1): hydratk.core.corehead:_init_message_router:0: Message Router 'raptor01' initialized successfully
     [12/05/2016 10:25:01.576] Debug(1): hydratk.core.corehead:_c_observer:0: Core message service 'c01' registered successfully
     [12/05/2016 10:25:01.578] Debug(1): hydratk.core.corehead:_c_observer:0: Core message queue '/tmp/hydratk/core.socket' initialized successfully
     [12/05/2016 10:25:01.579] Debug(1): hydratk.core.corehead:_c_observer:0: Starting to observe
     [12/05/2016 10:25:01.579] Debug(1): hydratk.core.corehead:_c_observer:0: Saving PID 4298 to file: /tmp/hydratk/hydra.pid
     [12/05/2016 10:25:01.587] Debug(1): hydratk.core.masterhead:add_core_thread:0: Initializing core thread id: 1
     [12/05/2016 10:25:01.591] Debug(1): hydratk.core.masterhead:add_core_thread:0: Initializing core thread id: 2
     [12/05/2016 10:25:01.597] Debug(1): hydratk.core.masterhead:add_core_thread:0: Initializing core thread id: 3
     [12/05/2016 10:25:01.608] Debug(1): hydratk.core.masterhead:add_core_thread:0: Initializing core thread id: 4
     
Application installs following (paths depend on your OS configuration)

* htk command in /usr/local/bin/htk
* modules in /usr/local/lib/python2.7/dist-packages/hydratk-0.3.0-py2.7egg
* configuration file in /etc/hydratk/hydratk.conf
* application folder in /var/local/hydratk         