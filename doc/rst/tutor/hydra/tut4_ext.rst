.. _tutor_hydra_tut4_ext:

Tutorial 4: Extension
=====================

If you would like to create own extension you should with this tutorial
which explains basic principles.

Skeleton
^^^^^^^^

HydraTK provides embedded command which creates extension skeleton.
Execute command ``create-ext-skel``

  .. code-block:: bash
  
     $ htk create-ext-skel
    
     Completed. 
     
Skeleton is created in directory ~/hydratk/hydratk-ext-hobbit.

  .. code-block:: bash
  
     /etc - configuration file
       /hydratk     
         /conf.d
           /hydratk-ext-hobbit.conf
     /src - source code
       /hydratk
         /extensions
           /hobbit - extension title
             bootstrapper.py - bootstrapper code
             hobbit.py - extension code
             __init__.py             
             /translation - langtexts for Czech and English language
               /cs
                 help.py - command line help
                 __init__.py
                 messages.py - messages used in code
               /en
                 help.py
                 __init__.py
                 messages.py
               __init__.py
           __init__.py
         __init__.py
     LICENSE.txt - license file with template text
     MANIFEST.in - manifest file with template text
     README.rst - readme file with template text
     requirements.txt - requirements file with template text
     setup.cfg - setup configuration
     setup.py - setup script with template text   
     
The texts are created from template, you should rewrite them upon specific needs.     
     
Skeleton command supports several options.
Use option ``--ext-skel-path <path>`` to create skeleton in requested directory.

  .. code-block:: bash
  
     $ htk --ext-skel-path ~/ext create-ext-skel
     
     Completed.
     
Wizard
^^^^^^     
     
Use option ``-i`` or ``--interactive`` to turn on skeleton wizard.
The wizard will guide you through creation process and ask some questions to customize skeleton files.

  .. code-block:: bash
  
     $ htk -i create-ext-skel
     
     ****************************************
     *   Extension skeleton create wizard   *
     ****************************************
     This wizard will create HydraTK extension development skeleton in following 6 steps
     Hit ENTER for default value, CTRL + C to exit
     
     1. Enter the directory, where the extension structure will be created
     [~/hydratk]: your path
     Extension skeleton directory set to: your path
     
     2. Enter the extension module name, must be one word short unique string
     [hobbit]: your ext name
     Extension module name set to: your ext name
     
     3. Enter the extension description
     [This extension provides example functionality, how to develop HydraTK extensions]: your description
     Extension description set to: your description
     
     4. Enter the extension author name
     [Bilbo Baggins]: your author
     Extension author name set to: your author
     
     5. Enter the extension author email
     [bilbo@shire.com]: your email
     Extension author email set to: your email
     
     6. Select extension usage and distribution license, currently supported are: BSD
     [BSD]: your license
     Extension usage and distribution license set to: your license
     
     Completed.
     
Skeleton is created in directory hydratk-ext-your_ext_name.         
     
Templates
^^^^^^^^^

See created files from template. Specific data can be overwritten by wizard.

* LICENSE.txt

Author and email can be overwritten.

  .. code-block:: cfg
  
     Copyright (c) 2016, Bilbo Baggins (bilbo@shire.com)
     All rights reserved.

     Redistribution and use in source and binary forms, with or without modification, 
     are permitted provided that the following conditions are met:

         * Redistributions of source code must retain the above copyright notice, 
           this list of conditions and the following disclaimer.
         * Redistributions in binary form must reproduce the above copyright notice, 
           this list of conditions and the following disclaimer in the documentation 
           and/or other materials provided with the distribution.
         * Neither the name of the Author nor the names of its contributors 
           may be used to endorse or promote products derived from this software 
           without specific prior written permission.

     THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
     ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
     WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
     DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE 
     FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
     DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
     SERVICES LOSS OF USE, DATA, OR PROFITS OR BUSINESS INTERRUPTION) HOWEVER 
     CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
     OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
     OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.    
     
* MANIFEST.in

  .. code-block:: cfg
  
     include *.txt     
     
* README.rst

Extension title and description can be overwritten.

  .. code-block:: cfg
  
     ==================
     README for Hobbit
     ==================

     | Hobbit is extension developed to use with Hydra Toolkit. 
     | This extension provides example functionality, how to develop HydraTK extensions
     | It has decent portfolio of features:

     * feature 1
     * feature 2
     * feature 3

     OS and Python versions support
     ==============================

     | Currently the Linux platform with CPython 2.6, 2.7, 3.x is supported, 
     | but the final version is planned to be crossplatform and targeted also to the other popular systems 
     | including Windows and OSX and possibly other Python versions such as Jython and IronPython 
     
* requirements.txt

  .. code-block:: cfg
  
     hydratk     
     
* setup.cfg

Wizard doesn't change thi file.

  .. code-block:: cfg
  
     [sdist]
     formats = gztar,zip

     [wheel]
     universal = 1

     [bdist_wheel]
     universal = 1

     [metadata]
     description-file = README.rst     
     
* setup.py

