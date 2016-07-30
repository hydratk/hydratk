# -*- coding: utf-8 -*-
"""HydraTK template repository

.. module:: core.template
   :platform: Unix
   :synopsis: HydraTK template repository
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

from datetime import datetime

lib_default_user_data      = {
                             'lib_name'     : 'whiteforce',  
                             'lib_ucname'   : 'WhiteForce',
                             'author_name'  : 'Obi-Wan Kenobi',
                             'author_email' : 'kenobi@jedi.com',
                             'lib_year'     : datetime.now().year,
                             'lib_desc'     : 'This library provides example functionality, how to develop HydraTK shared libraries',
                             'lib_license'  : 'BSD'                                                          
                             }

lib_dir_struct             = [                             
                            'hydratk-lib-{lib_name}/src/hydratk/lib/{lib_name}',                         
                          ]

lib_package_files          = [                            
                            'hydratk-lib-{lib_name}/src/hydratk/__init__.py',
                            'hydratk-lib-{lib_name}/src/hydratk/lib/__init__.py',
                            'hydratk-lib-{lib_name}/src/hydratk/lib/{lib_name}/__init__.py',                            
                          ]

lib_package_init_content = '''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)
'''

lib_data_files   =  {                            
                            'lib.module'       : 'hydratk-lib-{lib_name}/src/hydratk/lib/{lib_name}/{lib_name}.py',                            
                            'lib.setup.py'     : 'hydratk-lib-{lib_name}/setup.py',
                            'lib.setup.cfg'    : 'hydratk-lib-{lib_name}/setup.cfg',
                            'lib.readme'       : 'hydratk-lib-{lib_name}/README.rst',
                            'lib.license'      : 'hydratk-lib-{lib_name}/LICENSE.txt',
                            'lib.requirements' : 'hydratk-lib-{lib_name}/requirements.txt',
                            'lib.manifest'     : 'hydratk-lib-{lib_name}/MANIFEST.in',
                          }

library = '''# -*- coding: utf-8 -*-
"""This code is a part of {lib_ucname} extension

.. module:: lib.{lib_name}.{lib_name}
   :platform: Unix
   :synopsis: {lib_desc}
.. moduleauthor:: {author_name} <{author_email}>

"""

def some_library_function():
    pass
  
'''

lib_setup_py = '''# -*- coding: utf-8 -*-
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
      name='{lib_ucname}',
      version='0.1.0a-dev1',
      description='{lib_desc}',
      long_description=readme,
      author='{author_name}',
      author_email='{author_email}',
      url='http://library.hydratk.org/{lib_name}',
      license='BSD',
      packages=find_packages('src'),
      install_requires=requires,
      package_dir={{'' : 'src'}},
      classifiers=classifiers,
      zip_safe=False
     )        
'''

lib_setup_cfg = '''[sdist]
formats = gztar,zip

[wheel]
universal = 1

[bdist_wheel]
universal = 1

[metadata]
description-file = README.rst

'''

lib_license = {
                   'BSD': '''Copyright (c) {ext_year}, {author_name} ({author_email})
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
'''
}

lib_readme_rst = '''
==================
README for {lib_ucname}
==================

| {lib_ucname} is shared library developed to use with Hydra Toolkit. 
| {lib_desc}
| It has decent portfolio of features:

* feature 1
* feature 2
* feature 3

OS and Python versions support
==============================

| Currently the Linux platform with CPython 2.6, 2.7, 3.x is supported, 
| but the final version is planned to be crossplatform and targeted also to the other popular systems 
| including Windows and OSX and possibly other Python versions such as Jython and IronPython
'''

lib_requirements = '''hydratk
'''

lib_manifest = '''include *.txt
'''

extension_default_user_data = {
                             'ext_name'     : 'hobbit',  
                             'ext_ucname'   : 'Hobbit',
                             'author_name'  : 'Bilbo Baggins',
                             'author_email' : 'bilbo@shire.com',
                             'ext_year'     : datetime.now().year,
                             'ext_desc'     : 'This extension provides example functionality, how to develop HydraTK extensions',
                             'ext_license'  : 'BSD'                                                          
                             }

extension_dir_struct    = [ 
                            'hydratk-ext-{extension}/etc/hydratk/conf.d',
                            'hydratk-ext-{extension}/src/hydratk/extensions/{extension}/translation/en',
                            'hydratk-ext-{extension}/src/hydratk/extensions/{extension}/translation/cs',                         
                          ]

extension_package_files = [                            
                            'hydratk-ext-{extension}/src/hydratk/__init__.py',
                            'hydratk-ext-{extension}/src/hydratk/extensions/__init__.py',
                            'hydratk-ext-{extension}/src/hydratk/extensions/{extension}/__init__.py',
                            'hydratk-ext-{extension}/src/hydratk/extensions/{extension}/translation/__init__.py',
                            'hydratk-ext-{extension}/src/hydratk/extensions/{extension}/translation/en/__init__.py',
                            'hydratk-ext-{extension}/src/hydratk/extensions/{extension}/translation/cs/__init__.py',
                          ]

extension_package_init_content = '''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)
'''

extension_data_files   =  {
                            'ext.config' : 'hydratk-ext-{extension}/etc/hydratk/conf.d/hydratk-ext-{extension}.conf',
                            'ext.module' : 'hydratk-ext-{extension}/src/hydratk/extensions/{extension}/{extension}.py',
                            'ext.bootstrapper' : 'hydratk-ext-{extension}/src/hydratk/extensions/{extension}/bootstrapper.py',
                            'ext.translation.en.messages' : 'hydratk-ext-{extension}/src/hydratk/extensions/{extension}/translation/en/messages.py',
                            'ext.translation.en.help'     : 'hydratk-ext-{extension}/src/hydratk/extensions/{extension}/translation/en/help.py',
                            'ext.translation.cs.messages' : 'hydratk-ext-{extension}/src/hydratk/extensions/{extension}/translation/cs/messages.py',
                            'ext.translation.cs.help'     : 'hydratk-ext-{extension}/src/hydratk/extensions/{extension}/translation/cs/help.py',
                            'ext.setup.py'     : 'hydratk-ext-{extension}/setup.py',
                            'ext.setup.cfg'    : 'hydratk-ext-{extension}/setup.cfg',
                            'ext.readme'       : 'hydratk-ext-{extension}/README.rst',
                            'ext.license'      : 'hydratk-ext-{extension}/LICENSE.txt',
                            'ext.requirements' : 'hydratk-ext-{extension}/requirements.txt',
                            'ext.manifest'     : 'hydratk-ext-{extension}/MANIFEST.in',
                          }
 

extension = '''# -*- coding: utf-8 -*-
"""This code is a part of {ext_ucname} extension

