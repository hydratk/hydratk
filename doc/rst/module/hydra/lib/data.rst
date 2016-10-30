.. _module_hydra_lib_data:

data
====

This sections contains module documentation of data modules.

share
^^^^^

Module share provides shared objects stored in memory, originally designed for Yoda tests.
Unit tests available at hydratk/lib/data/share/01_methods_ut.jedi

Class **My**

**Attributes** :

* _pocket - reference to Pocket
* _piles - dictionary

**Properties (Getters)** :

* pocket - returns _pocket (automatically initialized if not set)
* piles - returns _piles

**Methods** :

* pile

Method creates new Pile identified by pile_id in _piles.

* drop_pile

Method deletes Pile identified by pile_id.

Class **Pocket**

**Attributes** :

* _data - dictionary

**Properties (Getters)** :

* content - returns _data

**Properties (Setters)** :

* content - sets _data

**Methods** : 

* show

Method prints data content.

* fill

Method sets _data to dictionary.

* purge

Method resets _data to empty dictionary.

  .. code-block:: python
  
     from hydratk.lib.data.share import Pocket   
     
     p = Pocket()
     data = {'data': 1, 'data2':2}
     p.fill(data)     

Class **Pile**

Empty class.