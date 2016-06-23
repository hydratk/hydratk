.. install_ext_yoda:

Yoda
====

You have 2 options how to install Yoda extension.

PIP
^^^

Install it via Python package manager PIP

  .. code-block:: bash
  
     $ sudo pip install hydratk-ext-yoda 

GitHub
^^^^^^

Download the source code from GitHub and install it manually.

  .. code-block:: bash
  
     $ git clone https://git.hydratk.org/hydratk-ext-yoda.git
     $ cd ./hydratk-ext-yoda
     $ sudo python setup.py install
     
Installation
^^^^^^^^^^^^

See installation example.
The extension requires hydratk.

  .. code-block:: bash
  
     installing library code to build/bdist.linux-x86_64/egg
     running install_lib
     running build_py
     creating build
     creating build/lib.linux-x86_64-2.7
     creating build/lib.linux-x86_64-2.7/hydratk
     copying src/hydratk/__init__.py -> build/lib.linux-x86_64-2.7/hydratk
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
     
     installing package data to build/bdist.linux-x86_64/egg
     running install_data
     creating /etc/hydratk/conf.d
     copying etc/hydratk/conf.d/hydratk-ext-yoda.conf -> /etc/hydratk/conf.d
     creating /var/local/hydratk/yoda
     creating /var/local/hydratk/yoda/yoda-tests
     creating /var/local/hydratk/yoda/yoda-tests/test1
     copying var/local/hydratk/yoda/yoda-tests/test1/example1.yoda -> /var/local/hydratk/yoda/yoda-tests/test1
     creating /var/local/hydratk/yoda/helpers
     creating /var/local/hydratk/yoda/helpers/yodahelpers
     copying var/local/hydratk/yoda/helpers/yodahelpers/__init__.py -> /var/local/hydratk/yoda/helpers/yodahelpers
     creating /var/local/hydratk/yoda/lib
     creating /var/local/hydratk/yoda/lib/yodalib
     copying var/local/hydratk/yoda/lib/yodalib/__init__.py -> /var/local/hydratk/yoda/lib/yodalib
     creating build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_yoda.egg-info/PKG-INFO -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_yoda.egg-info/SOURCES.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_yoda.egg-info/dependency_links.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_yoda.egg-info/entry_points.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_yoda.egg-info/requires.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_yoda.egg-info/top_level.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     creating dist
     creating 'dist/hydratk_ext_yoda-0.2.1-py2.7.egg' and adding 'build/bdist.linux-x86_64/egg' to it
     removing 'build/bdist.linux-x86_64/egg' (and everything under it)
     Processing hydratk_ext_yoda-0.2.1-py2.7.egg
     creating /usr/local/lib/python2.7/dist-packages/hydratk_ext_yoda-0.2.1-py2.7.egg
     Extracting hydratk_ext_yoda-0.2.1-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding hydratk-ext-yoda 0.2.1 to easy-install.pth file
     Installing yoda script to /usr/local/bin

     Using /usr/local/lib/python2.7/dist-packages/setproctitle-1.1.10-py2.7-linux-x86_64.egg
     Finished processing dependencies for hydratk-ext-yoda==0.2.1
       
Run
^^^

When installation is finished you can run the application.

Check hydratk-ext-yoda module is installed.

  .. code-block:: bash
  
     $ pip list | grep hydratk
     
     hydratk (0.3.0a0.dev1)
     hydratk-ext-yoda (0.2.0)
    
Check installed extensions

  .. code-block:: bash
  
     $ htk list-extensions
     
     Yoda: Yoda v0.2.0 (c) [2014 - 2016 Petr Czaderna <pc@hydratk.org>]
     
Type command htk help and detailed info is displayed.

  .. code-block:: bash
  
     $ htk help
     
     Commands:
       yoda-create-test-results-db - creates database for storing test results base on specified dsn configuration
         Options:
           --yoda-db-results-dsn <dsn> - test results database access definition
           --yoda-test-repo-root-dir <path> - test repository root directory

       yoda-run - starts the Yoda tester
         Options:
           --yoda-db-results-dsn <dsn> - test results database access definition
           --yoda-test-path <path> - test scenario path
           --yoda-test-repo-root-dir <path> - test repository root directory
           --yoda-test-results-output-create <state> - activates/deactivates native test results output handler
           --yoda-test-run-name <name> - test run identification
           -a, --yoda-test-results-output-handler <type> - set the test results output handler type

       yoda-simul - starts the Yoda tester in test simulation mode
         Options:
           --yoda-db-results-dsn <dsn> - test results database access definition
           --yoda-test-path <path> - test scenario path
           --yoda-test-repo-root-dir <path> - test repository root directory
           --yoda-test-results-output-create <state> - activates/deactivates native test results output handler
           --yoda-test-run-name <name> - test run identification
           -a, --yoda-test-results-output-handler <type> - set the test results output handler type
                  
You can run Yoda also in standalone mode.

  .. code-block:: bash
  
     $ yoda help
     
     Yoda v0.2.0
     (c) 2014 - 2016 Petr Czaderna <pc@hydratk.org>
     Usage: /usr/local/bin/yoda [options] command

     Commands:
       create-test-results-db - creates database for storing test results base on specified dsn configuration
         Options:
           --db-results-dsn <dsn> - test results database access definition
           -tr, --test-repo-root-dir <path> - test repository root directory

       help - prints help
       run - starts the Yoda tester
         Options:
           --db-results-dsn <dsn> - test results database access definition
           -oc, --test-results-output-create <state> - activates/deactivates native test results output handler
           -oh, --test-results-output-handler <type> - set the test results output handler type
           -tn, --test-run-name <name> - test run identification
           -tp, --test-path <path> - test scenario path
           -tr, --test-repo-root-dir <path> - test repository root directory

       simul - starts the Yoda tester in test simulation mode
         Options:
           --db-results-dsn <dsn> - test results database access definition
           -oc, --test-results-output-create <state> - activates/deactivates native test results output handler
           -oh, --test-results-output-handler <type> - set the test results output handler type
           -tn, --test-run-name <name> - test run identification
           -tp, --test-path <path> - test scenario path
           -tr, --test-repo-root-dir <path> - test repository root directory

     Global Options:
       -c, --config <file> - reads the alternate configuration file
       -d, --debug <level> - debug turned on with specified level > 0
       -e, --debug-channel <channel number, ..> - debug channel filter turned on
       -f, --force - enforces command
       -i, --interactive - turns on interactive mode
       -l, --language <language> - sets the text output language, the list of available languages is specified in the docs
       -m, --run-mode <mode> - sets the running mode, the list of available languages is specified in the docs
                        
Application installs following (paths depend on your OS configuration)

* yoda command in /usr/local/bin/yoda
* modules in /usr/local/lib/python2.7/dist-packages/hydratk-ext-yoda-0.2.0-py2.7egg
* configuration file in /etc/hydratk/conf.d/hydratk-ext-yoda.conf 
* application folder in /var/local/hydratk/yoda                         