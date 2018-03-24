.. _module_hydra_lib_compat:

compat
======

This sections contains module documentation of compat modules.

contentfix
^^^^^^^^^^

Module provides methods for Python compatibility problems.

* slash_escape - escaping undecoded unicode data

types
^^^^^

Module provides common data type names compatible both for Python 2 and Python 3.

* unicode - alias for str in Py3
* bytes - alias for str in Py2
* basestring - alias for (str,bytes) in Py3

utils
^^^^^

Module provides common method names compatible both for Python 2 and Python 3.

* range - alias for xrange in Py2