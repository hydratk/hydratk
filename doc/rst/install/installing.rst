.. _install_inst:

Installing
==========

You have 2 options how to install HydraTK.

Package
^^^^^^^

Install it via Python package managers PIP or easy_install.

  .. code-block:: bash
  
     $ sudo pip install --no-binary :all: hydratk
     
  .. code-block:: bash
  
     $ sudo easy_install hydratk
     
  .. note::
  
     PIP needs option --no-binary to run setup.py install.
     Otherwise it runs setup.py bdist_wheel.

Source
^^^^^^

Download the source code from GitHub or PyPi and install it manually.
Full PyPi URL contains MD5 hash, adapt sample code.

  .. code-block:: bash
  
     $ git clone https://github.com/hydratk/hydratk.git
     $ cd ./hydratk
     $ sudo python setup.py install
     
  .. code-block:: bash
  
     $ wget https://pypi.python.org/pypi/hydratk -O hydratk.tar.gz
     $ tar -xf hydratk.tar.gz
     $ cd ./hydratk
     $ sudo python setup.py install
     
  .. note::
  
     Source is distributed with Sphinx (not installed automatically) documentation in directory doc. 
     Type make html to build local documentation however is it recommended to use up to date online documentation.
     
Requirements
^^^^^^^^^^^^

Several python modules are used.
These modules will be installed automatically, if not installed yet (for Python 2.7).

* psutil
* pyyaml
* pyzmq
* setproctitle
* xtermcolor

Modules setproctitle, psutil, pyzmq require several libraries which will be installed via Linux package managers, if not installed yet.

setprocitle

* apt-get: gcc, wget, tar, bzip2, python-dev
* yum: gcc, wget, tar, bzip2, redhat-rpm-config, python-devel       
    
pyzmq

* apt-get: g++, libzmq-dev
* yum: gcc-c++, zeromq    

  .. note::
     
     Installation for Python 2.6 has some differences.
     Module importlib is automatically installed, it is part of standard distribution since 2.7.
     Library python2.6-dev or python2.6-devel is installed instead of python-dev.
     
  .. note::
  
     Installation for Python 3 has some differences.
     Library python3-dev or python3-devel is installed instead of python-dev.
    
Installation
^^^^^^^^^^^^

See installation example for Linux based on Debian distribution, Python 2.7. 

  .. note::
  
     The system is clean therefore external libraries will be also installed (several MBs will be downloaded)
     You can see strange log messages which are out of hydratk control. 
     
  .. code-block:: bash
  
     **************************************
     *     Running pre-install tasks      *
     **************************************
     
     *** Running task: version_update ***
     
     *** Running task: install_libs ***
     Checking gcc...FAILED
        Required gcc compiler not found in path
     Checking tar...OK
     Checking g++...FAILED
        Required g++ compiler not found in path
     Checking wget...OK
     Checking bzip2...OK
     Checking python-dev...FAILED
        Unable to locate package python-dev
     Checking libzmq-dev...FAILED
        Unable to locate shared library libzmq
     Installing package gcc
     Installing package g++
     Installing package python-dev
     Installing package libzmq-dev
     
     *** Running task: install_modules ***
     Installing module setproctitle>=1.1.9
     pip install "setproctitle>=1.1.9"
     Installing module pyzmq>=14.7.0
     pip install "pyzmq>=14.7.0"
     Installing module psutil>=3.1.1
     pip install "psutil>=3.1.1"
     Installing module pyyaml>=3.11
     pip install "pyyaml>=3.11"
     Installing module xtermcolor>=1.3
     pip install "xtermcolor>=1.3"
     
     running install
     running bdist_egg
     running egg_info
     creating src/hydratk.egg-info
     writing src/hydratk.egg-info/PKG-INFO
     writing top-level names to src/hydratk.egg-info/top_level.txt
     writing dependency_links to src/hydratk.egg-info/dependency_links.txt
     writing entry points to src/hydratk.egg-info/entry_points.txt
     writing manifest file 'src/hydratk.egg-info/SOURCES.txt'
     reading manifest file 'src/hydratk.egg-info/SOURCES.txt'
     reading manifest template 'MANIFEST.in'
     writing manifest file 'src/hydratk.egg-info/SOURCES.txt'
     installing library code to build/bdist.linux-x86_64/egg
     running install_lib
     running build_py
     creating build
     creating build/lib.linux-x86_64-2.7
     creating build/lib.linux-x86_64-2.7/hydratk
     ...
     creating dist
     creating 'dist/hydratk-0.5.0rc1-py2.7.egg' and adding 'build/bdist.linux-x86_64/egg' to it
     removing 'build/bdist.linux-x86_64/egg' (and everything under it)
     Processing hydratk-0.5.0rc1-py2.7.egg
     creating /usr/local/lib/python2.7/dist-packages/hydratk-0.5.0rc1-py2.7.egg
     Extracting hydratk-0.5.0rc1-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding hydratk 0.5.0rc1 to easy-install.pth file
     Installing htkprof script to /usr/local/bin
     Installing htk script to /usr/local/bin
     Installing htkuninstall script to /usr/local/bin  
     Installed /usr/local/lib/python2.7/dist-packages/hydratk-0.5.0rc1-py2.7.egg
     Processing dependencies for hydratk==0.5.0rc1
     Finished processing dependencies for hydratk==0.5.0rc1
     
     **************************************
     *     Running post-install tasks     *
     **************************************

     *** Running task: set_config ***

     Creating directory /etc/hydratk
     Copying file etc/hydratk/hydratk.conf to /etc/hydratk

     *** Running task: create_dirs ***

     Creating directory /var/local/hydratk/dbconfig

     *** Running task: set_access_rights ***

     Setting rights a+rwx for /var/local/hydratk
     Setting rights a+r for /etc/hydratk

     *** Running task: set_manpage ***        

     
