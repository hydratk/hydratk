.. _module_ext_benchmark_tests:

Test
====

This sections contains module documentation of test modules.

Disk
^^^^

Module contains tests for disk operations.

* file_single

Method creates single file of 10MB.

* file_mult

Method creates 1000 files of 1kB.

* dir_mult

Method creates 1000 directories.

* dir_tree

Method creates tree of 500 directories.

Event
^^^^^

Module contains tests for event processing.

* throughput

Method fires 10000 events processed by callback.

Math
^^^^

Module contains tests for mathematical algorithms.

* factorial

Method calculates factorial of 10000.

* fibonacci

Method calculates 10000 Fibonacci number.

* floating_point

Method performs 1e6 floating point operations.

Memory
^^^^^^

Module contains tests for memory operations.

* allocate_single

Method allocates variable of 1GB.

* allocate_mult

Method allocates 1000 variables of 1MB.

Network
^^^^^^^

Module contains tests for network operations.

* request_single

Method sends TCP request to localhost with data of 1MB.

* request_mult

Method sends 100 TCP requests to localhost with data of 1kB.