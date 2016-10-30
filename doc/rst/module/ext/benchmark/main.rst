.. _module_ext_benchmark_main:

Main
====

This sections contains module documentation of main benchmark modules.
Benchmark extension is bundled with hydratk (not standalone extension).

benchmark
^^^^^^^^^

Modules provides class Extension inherited from class hydratk.core.extension.Extension.
Unit tests available at hydratk/extensions/benchmark/benchmark/01_methods_ut.jedi

**Attributes** :

* _test_results - details of individual tests
* _print_details - bool, print to console
* _check_cycles - count of test cycles (default 10)

**Methods** :

* _init_extension

Method sets extension metadata (id, name, version, author, year). 

* _register_actions

Method registers action hooks.

commands - start-benchmark
long options - details

* _setup_params

Method sets _print_details according to option details. 

* start_bench_fc

Method handles command start-benchmark. It runs tests and prints results if allowed.

* _run_basic_tests

Method runs all tests.

* _print_test_info

Method prints test results.

* _event_thru_test

Method tests event performance, it fires 1e7 benchmark_test_event1 events with 1Kb message. It measures average processing time. 

* _factorial_test

Method tests factorial calculation, it calculates factorial of 10000 (recursive algorithm) in 10 cycles. It measures average, 
maximum and minimum processing time.

* __fibcalc

Auxiliary method which calculates n-th Fibonnaci number (effective non-recursive algorithm).

* _fib_test

Method tests Fibonacci numbers calculation, it calculates 10000th number in 10 cycles. It measures average, maximum and minimum processing time.

* _calc_flops_test

Method tests performance of floating point arithmetics, it performs 1e9 (GFLOP) sum operations in 10 cycles. It measures average, 
maximum and minimum processing time.
