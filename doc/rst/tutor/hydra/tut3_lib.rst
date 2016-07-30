.. _tutor_hydra_tut3_lib:

Tutorial 3: Library
===================

If you would like to create own library you should with this tutorial
which explains basic principles.

Skeleton
^^^^^^^^

HydraTK provides embedded command which creates library skeleton.
Execute command ``create-lib-skel``

  .. code-block:: bash
  
     $ htk create-lib-skel
    
     Completed. 
    
Skeleton is created in directory ~/hydratk/hydratk-lib-whiteforce.   

  .. code-block:: bash
  
     /src - source code
       /hydratk
         /lib
           /whiteforce - library title
             __init__.py
             whiteforce.py - library code
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
Use option ``--lib-skel-path <path>`` to create skeleton in requested directory.

  .. code-block:: bash
  
     $ htk --lib-skel-path ~/lib create-lib-skel
     
     Completed.
     
Wizard
^^^^^^     
     
Use option ``-i`` or ``--interactive`` to turn on skeleton wizard.
The wizard will guide you through creation process and ask some questions to customize skeleton files.

  .. code-block:: bash
  
     $ htk -i create-lib-skel
     
     **************************************
     *   Library skeleton create wizard   *
     **************************************  
     This wizard will create HydraTK shared library development skeleton in following 6 steps
     Hit ENTER for default value, CTRL + C to exit
     
     1. Enter the directory, where the library structure will be created
     [~/hydratk]: your path
     Library skeleton directory set to: your path
     
     2. Enter the library module name, must be one word short unique string
     [whiteforce]: your lib name
     Library module name set to: your lib name
     
     3. Enter the library description
     [This library provides example functionality, how to develop HydraTK shared libraries]: your description
     Library description set to: your description
     
     4. Enter the lib author name
     [Obi-Wan Kenobi]: your author
     lib author name set to: your author
     
     5. Enter the library author email
     [kenobi@jedi.com]: your email
     Library author email set to: your email
     
     6. Select lib usage and distribution license, currently supported are: BSD
     [BSD]: your license
     Library usage and distribution license set to: your license
     
     Completed.
     
Skeleton is created in directory hydratk-lib-your_lib_name.     
     
Templates
^^^^^^^^^

See created files from template. Specific data can be overwritten by wizard.

* LICENSE.txt

Author and email can be overwritten.

  .. code-block:: cfg
  
     Copyright (c) 2016, Obi-Wan Kenobi (kenobi@jedi.com)
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

Library title and description can be overwritten.

  .. code-block:: cfg
  
     ==================
     README for WhiteForce
     ==================

     | WhiteForce is shared library developed to use with Hydra Toolkit. 
     | This library provides example functionality, how to develop HydraTK shared libraries
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

Library title and description, author and email can be overwritten.
Module ``hydratk`` is automatically configured as required.

  .. code-block:: python
  
     # -*- coding: utf-8 -*-
     from setuptools import setup, find_packages

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
         
     setup(
           name='WhiteForce',
           version='0.1.0a-dev1',
           description='This library provides example functionality, how to develop HydraTK shared libraries',
           long_description=readme,
           author='Obi-Wan Kenobi',
           author_email='kenobi@jedi.com',
           url='http://library.hydratk.org/whiteforce',
           license='BSD',
           packages=find_packages('src'),
           install_requires=requires,
           package_dir={'' : 'src'},
           classifiers=classifiers,
           zip_safe=False
          )     
          
* whiteforce.py

Library title and description, author and email can be overwritten.

  .. code-block:: python
  
     # -*- coding: utf-8 -*-
     """This code is a part of WhiteForce library

     .. module:: lib.whiteforce.whiteforce
        :platform: Unix
        :synopsis: This library provides example functionality, how to develop HydraTK shared libraries
     .. moduleauthor:: Obi-Wan Kenobi <kenobi@jedi.com>

     """

     def some_library_function():
         pass
         
Development
^^^^^^^^^^^

Let's develop simple library with sorting algorithms.
We will use created source file whiteforce.py and add new methods.  

  .. code-block:: python
  
     def bubble_sort (a):

         cnt = len(a)
         for i in xrange(0, cnt-1):
             for j in xrange(1, cnt-i):
                 if (a[j-1] > a[j]):
                     aux = a[j]
                     a[j] = a[j-1]
                     a[j-1] = aux

         return a    
         
     def selection_sort(a):

        cnt = len(a)
        for i in xrange(0, cnt-2):
            min = a[i]
            idx = i

            for j in xrange(i+1, cnt-1):
                if (a[j] < min):
                    min = a[j]    
                    idx = j

            aux = a[i]
            a[i] = min
            a[idx] = aux

        return a
                  
Install the library as standard Python module.

  .. code-block:: python
  
     $ python setup.py install
     
     Finished processing dependencies for WhiteForce==0.1.0a-dev1
     
     $ pip list | grep WhiteForce
     
     WhiteForce (0.1.0a-dev1)

Now use it from Python console.

  .. code-block:: python
  
     $ python
  
     >>> from hydratk.lib.whiteforce import whiteforce     
     >>> a = [1, 8, 5, 6, 4, 10]
     >>> b = whiteforce.bubble_sort(a)
     >>> print b
     [1, 4, 5, 6, 8, 10]
     >>> c = whiteforce.selection_sort(a)
     >>> print c
     [1, 4, 5, 6, 8, 10]  
     
  .. note::
  
     If you want to use HydraTK core functionalities (i.e. event, debug messages), HydraTK must be running.
     So you can't use the library just from console. More complex libraries are intended to be used from extensions or core modules.
     
Uninstall library as standard Python module.

  .. code-block:: python
  
     $ pip uninstall WhiteForce
     
     Successfully uninstalled WhiteForce        