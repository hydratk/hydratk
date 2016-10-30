.. _module_hydra_lib_array:

array
=====

This sections contains module documentation of array modules.

multidict
^^^^^^^^^

Module multidict provides class MultiDict inherited from collection defaultdict.
Unit tests available at hydratk/lib/array/multidict/01_methods_ut.jedi

**Methods** :

* __init__

Methods reuses defaultdict method __init__.

* __repr__

Methods reuses dict method __repr__.

operation
^^^^^^^^^

Module provides methods to manipulate with collections.
Unit tests available at hydratk/lib/array/operation/01_methods_ut.jedi

**Methods** :

* subdict

Method returns subdictionary (given items from original dictionary).

  .. code-block:: python
  
     from hydratk.lib.array.operation import subdict
     d = {'data1': 1, 'data2': 2, 'data3': 3}
     
     # one item
     res = subdict(d, ['data1'])
     
     # two items
     res = subdict(d, ['data1', 'data3'])