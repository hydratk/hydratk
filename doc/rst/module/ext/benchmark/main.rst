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

* _groups - test group to execute, default all
* _cycles - test cycles, default 20
* _outfile - output filename, dafault not generated
* _enable_gc - enable garbage collector, default False
* _result - test execution results
* _test_groups - test groups modules mapping

**Methods** :

* _init_extension

Method sets extension metadata (id, name, version, author, year). 

* _register_actions

Method registers action hooks.

commands - benchmark
long options - bench-groups, bench-cycles, bench-out, bench-gc

* run_benchmark

Method handles command benchmark. It parses command options bench-groups, bench-cycles, bench-out, bench-gc.
Default values are taken from configuration parameters groups (all), cycles (20), outfile (None), enable_gc (False).
It fires event benchmark_start, calls method run_test_groups and fires event benchmark_finish. 

* run_test_groups

Method executes requested test groups and prints report.

* run_test_group

Method executes tests in given test group. Tests are stored in separate module which is imported.
It returns test group results as dictionary.

* run_test

Method executes given test. It uses class Timer from module timeit. Test code is imported in setup script.
Test is executed several times according to option cycles. Garbage collector is enabled/disabled according to option enable_gc.
It returns test results as list (execution times in milliseconds).

* gen_report

Method generates report in CSV format and stores it to file according to option outfile.

* calc_stats

Method calculates statistic parameters from execution times.
Mean, median, minimum, maximum, variance, standard deviation, 1st quartile, 3rd quartile.

* print_report

Method prints report as formatted table (sorted by group, test). Statistic parameters are displayed only (not execution times).