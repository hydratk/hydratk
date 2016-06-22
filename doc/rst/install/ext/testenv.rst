.. install_ext_testenv:

TestEnv
=======

You have 2 options how to install TestEnv extension.

PIP
^^^

Install it via Python package manager PIP

  .. code-block:: bash
  
     $ sudo pip install hydratk-ext-testenv 

GitHub
^^^^^^

Download the source code from GitHub and install it manually.

  .. code-block:: bash
  
     $ git clone https://git.hydratk.org/hydratk-ext-testenv.git
     $ cd ./hydratk-ext-testenv
     $ sudo python setup.py install
     
Installation
^^^^^^^^^^^^

See installation example.
The extension requires modules web.py (automatically installed) and hydratk, hydratk-lib-network, hydratk-ext-yoda.     

  .. code-block:: bash
  
     installing library code to build/bdist.linux-x86_64/egg
     running install_lib
     running build_py
     creating build
     creating build/lib.linux-x86_64-2.7
     creating build/lib.linux-x86_64-2.7/hydratk
     copying src/hydratk/__init__.py -> build/lib.linux-x86_64-2.7/hydratk
     creating build/lib.linux-x86_64-2.7/hydratk/extensions
     copying src/hydratk/extensions/__init__.py -> build/lib.linux-x86_64-2.7/hydratk/extensions
     ...
     
     byte-compiling build/bdist.linux-x86_64/egg/hydratk/__init__.py to __init__.pyc
     byte-compiling build/bdist.linux-x86_64/egg/hydratk/extensions/__init__.py to __init__.pyc
     ...
     
     installing package data to build/bdist.linux-x86_64/egg
     running install_data
     copying etc/hydratk/conf.d/hydratk-ext-testenv.conf -> /etc/hydratk/conf.d
     creating /var/local/hydratk/testenv
     copying var/local/hydratk/testenv/install_db.sql -> /var/local/hydratk/testenv
     copying var/local/hydratk/testenv/crm.wsdl -> /var/local/hydratk/testenv
     copying var/local/hydratk/testenv/crm.xsd -> /var/local/hydratk/testenv
     creating /var/local/hydratk/yoda/lib/yodalib/testenv
     copying var/local/hydratk/yoda/lib/yodalib/testenv/__init__.py -> /var/local/hydratk/yoda/lib/yodalib/testenv
     copying var/local/hydratk/yoda/lib/yodalib/testenv/db_int.py -> /var/local/hydratk/yoda/lib/yodalib/testenv
     copying var/local/hydratk/yoda/lib/yodalib/testenv/rest_int.py -> /var/local/hydratk/yoda/lib/yodalib/testenv
     copying var/local/hydratk/yoda/lib/yodalib/testenv/soap_int.py -> /var/local/hydratk/yoda/lib/yodalib/testenv
     creating /var/local/hydratk/yoda/helpers/yodahelpers/testenv
     copying var/local/hydratk/yoda/helpers/yodahelpers/testenv/__init__.py -> /var/local/hydratk/yoda/helpers/yodahelpers/testenv
     copying var/local/hydratk/yoda/helpers/yodahelpers/testenv/helpers.py -> /var/local/hydratk/yoda/helpers/yodahelpers/testenv
     creating /var/local/hydratk/yoda/yoda-tests/testenv
     copying var/local/hydratk/yoda/yoda-tests/testenv/db.jedi -> /var/local/hydratk/yoda/yoda-tests/testenv
     copying var/local/hydratk/yoda/yoda-tests/testenv/rest.jedi -> /var/local/hydratk/yoda/yoda-tests/testenv
     copying var/local/hydratk/yoda/yoda-tests/testenv/soap.jedi -> /var/local/hydratk/yoda/yoda-tests/testenv
     creating build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_testenv.egg-info/PKG-INFO -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_testenv.egg-info/SOURCES.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_testenv.egg-info/dependency_links.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_testenv.egg-info/entry_points.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_testenv.egg-info/requires.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_testenv.egg-info/top_level.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     creating dist
     creating 'dist/hydratk_ext_testenv-0.2.0-py2.7.egg' and adding 'build/bdist.linux-x86_64/egg' to it
     removing 'build/bdist.linux-x86_64/egg' (and everything under it)
     Processing hydratk_ext_testenv-0.2.0-py2.7.egg
     creating /usr/local/lib/python2.7/dist-packages/hydratk_ext_testenv-0.2.0-py2.7.egg
     Extracting hydratk_ext_testenv-0.2.0-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding hydratk-ext-testenv 0.2.0 to easy-install.pth file
     Installing testenv script to /usr/local/bin

     Installed /usr/local/lib/python2.7/dist-packages/hydratk_ext_testenv-0.2.0-py2.7.egg
     Processing dependencies for hydratk-ext-testenv==0.2.0
     Searching for web.py>=0.37
     Reading https://pypi.python.org/simple/web.py/
     Best match: web.py 0.37
     Downloading https://pypi.python.org/packages/24/61/e5adedea4f716539b7858faea90e2e35299bf33c57aa0194b437fd01ec53/web.py-0.37.tar.gz#md5=93375e3f03e74d6bf5c5096a4962a8db
     Processing web.py-0.37.tar.gz
     Writing /tmp/easy_install-Z_z8zl/web.py-0.37/setup.cfg
     Running web.py-0.37/setup.py -q bdist_egg --dist-dir /tmp/easy_install-Z_z8zl/web.py-0.37/egg-dist-tmp-HS2G3T
     creating /usr/local/lib/python2.7/dist-packages/web.py-0.37-py2.7.egg
     Extracting web.py-0.37-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding web.py 0.37 to easy-install.pth file

     Using /usr/local/lib/python2.7/dist-packages/pycparser-2.14-py2.7.egg
     Finished processing dependencies for hydratk-ext-testenv==0.2.0
     
