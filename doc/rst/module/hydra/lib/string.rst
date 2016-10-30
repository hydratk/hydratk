.. _module_hydra_lib_string:

string
======

This sections contains module documentation of string modules.

operation
^^^^^^^^^

Module provides methods for operations with string.
Unit tests available at hydratk/lib/string/operation/01_methods_ut.jedi

* mreplace

Method replaces string occurrences with new values (dictionary, key - string to replace).

  .. code-block:: python
  
     from hydratk.lib.string.operation import mreplace 
     
     # single key
     text = 'test 1234 test'
     res = mreplace(text, {'test ': '', '124': '421'})

     # multiple keys
     res = mreplace(text, {'test ': '', '1234 ': '4'})

* str_split

Method splits string to substring with given length.

* strip_accents

Method remove diacritics from string using unicodedata method normalize.

  .. code-block:: python
  
     from hydratk.lib.string.operation import strip_accents 
     
     text = 'Příliš žluťoučký kůň úpěl ďábelské ódy'
     res = strip_accents(text)
     # returns 'Prilis zlutoucky kun upel dabelske ody'     

prettify
^^^^^^^^

Module provides methods for pretty printing.
Unit tests available at hydratk/lib/string/prettify/01_methods_ut.jedi

* xml_prettify

Method transforms xml string to more human readable form (with indentation).