Extension title and description, author and email can be overwritten.
Module ``hydratk`` is automatically configured as required.

  .. code-block:: python

     # -*- coding: utf-8 -*-
     from setuptools import setup, find_packages
     from sys import argv, version_info
     from os import path
     from subprocess import call

     with open("README.rst", "r") as f:
         readme = f.read()
    
     classifiers = [
         "Development Status :: 3 - Alpha",
         "Environment :: Console",
         "Environment :: Other Environment",
         "Intended Audience :: Developers",
         "License :: Freely Distributable",
         "Operating System :: OS Independent",   
         "License :: OSI Approved :: BSD License",
         "Programming Language :: Python",    
         "Programming Language :: Python :: 2.6",
         "Programming Language :: Python :: 2.7",
         "Programming Language :: Python :: 3.3",
         "Programming Language :: Python :: 3.4",
         "Programming Language :: Python :: 3.5",
         "Programming Language :: Python :: Implementation",
         "Programming Language :: Python :: Implementation :: CPython",  
         "Topic :: Software Development :: Libraries :: Application Frameworks",
         "Topic :: Utilities"
     ]

     requires = [
                 'hydratk'           
                ]
         
     files = {
              'etc/hydratk/conf.d/hydratk-ext-hobbit.conf' : '/etc/hydratk/conf.d'
             }                           
         
     entry_points = {
                'console_scripts': [
                    'hobbit = hydratk.extensions.hobbit.bootstrapper:run_app'                               
                     ]
                    }          
                        
     setup(
           name='hobbit',
           version='0.1.0a-dev1',
           description='This extension provides example functionality, how to develop HydraTK extensions',
           long_description=readme,
           author='Bilbo Baggins',
           author_email='bilbo@shire.com',
           url='http://extensions.hydratk.org/Hobbit',
           license='BSD',
           packages=find_packages('src'),
           install_requires=requires,
           package_dir={'' : 'src'},
           classifiers=classifiers,
           zip_safe=False,
           entry_points=entry_points  
          )        
     
     if ('install' in argv or 'bdist_egg' in argv or 'bdist_wheel' in argv):
    
         for file, dir in files.items():    
             if (not path.exists(dir)):
                 call('mkdir -p dir'.format(dir=dir), shell=True)
            
             call('cp file dir'.format(file=file, dir=dir), shell=True) 
        
         call('chmod -R a+r /etc/hydratk', shell=True)                 

* hydratk-ext-hobbit.conf

Configuration file, extension is enabled by default.

  .. code-block:: yaml
  
     Extensions:
       Hobbit:
         package: hydratk.extensions.hobbit
         module: hobbit       
         enabled: 1   
    
* bootstrapper.py

Extension title and description, author and email can be overwritten.

  .. code-block:: python  
  
     # -*- coding: utf-8 -*-
     """Providing custom bootstrapper for hobbit standalone app

     .. module:: extensions.hobbit.bootstrapper
        :platform: Unix
        :synopsis: Providing custom bootstrapper for hobbit standalone app
     .. moduleauthor:: Bilbo Baggins <bilbo@shire.com>

     """

     import sys

     PYTHON_MAJOR_VERSION = sys.version_info[0]
     if PYTHON_MAJOR_VERSION == 2:
         reload(sys)
         sys.setdefaultencoding('UTF8')
    
     def run_app(): 
      
         from hydratk.core.masterhead import MasterHead    
         mh = MasterHead.get_head()
         mh.set_cli_cmdopt_profile('hobbit')            
         mh.run_fn_hook('h_bootstrap')
         trn = mh.get_translator()  
         mh.dmsg('htk_on_debug_info', trn.msg('htk_app_exit'), mh.fromhere())                  
         sys.exit(0)    
          
* hobbit.py

Extension title and description, author and email can be overwritten.

  .. code-block:: python
  
     # -*- coding: utf-8 -*-
     """This code is a part of Hobbit extension

     .. module:: extensions.hobbit.hobbit
        :platform: Unix
        :synopsis: This HydraTK generated extension is providing some cool functionality
     .. moduleauthor:: Bilbo Baggins <bilbo@shire.com>

     """

     from hydratk.core import extension

     class Extension(extension.Extension):

         def _init_extension(self):
             self._ext_name    = 'Hobbit'
             self._ext_version = '0.1.0a-dev1'
             self._ext_author  = 'Bilbo Baggins <bilbo@shire.com>'
             self._ext_year    = '2016'
             self._ext_desc    = 'This extension provides example functionality, how to develop HydraTK extensions'

         def _check_dependencies(self):
             return True
        
         def _do_imports(self):
             pass   
    
         def _register_actions(self):
             pass
    
* help.py

Extension title and description, author and email can be overwritten.

  .. code-block:: python
  
     # -*- coding: utf-8 -*-
     """This code is a part of Hobbit extension

     .. module:: extensions.hobbit.translation.en.help
        :platform: Unix
        :synopsis: English language translation for Hobbit extension help generator
     .. moduleauthor:: Bilbo Baggins <bilbo@shire.com>

     """

     language = {
       'name' : 'English',
       'ISO-639-1' : 'en'
     } 

     ''' Hobbit Commands '''
     help_cmd = {
        'hobbit-test' : 'starts the Hobbit test command',                   
     }

     ''' Hobbit Options '''
     help_opt = {
        'hobbit-test-option' : { '{h}--hobbit-test-option <option>{e}' : { 'description' : 'test option', 'commands' : ('hobbit-test')}},   
     }
     
