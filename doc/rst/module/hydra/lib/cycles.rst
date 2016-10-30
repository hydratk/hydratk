.. _module_hydra_lib_cycles:

cycles
======

This sections contains module documentation of cycles modules.

loop
^^^^

Module loop provides methods for cyclic data manipulation.
Unit tests available at hydratk/lib/cycles/loop/01_methods_ut.jedi

**Methods** :

* do_until

Method emulates do..until condition loop. Parameter call is callable of some method and parameters. until_call_result is requested method result 
which ends loop processing. Remaining parameters are used to end processing when result is not met (delay, until_max_attempts, until_duration, until_exact_time).
The method checks method result. If met the processing is finished. If not it checks whether the processing should be stopped otherwise it sleeps thread.

  .. code-block:: python
  
     from hydratk.lib.cycles.loop import do_until
     
     # delay
     do_until((dummy_method,), False, delay=0.13)
     
     # max attempts
     do_until((dummy_method,), False, until_max_attempts=2)
     
     # max duration
     do_until((dummy_method,), False, until_duration=1)
     
     # fixed end time
     do_until((dummy_method,), False, until_exact_time=start+1)