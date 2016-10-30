.. _module_hydra_core_template:

template
========

This sections contains module documentation of template module.

template
^^^^^^^^

Module provides configuration to generate extension and library skeletons (used by methods gen_ext_skel, gen_lib_skel).
It contains directory structure and template file content (can be adapted using user input).

**Extension**

* directories - /doc, /etc/hydratk/conf.d, /src/hydratk/extensions/{extension}/translation/en (and cs)
* data_files - /doc/{extension}.1, /etc/hydratk/conf.d/hydratk-ext-{extension}.conf, bootstrapper.py, messages.py, help.py, setup.py, setup.cfg, README.rst, LICENSE.txt, requirements.txt, MANIFEST.in 
* package_files - files __init__.py to access all source directories
* metadata - ext_name hobbit, author Bilbo Baggins, email bilbo@shire.com

**Library**

* directories - /doc, /src/hydratk/lib/{lib_name}
* data files - /src/hydratk/lib/{lib_name}/{lib_name}.py, setup.py, setup.cfg, README.rst, LICENSE.txt, requirements.txt, MANIFEST.in 
* package files - files __init__.py to access all source directories
* metadata - lib_name whiteforce, author Obi-Wan Kenobi, email kenobi@jedi.com 