* messages.py

Extension title and description, author and email can be overwritten.

  .. code-block:: python
  
     # -*- coding: utf-8 -*-
     """This code is a part of Hobbit extension

     .. module:: extensions.hobbit.translation.en
        :platform: Unix
        :synopsis: English language translation for Hobbit extension
     .. moduleauthor:: Bilbo Baggins <bilbo@shire.com>

     """

     language = {
       'name' : 'English',
       'ISO-639-1' : 'en'
     }

     msg = {
         'hobbit_hello' : 'Hello from Hobbit extension',         
     }     
     
Development
^^^^^^^^^^^

Let's develop simple extension.
We will use created source file hobbit.py.

Implement method _register_actions to register two commands: hobbit-start, hobbit-stop.
When command received HydraTK calls specified callback method.
Extension supports long command option --mode with expected value.

Method start reads option --mode and prints message. 
Method stop prints message.

  .. code-block:: python
  
     def _register_actions(self):

        self._mh.match_cli_command('hobbit-start')
        self._mh.match_cli_command('hobbit-stop')

        hook = [
                {'command' : 'hobbit-start', 'callback' : self.start},
                {'command' : 'hobbit-stop', 'callback' : self.stop},
               ]
        self._mh.register_command_hook(hook)

        self._mh.match_long_option('mode', True)

    def start(self):

        from hydratk.lib.console.commandlinetool import CommandlineTool
        mode = CommandlineTool.get_input_option('--mode')

        print('starting in mode: %s' % mode)
        
    def stop(self):
 
        print('stopping')        
          
Install the extension as standard Python module.

  .. code-block:: python
  
     $ python setup.py install
     
     Finished processing dependencies for Hobbit==0.1.0a
     
     $ pip list | grep Hobbit
     
     Hobbit (0.1.0a) 
     
Test both commands including option.

  .. code-block:: python
  
     $ htk --mode standard hobbit-start  
     
     starting in mode: standard
     
     $ htk hobbit-stop
     
     stopping 
     
Uninstall extension as standard Python module.

  .. code-block:: python
  
     $ pip uninstall Hobbit
     
     Successfully uninstalled Hobbit        
     
Command help
^^^^^^^^^^^^

Now we will configure command line help in file help.py.
Extension supports two commands: hobbit-start, hobbit-stop. Option mode is used for command hobbit-start.

  .. code-block:: python
  
     ''' Hobbit Commands '''
     help_cmd = {
         'hobbit-start' : 'starts Hobbit extension',
         'hobbit-stop' : 'stops Hobbit extension'
     }

     ''' Hobbit Options '''
     help_opt = {
         'mode' : { '{h}--mode <mode>{e}' : { 'description' : 'mode', 'commands' : ('hobbit-start')}},
     }
        
  
Print HydraTK help and check new commands.  
        
  .. code-block:: python
  
     $ htk help
     
     hobbit-start - starts Hobbit extension
       Options:
         --mode <mode> - mode

     hobbit-stop - stops Hobbit extension
                          
Langtexts   
^^^^^^^^^

Now we will configure langtexts in file messages.py.
Langtext hobbit_start is parametric.

  .. code-block:: python
  
     msg = {
         'hobbit_start' : ["Starting in mode: {0}"],
         'hobbit_stop'  : ["Stopping"]
     }

Start and stop methods use the langtexts as debug messages. 
 
  .. code-block:: python
  
     def start(self):

        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('hobbit_start', mode), self._mh.fromhere())

     def stop(self):
 
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('hobbit_stop'), self._mh.fromhere())
  
Test both commands in debug mode.

  .. code-block:: bash
  
     $ htk -d 1 --mode standard hobbit-start
     
     starting in mode: standard
     [16/05/2016 16:51:30.300] Debug(1): hydratk.extensions.hobbit.hobbit:start:0: Starting in mode: standard
          
     $ htk -d 1 hobbit-stop
     
     stopping
     [16/05/2016 16:50:07.244] Debug(1): hydratk.extensions.hobbit.hobbit:stop:0: Stopping
                                     
Configuration
^^^^^^^^^^^^^

Configuration file is stored in directory /etc/hydratk/conf.d.
We add configuration parameter mode with value standard to set default mode if not set in command line.

  .. code-block:: yaml
  
     Extensions:
       Hobbit:
         package: hydratk.extensions.hobbit
         module: hobbit
         enabled: 1
         mode: standard   
  
Start method reads configuration parameter.  
         
  .. code-block:: python
  
     def start(self):

         from hydratk.lib.console.commandlinetool import CommandlineTool
         mode = CommandlineTool.get_input_option('--mode')

         if (mode == False):
             mode = self._mh.cfg['Extensions']['Hobbit']['mode']
       
Test start command.

  .. code-block:: bash
  
     $ htk hobbit-start
     
     starting in mode: standard                                       