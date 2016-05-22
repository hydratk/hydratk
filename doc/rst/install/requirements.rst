.. _install_req:

Requirements
============

HydraTK is implemented in Python. Before you can install, you must fulfill basic requirements.

.. _install_req_basic:

Basic
^^^^^
* Any OS Unix - distributions Debian, Red Hat, etc with apt-get or yum package manager
* Python interpreter - versions `2.7x <https://www.python.org/downloads/release/python-2711/>`_, `3.1x <https://www.python.org/download/releases/3.1.4/>`_, `PyPy 2.6x <http://pypy.org/download.html>`_
* `PIP <https://pypi.python.org/pypi/pip>`_ module to enable installation from PyPi repository

.. note::

   OS Windows and OS X are not supported, but there are future plans to support them.

.. _install_req_modules:

Modules
^^^^^^^

HydraTK also uses several 3rd party open source Python modules.
These libraries will be installed automatically, if not installed yet.

* `psutil <https://pypi.python.org/pypi/psutil>`_: additional os process info
* `pyyaml <https://pypi.python.org/pypi/PyYAML>`_: YAML format parser
* `pyzmq <https://pypi.python.org/pypi/pyzmq>`_: support for Zero Message Queue
* `setproctitle <https://pypi.python.org/pypi/setproctitle>`_: custom os process titles
* `xtermcolor <https://pypi.python.org/pypi/xtermcolor>`_: colorizing terminal output

.. note:: 

   Modules pyzmq and setproctitle require some other libraries (written in C) which will be also installed.