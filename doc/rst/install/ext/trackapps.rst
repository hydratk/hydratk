.. install_ext_trackapps:

TrackApps
=========

You have 2 options how to install TrackApps extension.

PIP
^^^

Install it via Python package manager PIP

  .. code-block:: bash
  
     $ sudo pip install hydratk-ext-trackapps 

GitHub
^^^^^^

Download the source code from GitHub and install it manually.

  .. code-block:: bash
  
     $ git clone https://git.hydratk.org/hydratk-ext-trackapps.git
     $ cd ./hydratk-ext-trackapps
     $ sudo python setup.py install
     
Installation
^^^^^^^^^^^^

See installation example.
The extension requires hydratk, hydratk-lib-network.

  .. code-block:: bash
  
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
     
     Installed /usr/local/lib/python2.7/dist-packages/hydratk_ext_trackapps-0.1.0-py2.7.egg
     Processing dependencies for hydratk-ext-trackapps==0.1.0
     Searching for hydratk-lib-network==0.1.0
     Best match: hydratk-lib-network 0.1.0
     Processing hydratk_lib_network-0.1.0-py2.7.egg
     hydratk-lib-network 0.1.0 is already the active version in easy-install.pth

     Using /usr/local/lib/python2.7/dist-packages/hydratk_lib_network-0.1.0-py2.7.egg
     Searching for hydratk==0.3.0a0.dev1
     Best match: hydratk 0.3.0a0.dev1
     Processing hydratk-0.3.0a0.dev1-py2.7.egg
     hydratk 0.3.0a0.dev1 is already the active version in easy-install.pth
     Using /usr/local/lib/python2.7/dist-packages/pycparser-2.14-py2.7.egg
     Finished processing dependencies for hydratk-ext-trackapps==0.1.0
       
Run
^^^

When installation is finished you can run the application.

Check hydratk-ext-trackapps module is installed.   

  .. code-block:: bash
  
     $ pip list | grep hydratk
     
     hydratk (0.3.0a0.dev1)
     hydratk-ext-trackapps (0.1.0)
     
Check installed extensions

  .. code-block:: bash
  
     $ htk list-extensions
     
     TrackApps: TrackApps v0.1.0 (c) [2016 Petr Rašek <bowman@hydratk.org>]
     
Type command htk help and detailed info is displayed.

  .. code-block:: bash
  
     $ htk help
     
     Commands:
       track - start trackapps command line extension
         Options:
           [--tr-dev-key <key>] - developer key, configurable, supported for app: testlink
           [--tr-domain <domain>] - domain, configurable, supported for app: qc
           [--tr-fields <list>] - requested fields, name1,name2,... , supported for action: read
           [--tr-id <num>] - record id, supported for actions: read|update|delete
           [--tr-input <filename>] - filename, content is written to ticket description, supported for actions: create|update
           [--tr-limit <num>] - limit, supported for action: read, apps: qc|bugzilla|jira
           [--tr-offset <num>] - offset, supported for action: read, apps: qc|bugzilla|jira
           [--tr-order-by <expression>] - record ordering, name1:direction,name2:direction,... , direction asc|desc, supported for action: read, app: qc
           [--tr-output <filename>] - filename, writes action output, supported for action: read
           [--tr-page <num>] - record page, supported for action: read, app: mantis
           [--tr-params <dict>] - record parameters, name1:value,name2:value,... , supported for actions: create|update
           [--tr-passw <password>] - password, configurable
           [--tr-path <path>] - directory path, dir1/dir2/... , supported for use cases: read/create folder|read/create test set|create test|read/create suite, apps: qc|testlink
           [--tr-per-page <num>] - records per page, supported for action: read, app: mantis
           [--tr-project <project>] - project, configurable, supported for apps: qc|mantis|trac|jira|testlink
           [--tr-query <expression>] - query, supported for action: read, apps: qc|bugzilla|trac|jira
           [--tr-steps <list>] - test steps delimited by |, step parameters use dictionary form, name1:value,name2:value,...|name1:value,name2:value,... , supported for action: create, app: testlink
           [--tr-type defect|test-folder|test|test-set-folder|test-set|test-instance|test-suite|test-plan|build] - entity type, default defect, supported for actions: read|create|update|delete, apps: qc|testlink
           [--tr-url <url>] - url, configurable
           [--tr-user <username>] - username, configurable
           --tr-action read|create|update|delete - action, delete supported for apps: qc|mantis|trac
           --tr-app qc|bugzilla|mantis|trac|testlink - application
           
You can run TrackApps also in standalone mode.

  .. code-block:: bash
  
     $ trackapps help
     
     TrackApps v0.1.0
     (c) 2016 Petr Rašek <bowman@hydratk.org>
     Usage: /usr/local/bin/trackapps [options] command

     Commands:
       help - prints help
       run - start testing environment
         Options:
           [--dev-key <key>] - developer key, configurable, supported for app: testlink
           [--domain <domain>] - domain, configurable, supported for app: qc
           [--fields <list>] - requested fields, name1,name2,... , supported for action: read
           [--id <num>] - record id, supported for actions: read|update|delete
           [--limit <num>] - limit, supported for action: read, apps: qc|bugzilla|jira
           [--offset <num>] - offset, supported for action: read, apps: qc|bugzilla|jira
           [--order-by <expression>] - record ordering, name1:direction,name2:direction,... , direction asc|desc, supported for action: read, app: qc
           [--page <num>] - record page, supported for action: read, app: mantis
           [--params <dict>] - record parameters, name1:value,name2:value,... , supported for actions: create|update
           [--passw <password>] - password, configurable
           [--path <path>] - directory path, dir1/dir2/... , supported for use cases: read/create folder|read/create test set|create test|read/create suite, apps: qc|testlink
           [--per-page <num>] - records per page, supported for action: read, app: mantis
           [--project <project>] - project, configurable, supported for apps: qc|mantis|trac|jira|testlink
           [--query <expression>] - query, supported for action: read, apps: qc|bugzilla|trac|jira
           [--steps <list>] - test steps delimited by |, step parameters use dictionary form, name1:value,name2:value,...|name1:value,name2:value,... , supported for action: create, app: testlink
           [--type defect|test-folder|test|test-set-folder|test-set|test-instance|test-suite|test-plan|build] - entity type, default defect, supported for actions: read|create|update|delete, apps: qc|testlink
           [--url <url>] - url, configurable
           [--user <username>] - username, configurable
           --app qc|bugzilla|mantis|trac|testlink - application

     Global Options:
       -c, --config <file> - reads the alternate configuration file
       -d, --debug <level> - debug turned on with specified level > 0
       -e, --debug-channel <channel number, ..> - debug channel filter turned on
       -f, --force - enforces command
       -i, --interactive - turns on interactive mode
       -l, --language <language> - sets the text output language, the list of available languages is specified in the docs
       -m, --run-mode <mode> - sets the running mode, the list of available languages is specified in the docs                

Application installs following (paths depend on your OS configuration)

* trackapps command in /usr/local/bin/trackapps
* modules in /usr/local/lib/python2.7/dist-packages/hydratk_ext_trackapps-0.1.0-py2.7.egg
* configuration file in /etc/hydratk/conf.d/hydratk-ext-trackapps.conf                   