.. module:: extensions.{extension}.{extension}
   :platform: Unix
   :synopsis: This HydraTK generated extension is providing some cool functionality
.. moduleauthor:: {author_name} <{author_email}>

"""

from hydratk.core import extension

class Extension(extension.Extension):

    def _init_extension(self):
        self._ext_id      = '{extension}'
        self._ext_name    = '{ext_ucname}'
        self._ext_version = '0.1.0a-dev1'
        self._ext_author  = '{author_name} <{author_email}>'
        self._ext_year    = '{ext_year}'
        self._ext_desc    = '{ext_desc}'

    def _check_dependencies(self):
        return True
        
    def _do_imports(self):
        pass   
    
    def _register_actions(self):
        pass
                
'''

extension_bootstrapper = '''# -*- coding: utf-8 -*-
"""Providing custom bootstrapper for {extension} standalone app

.. module:: extensions.{extension}.bootstrapper
   :platform: Unix
   :synopsis: Providing custom bootstrapper for {extension} standalone app
.. moduleauthor:: {author_name} <{author_email}>

"""

import sys

PYTHON_MAJOR_VERSION = sys.version_info[0]
if PYTHON_MAJOR_VERSION == 2:
    reload(sys)
    sys.setdefaultencoding('UTF8')
    
def run_app(): 
      
    from hydratk.core.masterhead import MasterHead    
    mh = MasterHead.get_head()
    mh.set_cli_cmdopt_profile('{extension}')            
    mh.run_fn_hook('h_bootstrap')
    trn = mh.get_translator()  
    mh.dmsg('htk_on_debug_info', trn.msg('htk_app_exit'), mh.fromhere())                  
    sys.exit(0)
'''

extension_setup_py = '''# -*- coding: utf-8 -*-
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
         
files = {{
         'etc/hydratk/conf.d/hydratk-ext-{extension}.conf' : '/etc/hydratk/conf.d'
        }}                           
         
entry_points = {{
                'console_scripts': [
                    '{extension} = hydratk.extensions.{extension}.bootstrapper:run_app'                               
                ]
               }}          
                        
setup(
      name='{extension}',
      version='0.1.0a-dev1',
      description='{ext_desc}',
      long_description=readme,
      author='{author_name}',
      author_email='{author_email}',
      url='http://extensions.hydratk.org/{ext_ucname}',
      license='BSD',
      packages=find_packages('src'),
      install_requires=requires,
      package_dir={{'' : 'src'}},
      classifiers=classifiers,
      zip_safe=False,
      entry_points=entry_points  
     )        
     
if ('install' in argv or 'bdist_egg' in argv or 'bdist_wheel' in argv):
    
    for file, dir in files.items():    
        if (not path.exists(dir)):
            call('mkdir -p {dir}'.format(dir=dir), shell=True)
            
        call('cp {file} {dir}'.format(file=file, dir=dir), shell=True) 
        
    call('chmod -R a+r /etc/hydratk', shell=True)       
        
'''

extension_setup_cfg = '''[sdist]
formats = gztar,zip

[wheel]
universal = 1

[bdist_wheel]
universal = 1

[metadata]
description-file = README.rst

'''

extension_config = '''Extensions:
  {uc_extension}:
    package: hydratk.extensions.{extension}
    module: {extension}       
    enabled: 1    

'''

extension_translation_en_messages = '''# -*- coding: utf-8 -*-
"""This code is a part of {ext_ucname} extension

