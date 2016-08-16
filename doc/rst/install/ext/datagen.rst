.. install_ext_datagen:

DataGen
=======

You have 2 options how to install DataGen extension.

Package
^^^^^^^

Install it via Python package managers PIP or easy_install.

Filename after PIP download contains version, adapt sample code.

  .. code-block:: bash
  
     $ sudo pip download hydratk-ext-datagen
     $ sudo pip install hydratk-ext-datagen.tar.gz 
     
  .. code-block:: bash
  
     $ sudo easy_install hydratk-ext-datagen
     
  .. note::
  
     Use PIP to install package from local file for correct installation.
     When installed from remote repository, PIP sometimes doesn't call setup.py.       

Source
^^^^^^

Download the source code from GitHub or PyPi and install it manually.
Full PyPi URL contains MD5 hash, adapt sample code.

  .. code-block:: bash
  
     $ git clone https://github.com/hydratk/hydratk-ext-datagen.git
     $ cd ./hydratk-ext-datagen
     $ sudo python setup.py install
     
  .. code-block:: bash
  
     $ wget https://python.org/pypi/hydratk-ext-datagen -O hydratk-ext-datagen.tar.gz
     $ tar -xf hydratk-ext-datagen.tar.gz
     $ cd ./hydratk-ext-datagen
     $ sudo python setup.py install
     
Requirements
^^^^^^^^^^^^     
     
The extension requires hydratk, hydratk-lib-network. 

.. note::
 
   ASN.1 codec is supported for Python 2.7 only.    
     
Installation
^^^^^^^^^^^^

See installation example.

  .. code-block:: bash
  
     running install
     running bdist_egg
     running egg_info
     writing requirements to src/hydratk_ext_datagen.egg-info/requires.txt
     writing src/hydratk_ext_datagen.egg-info/PKG-INFO
     writing top-level names to src/hydratk_ext_datagen.egg-info/top_level.txt
     writing dependency_links to src/hydratk_ext_datagen.egg-info/dependency_links.txt
     writing entry points to src/hydratk_ext_datagen.egg-info/entry_points.txt
     reading manifest file 'src/hydratk_ext_datagen.egg-info/SOURCES.txt'
     reading manifest template 'MANIFEST.in'
     writing manifest file 'src/hydratk_ext_datagen.egg-info/SOURCES.txt'
     installing library code to build/bdist.linux-x86_64/egg
     running install_lib
     running build_py
     creating build
     creating build/lib.linux-x86_64-2.7
     creating build/lib.linux-x86_64-2.7/hydratk
     copying src/hydratk/__init__.py -> build/lib.linux-x86_64-2.7/hydratk
     creating build/lib.linux-x86_64-2.7/hydratk/extensions
     copying src/hydratk/extensions/__init__.py -> build/lib.linux-x86_64-2.7/hydratk/extensions
     creating build/lib.linux-x86_64-2.7/hydratk/extensions/datagen
     copying src/hydratk/extensions/datagen/__init__.py -> build/lib.linux-x86_64-2.7/hydratk/extensions/datagen
     ...
     
     byte-compiling build/bdist.linux-x86_64/egg/hydratk/__init__.py to __init__.pyc
     byte-compiling build/bdist.linux-x86_64/egg/hydratk/extensions/__init__.py to __init__.pyc
     ...
     
     creating build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_datagen.egg-info/PKG-INFO -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_datagen.egg-info/SOURCES.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_datagen.egg-info/dependency_links.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_datagen.egg-info/entry_points.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_datagen.egg-info/not-zip-safe -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_datagen.egg-info/requires.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     copying src/hydratk_ext_datagen.egg-info/top_level.txt -> build/bdist.linux-x86_64/egg/EGG-INFO
     creating dist
     creating 'dist/hydratk_ext_datagen-0.1.0a0.dev1-py2.7.egg' and adding 'build/bdist.linux-x86_64/egg' to it
     removing 'build/bdist.linux-x86_64/egg' (and everything under it)
     Processing hydratk_ext_datagen-0.1.0a0.dev1-py2.7.egg
     creating /usr/local/lib/python2.7/dist-packages/hydratk_ext_datagen-0.1.0a0.dev1-py2.7.egg
     Extracting hydratk_ext_datagen-0.1.0a0.dev1-py2.7.egg to /usr/local/lib/python2.7/dist-packages
     Adding hydratk-ext-datagen 0.1.0a0.dev1 to easy-install.pth file
     Installing datagen script to /usr/local/bin
     Installed /usr/local/lib/python2.7/dist-packages/hydratk_ext_datagen-0.1.0a0.dev1-py2.7.egg  
  
