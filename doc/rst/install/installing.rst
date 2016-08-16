.. _install_inst:

Installing
==========

You have 2 options how to install HydraTK.

Package
^^^^^^^

Install it via Python package managers PIP or easy_install.
Filename after PIP download contains version, adapt sample code.

  .. code-block:: bash
  
     $ sudo pip download hydratk
     $ sudo pip install hydratk.tar.gz 
     
  .. code-block:: bash
  
     $ sudo easy_install hydratk
     
  .. note::
  
     Use PIP to install package from local file for correct installation.
     When installed from remote repository, PIP sometimes doesn't call setup.py.

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

See installation example for Linux based on Debian distribution. 

  .. note::
  
     The system is clean therefore external libraries will be also installed (several MBs will be downloaded)
     You can see strange log messages which are out of hydratk control. 
     
  .. code-block:: bash
  
     **************************************
     *     Running pre-install tasks      *
     **************************************

     *** Running task: install_libs_from_repo ***

     Installing package g++
     Installing package libzmq-dev
     Installing package gcc
     Installing package wget
     Installing package bzip2
     Installing package tar
     Installing package python-dev
     running install
     running bdist_egg
     running egg_info
     writing requirements to src/hydratk.egg-info/requires.txt
     writing src/hydratk.egg-info/PKG-INFO
     writing top-level names to src/hydratk.egg-info/top_level.txt
     writing dependency_links to src/hydratk.egg-info/dependency_links.txt
     writing entry points to src/hydratk.egg-info/entry_points.txt
     reading manifest file 'src/hydratk.egg-info/SOURCES.txt'
     reading manifest template 'MANIFEST.in'
     writing manifest file 'src/hydratk.egg-info/SOURCES.txt'
     installing library code to build/bdist.linux-x86_64/egg
     running install_lib
     running build_py
     creating build
     creating build/lib.linux-x86_64-2.7
     creating build/lib.linux-x86_64-2.7/hydratk
     copying src/hydratk/__init__.py -> build/lib.linux-x86_64-2.7/hydratk
     ...
     
     byte-compiling build/bdist.linux-x86_64/egg/hydratk/__init__.py to __init__.pyc
     byte-compiling build/bdist.linux-x86_64/egg/hydratk/extensions/__init__.py to __init__.pyc
     ...
     
     copying src/hydratk.egg-info/PKG-INFO -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk.egg-info/SOURCES.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk.egg-info/dependency_links.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk.egg-info/entry_points.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk.egg-info/not-zip-safe -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk.egg-info/requires.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk.egg-info/top_level.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     creating dist
     creating 'dist/hydratk-0.3.0a0.dev4-py2.7.egg' and adding 'build/bdist.linux-x86_64/egg' to it
     removing 'build/bdist.linux-x86_64/egg' (and everything under it)
     Processing hydratk-0.3.0a0.dev4-py2.7.egg
     creating /usr/local/lib/python2.7/dist-packages/hydratk-0.3.0a0.dev4-py2.7.egg
     Extracting hydratk-0.3.0a0.dev4-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding hydratk 0.3.0a0.dev4 to easy-install.pth file
     Installing htkprof script to /usr/local/bin
     Installing htk script to /usr/local/bin
     Installed /usr/local/lib/python2.7/dist-packages/hydratk-0.3.0a0.dev4-py2.7.egg
     Processing dependencies for hydratk==0.3.0a0.dev4
     
     Searching for xtermcolor>=1.3
     Reading https://pypi.python.org/simple/xtermcolor/
     Best match: xtermcolor 1.3
     Downloading https://pypi.python.org/packages/65/46/c17b53f040396fb6bc0ee6afd0e809c12580791a61b801728708b48b6711/xtermcolor-1.3.tar.gz#md5=9f674649d431536a35b1cf911c44ce2c
     Processing xtermcolor-1.3.tar.gz
     Installed /usr/local/lib/python2.7/dist-packages/xtermcolor-1.3-py2.7.egg
     
     Searching for pyyaml>=3.11
     Reading https://pypi.python.org/simple/pyyaml/
     Best match: PyYAML 3.11
     Downloading https://pypi.python.org/packages/75/5e/b84feba55e20f8da46ead76f14a3943c8cb722d40360702b2365b91dec00/PyYAML-3.11.tar.gz#md5=f50e08ef0fe55178479d3a618efe21db
     Processing PyYAML-3.11.tar.gz   
     Installed /usr/local/lib/python2.7/dist-packages/PyYAML-3.11-py2.7-linux-x86_64.egg
     
     Searching for psutil>=3.1.1
     Reading https://pypi.python.org/simple/psutil/
     Best match: psutil 4.3.0
     Downloading https://pypi.python.org/packages/22/a8/6ab3f0b3b74a36104785808ec874d24203c6a511ffd2732dd215cf32d689/psutil-4.3.0.tar.gz#md5=ca97cf5f09c07b075a12a68b9d44a67d
     Processing psutil-4.3.0.tar.gz
     Installed /usr/local/lib/python2.7/dist-packages/psutil-4.3.0-py2.7-linux-x86_64.egg
     
     Searching for pyzmq>=14.7.0
     Reading https://pypi.python.org/simple/pyzmq/
     Best match: pyzmq 15.2.0
     Downloading https://pypi.python.org/packages/69/d8/5366d3ecb3907ea079483c38a7aa6c8902a44ca322ba2eece0d587707e2e/pyzmq-15.2.0.tar.gz#md5=9722046c27475441d47ac17a98c665bb
     Processing pyzmq-15.2.0.tar.gz
     Installed /usr/local/lib/python2.7/dist-packages/pyzmq-15.2.0-py2.7-linux-x86_64.egg
     
     Searching for setproctitle>=1.1.9
     Reading https://pypi.python.org/simple/setproctitle/
     Best match: setproctitle 1.1.10
     Downloading https://pypi.python.org/packages/8a/b9/058c53e8e55e9d549da8d60bbb7a404aac57b153c7cb815129d726c4cbbb/setproctitle-1.1.10.zip#md5=5002e26d06564000db1a45c801b615e9
     Processing setproctitle-1.1.10.zip
     Installed /usr/local/lib/python2.7/dist-packages/setproctitle-1.1.10-py2.7-linux-x86_64.egg
     
     Finished processing dependencies for hydratk==0.3.0a0.dev4
     **************************************
     *     Running post-install tasks     *
     **************************************

     *** Running task: copy_files ***

     Creating directory /etc/hydratk
     Copying file etc/hydratk/hydratk.conf to /etc/hydratk
     Creating directory /var/local/hydratk/dbconfig
     Copying file var/local/hydratk/dbconfig/__init__.py to /var/local/hydratk/dbconfig

     *** Running task: set_access_rights ***

     Setting rights a+rwx for /var/local/hydratk
     Setting rights a+r for /etc/hydratk  
     
Application installs following (paths depend on your OS configuration)

* htk command in /usr/local/bin/htk
* modules in /usr/local/lib/python2.7/dist-packages/hydratk-0.3.0-py2.7egg
* configuration file in /etc/hydratk/hydratk.conf
* application folder in /var/local/hydratk        

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