.. module:: extensions.{extension}.translation.en
   :platform: Unix
   :synopsis: English language translation for {ext_ucname} extension
.. moduleauthor:: {author_name} <{author_email}>

"""

language = {{
  'name' : 'English',
  'ISO-639-1' : 'en'
}}

msg = {{
    '{extension}_hello' : 'Hello from {ext_ucname} extension',         
}}
''' 

extension_translation_cs_messages = '''# -*- coding: utf-8 -*-
"""This code is a part of {ext_ucname} extension

.. module:: extensions.{extension}.translation.en
   :platform: Unix
   :synopsis: Czech language translation for {ext_ucname} extension
.. moduleauthor:: {author_name} <{author_email}>

"""

language = {{
  'name' : 'Čeština',
  'ISO-639-1' : 'cs'
}}

msg = {{
    '{extension}_hello' : 'Ahoj z rozšíření {ext_ucname}',         
}}
'''

extension_translation_en_help = '''# -*- coding: utf-8 -*-
"""This code is a part of {ext_ucname} extension

.. module:: extensions.{extension}.translation.en.help
   :platform: Unix
   :synopsis: English language translation for {ext_ucname} extension help generator
.. moduleauthor:: {author_name} <{author_email}>

"""

language = {{
  'name' : 'English',
  'ISO-639-1' : 'en'
}} 

\''' {ext_ucname} Commands \'''
help_cmd = {{
   '{extension}-test' : 'starts the {ext_ucname} test command',                   
}}

\''' {ext_ucname} Options \'''
help_opt = {{
   '{extension}-test-option' : {{ '{{h}}--{extension}-test-option <option>{{e}}' : {{ 'description' : 'test option', 'commands' : ('{extension}-test')}}}},   
}}
'''

extension_translation_cs_help = '''# -*- coding: utf-8 -*-
"""This code is a part of {ext_ucname} extension

.. module:: extensions.{extension}.translation.en.help
   :platform: Unix
   :synopsis: Czech language translation for {ext_ucname} extension help generator
.. moduleauthor:: {author_name} <{author_email}>

"""

language = {{
  'name' : 'Čeština',
  'ISO-639-1' : 'cs'
}} 

\''' {ext_ucname} Commands \'''
help_cmd = {{
   '{extension}-test' : 'spustí {ext_ucname} testovací příkaz',                   
}}

\''' {ext_ucname} Options \'''
help_opt = {{
   '{extension}-test-option' : {{ '{{h}}--{extension}-test-option <option>{{e}}' : {{ 'description' : 'testovazí možnost', 'commands' : ('{extension}-test')}}}},   
}}
''' 

extension_license = {
                   'BSD': '''Copyright (c) {ext_year}, {author_name} ({author_email})
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
'''
}


extension_readme_rst = '''
==================
README for {ext_ucname}
==================

| {ext_ucname} is extension developed to use with Hydra Toolkit. 
| {ext_desc}
| It has decent portfolio of features:

* feature 1
* feature 2
* feature 3

OS and Python versions support
==============================

| Currently the Linux platform with CPython 2.6, 2.7, 3.x is supported, 
| but the final version is planned to be crossplatform and targeted also to the other popular systems 
| including Windows and OSX and possibly other Python versions such as Jython and IronPython
'''

extension_requirements = '''hydratk
'''

extension_manifest = '''include *.txt
'''