Application installs following (paths depend on your OS configuration)

* commands htk, htkprof, htkuninstall in /usr/local/bin
* modules in /usr/local/lib/python2.7/dist-packages/hydratk-0.5.0-py2.7egg
* configuration file in /etc/hydratk/hydratk.conf
* application folder in /var/local/hydratk        

Run
^^^

When installation is finished you can run the application.

Check hydratk module is installed.

  .. code-block:: bash
  
     $ pip list | grep hydratk
     
     hydratk (0.5.0)

Type command htk and simple info is displayed.

  .. code-block:: bash
  
     $ htk
  
     HydraTK v0.5.0
     (c) 2009 - 2017 Petr Czaderna <pc@hydratk.org>, HydraTK team <team@hydratk.org>
     Usage: htk [options] command
     For list of the all available commands and options type htk help

     
Type command htk help and detailed info is displayed.
Type man htk to display manual page. 

  .. code-block:: bash
  
     $ htk help
     
     HydraTK v0.5.0
     (c) 2009 - 2017 Petr Czaderna <pc@hydratk.org>, HydraTK team <team@hydratk.org>
     Usage: htk [options] command

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
        -h, --home - sets htk_root_dir to the current user home directory
        -i, --interactive - turns on interactive mode
        -l, --language <language> - sets the text output language, the list of available languages is specified in the docs
        -m, --run-mode <mode> - sets the running mode, the list of available modes is specified in the docs
  
        