Application installs following (paths depend on your OS configuration)

* datagen command in /usr/local/bin/datagen
* modules in /usr/local/lib/python2.7/dist-packages/hydratk_ext_datagen-0.1.0-py2.7.egg
* configuration file in /etc/hydratk/conf.d/hydratk-ext-datagen.conf    
     
Run
^^^

When installation is finished you can run the application.

Check hydratk-ext-datagen module is installed.   

  .. code-block:: bash
  
     $ pip list | grep hydratk
     
     hydratk (0.3.0a0.dev1)
     hydratk-ext-datagen (0.1.0)
     
Check installed extensions

  .. code-block:: bash
  
     $ htk list-extensions
     
     Datagen: Datagen v0.1.0 (c) [2016 Petr Rašek <bowman@hydratk.org>] 
     
Type command htk help and detailed info is displayed.

  .. code-block:: bash
  
     $ htk help
     
     Commands:    
       gen-asn1 - encode text file, decode binary file according to ASN.1 specification
         Options:
           --gen-action encode|decode - action
           --gen-element <title> - element title from specification
           --gen-input <path> - input filename
           --gen-spec <path> - specification filename
           [--gen-output <path>] - output filename, default input filename with changed suffix or sample.json, sample.xml

       gen-json - generate sample json file according to JSON specification
         Options:
           --gen-spec <path> - specification filename
           [--gen-output <path>] - output filename, default input filename with changed suffix or sample.json, sample.xml

       gen-xml - generate sample xml file according to WSDL/XSD specification
         Options:
           --gen-element <title> - element title from specification
           --gen-spec <path> - specification filename
           [--gen-envelope] - generate including SOAP envelope
           [--gen-output <path>] - output filename, default input filename with changed suffix or sample.json, sample.xml
           
You can run DataGen also in standalone mode.  

  .. code-block:: bash
  
     $ datagen help
     
     Datagen v0.1.0
     (c) 2016 Petr Rašek <bowman@hydratk.org>
     Usage: /usr/local/bin/datagen [options] command

     Commands:
       asn1 - encode text file, decode binary file according to ASN.1 specification
         Options:
           --action encode|decode - action
           --element <title> - element title from specification
           --input <path> - input filename
           --spec <path> - specification filename
           [--output <path>] - output filename, default input filename with changed suffix or sample.json, sample.xml

       help - prints help
       json - generate sample json file according to JSON specification
         Options:
           --spec <path> - specification filename
           [--output <path>] - output filename, default input filename with changed suffix or sample.json, sample.xml

       xml - generate sample xml file according to WSDL/XSD specification
         Options:
           --element <title> - element title from specification
           --spec <path> - specification filename
           [--envelope] - generate including SOAP envelope
           [--output <path>] - output filename, default input filename with changed suffix or sample.json, sample.xml
              
     Global Options:
       -c, --config <file> - reads the alternate configuration file
       -d, --debug <level> - debug turned on with specified level > 0
       -e, --debug-channel <channel number, ..> - debug channel filter turned on
       -f, --force - enforces command
       -i, --interactive - turns on interactive mode
       -l, --language <language> - sets the text output language, the list of available languages is specified in the docs
       -m, --run-mode <mode> - sets the running mode, the list of available languages is specified in the docs                                   