Run
^^^

When installation is finished you can run the application.

Check hydratk-ext-testenv module is installed.

  .. code-block:: bash
  
     $ pip list | grep hydratk
     
     hydratk (0.3.0a0.dev1)
     hydratk-ext-testenv (0.2.0a0)

Check installed extensions

  .. code-block:: bash
  
     $ htk list-extensions
     
     TestEnv: TestEnv v0.2.0 (c) [2015-2016 Petr Rašek <bowman@hydratk.org>]
     
Type command htk help and detailed info is displayed.

  .. code-block:: bash
  
     $ htk help
     
     Commands:
       te-install - install testing environment database
       te-run - start testing environment
       
You can run TestEnv also in standalone mode.

  .. code-block:: bash
  
     $ testenv help        
       
     TestEnv v0.2.0
     (c) 2015-2016 Petr Rašek <bowman@hydratk.org>
     Usage: /usr/local/bin/testenv [options] command

     Commands:
       help - prints help
       install - install testing environment database
       run - start testing environment

     Global Options:
       -c, --config <file> - reads the alternate configuration file
       -d, --debug <level> - debug turned on with specified level > 0
       -e, --debug-channel <channel number, ..> - debug channel filter turned on
       -f, --force - enforces command
       -i, --interactive - turns on interactive mode
       -l, --language <language> - sets the text output language, the list of available languages is specified in the docs
       -m, --run-mode <mode> - sets the running mode, the list of available languages is specified in the docs
              
Application installs following (paths depend on your OS configuration)

* testenv command in /usr/local/bin/testenv
* modules in /usr/local/lib/python2.7/dist-packages/hydratk-ext-testenv-0.2.0-py2.7egg
* configuration file in /etc/hydratk/conf.d/hydratk-ext-testenv.conf 
* application folder in /var/local/hydratk/testenv 
* yoda scripts in /var/local/hydratk/yoda                 