Type command htk -d 1 start and see debug log.

  .. code-block:: bash
  
     htk -d 1 start    
     

     [17/11/2016 16:13:20.444] Debug(1): hydratk.core.masterhead:check_debug:0: Debug level set to 1
     [17/11/2016 16:13:20.445] Debug(1): hydratk.core.corehead:_apply_config:0: Language set to 'English'
     [17/11/2016 16:13:20.445] Debug(1): hydratk.core.corehead:_import_global_messages:0: Trying to to load global messages for language 'en', package 'hydratk.translation.core.en.messages'
     [17/11/2016 16:13:20.446] Debug(1): hydratk.core.corehead:_import_global_messages:0: Global messages for language en, loaded successfully
     [17/11/2016 16:13:20.447] Debug(1): hydratk.core.corehead:_import_global_messages:0: Trying to to load global help for language en, package 'hydratk.translation.core.en.help'
     [17/11/2016 16:13:20.448] Debug(1): hydratk.core.corehead:_import_global_messages:0: Global help for language en, loaded successfully
     [17/11/2016 16:13:20.448] Debug(1): hydratk.core.corehead:_apply_config:0: Run mode set to '1 (CORE_RUN_MODE_SINGLE_APP)'
     [17/11/2016 16:13:20.449] Debug(1): hydratk.core.corehead:_apply_config:0: Main message router id set to 'raptor01'
     [17/11/2016 16:13:20.45] Debug(1): hydratk.core.corehead:_apply_config:0: Number of core workers set to: 4
     [17/11/2016 16:13:20.45] Debug(1): hydratk.core.corehead:_load_extension:0: Loading internal extension: 'BenchMark'
     [17/11/2016 16:13:20.451] Debug(1): hydratk.core.corehead:_import_extension_messages:0: Trying to to load extension messages for language en, package 'hydratk.extensions.benchmark.translation.en.messages'
     [17/11/2016 16:13:20.452] Debug(1): hydratk.core.corehead:_import_extension_messages:0: Extensions messages for language en, loaded successfully
     [17/11/2016 16:13:20.453] Debug(1): hydratk.core.corehead:_import_extension_messages:0: Trying to to load extension help for language en, package 'hydratk.extensions.benchmark.translation.en.help'
     [17/11/2016 16:13:20.453] Debug(1): hydratk.core.corehead:_load_extension:0: Internal extension: 'BenchMark v0.1.0 (c) [2013 - 2016 Petr Czaderna <pc@hydratk.org>]' loaded successfully
     [17/11/2016 16:13:20.454] Debug(1): hydratk.core.corehead:_load_extensions:0: Finished loading internal extensions
     [17/11/2016 16:13:20.456] Debug(1): hydratk.core.corehead:_start_app:0: Starting application
     [17/11/2016 16:13:20.457] Debug(1): hydratk.core.corehead:_init_message_router:0: Message Router 'raptor01' initialized successfully
     [17/11/2016 16:13:20.457] Debug(1): hydratk.core.corehead:_c_observer:0: Core message service 'c01' registered successfully
     [17/11/2016 16:13:20.458] Debug(1): hydratk.core.corehead:_c_observer:0: Core message queue '/tmp/hydratk/core.socket' initialized successfully
     [17/11/2016 16:13:20.459] Debug(1): hydratk.core.corehead:_c_observer:0: Starting to observe
     [17/11/2016 16:13:20.459] Debug(1): hydratk.core.corehead:_c_observer:0: Saving PID 8222 to file: /tmp/hydratk/hydratk.pid
     [17/11/2016 16:13:20.462] Debug(1): hydratk.core.masterhead:add_core_thread:0: Initializing core thread id: 1
     [17/11/2016 16:13:20.464] Debug(1): hydratk.core.masterhead:add_core_thread:0: Initializing core thread id: 2
     [17/11/2016 16:13:20.466] Debug(1): hydratk.core.masterhead:add_core_thread:0: Initializing core thread id: 3
     [17/11/2016 16:13:20.47] Debug(1): hydratk.core.masterhead:add_core_thread:0: Initializing core thread id: 4
     [17/11/2016 16:13:20.474] Debug(1): hydratk.core.corehead:_c_worker:1: Core message queue '/tmp/hydratk/core.socket' connected successfully
     [17/11/2016 16:13:20.485] Debug(1): hydratk.core.corehead:_c_worker:1: Starting to work
     [17/11/2016 16:13:20.489] Debug(1): hydratk.core.corehead:_c_worker:3: Core message queue '/tmp/hydratk/core.socket' connected successfully
     [17/11/2016 16:13:20.48] Debug(1): hydratk.core.corehead:_c_worker:2: Core message queue '/tmp/hydratk/core.socket' connected successfully
     [17/11/2016 16:13:20.49] Debug(1): hydratk.core.corehead:_c_worker:2: Starting to work
     [17/11/2016 16:13:20.491] Debug(1): hydratk.core.corehead:_c_worker:3: Starting to work
     [17/11/2016 16:13:20.493] Debug(1): hydratk.core.corehead:_c_worker:4: Core message queue '/tmp/hydratk/core.socket' connected successfully
     [17/11/2016 16:13:20.494] Debug(1): hydratk.core.corehead:_c_worker:4: Starting to work
     [17/11/2016 16:13:30.522] Debug(1): hydratk.core.corehead:_check_cw_activity:0: Checking live status on thread: 1, last activity before: 0.0770130157471
     [17/11/2016 16:13:30.525] Debug(1): hydratk.core.corehead:_check_cw_activity:0: Checking live status on thread: 2, last activity before: 0.0612938404083
     [17/11/2016 16:13:30.528] Debug(1): hydratk.core.corehead:_check_cw_activity:0: Checking live status on thread: 3, last activity before: 0.0646958351135
     [17/11/2016 16:13:30.531] Debug(1): hydratk.core.corehead:_check_cw_activity:0: Checking live status on thread: 4, last activity before: 0.0701160430908
        
Upgrade
=======

Use same procedure as for installation. Use command option --upgrade for pip, easy_install, --force for setup.py.
If configuration file differs from default settings the file is backuped (extension _old) and replaced by default. Adapt the configuration if needed.

Uninstall
=========    

Run command htkuninstall. Use option -y if you want to uninstall also dependent Python modules (for advanced user).    