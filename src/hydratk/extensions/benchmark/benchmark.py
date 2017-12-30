# -*- coding: utf-8 -*-
"""Benchmark extension for tuning and testing hydra toolkit performance

.. module:: benchmark.benchmark
   :platform: Unix
   :synopsis: Benchmark extension for tuning and testing hydra toolkit performance.
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

"""
Events:
-------
benchmark_start
benchmark_finish

"""

from hydratk.core import extension
from hydratk.lib.console.commandlinetool import CommandlineTool
from hydratk.core import event
from importlib import import_module
from timeit import Timer
from csv import reader
from itertools import count
from math import sqrt

try:
    from itertools import izip_longest
    from StringIO import StringIO
except ImportError:
    from itertools import zip_longest as izip_longest
    from io import StringIO

class Extension(extension.Extension):
    """Class Extension
    """

    _groups = None
    _cycles = None
    _outfile = None
    _enable_gc = None
    _result = {}

    _test_groups = {
                    'disk'    : 'hydratk.extensions.benchmark.tests.disk',
                    'event'   : 'hydratk.extensions.benchmark.tests.event',
                    'math'    : 'hydratk.extensions.benchmark.tests.math',
                    'memory'  : 'hydratk.extensions.benchmark.tests.memory',
                    'network' : 'hydratk.extensions.benchmark.tests.network'
                   }

    def _init_extension(self):
        """Method initializes extension

        Args:
           none

        Returns:
           void

        """

        self._ext_id = 'benchmark'
        self._ext_name = 'BenchMark'
        self._ext_version = '0.2.0'
        self._ext_author = 'Petr Czaderna <pc@hydratk.org>, HydraTK team <team@hydratk.org>'
        self._ext_year = '2013 - 2018'

    def _register_actions(self):
        """Method registers actions

        Args:
           none

        Returns:
           void

        """

        self._mh.match_cli_command('benchmark')

        hook = [
            {'command': 'benchmark', 'callback': self.run_benchmark}
        ]
        self._mh.register_command_hook(hook)

        self._mh.match_long_option('bench-groups', True, 'bench-groups')
        self._mh.match_long_option('bench-cycles', True, 'bench-cycles')
        self._mh.match_long_option('bench-out', True, 'bench-out')
        self._mh.match_long_option('bench-gc', False, 'bench-gc')

    def run_benchmark(self):
        """Method handles command benchmark

        Args:
           none

        Returns:
           void

        """

        groups = CommandlineTool.get_input_option('bench-groups')
        cycles = CommandlineTool.get_input_option('bench-cycles')
        outfile = CommandlineTool.get_input_option('bench-out')
        enable_gc = CommandlineTool.get_input_option('bench-gc')

        self._cfg = self._mh.cfg['Extensions']['BenchMark']
        if (not groups):
            self._groups = self._test_groups.keys() if (self._cfg['groups'] == 'all') else self._cfg['groups'].split(',')
        else:
            self._groups = groups.split(',')
        self._cycles = self._cfg['cycles'] if (not cycles) else int(cycles)
        self._outfile = self._cfg['outfile'] if (not outfile) else outfile
        self._enable_gc = self._cfg['enable_gc'] if (not enable_gc) else True
        
        self._mh.demsg('htk_on_debug_info', self._mh._trn.msg('benchmark_start'), self._mh.fromhere())
        ev = event.Event('benchmark_start')
        self._mh.fire_event(ev)

        self.run_test_groups()

        self._mh.demsg('htk_on_debug_info', self._mh._trn.msg('benchmark_finish'), self._mh.fromhere())
        ev = event.Event('benchmark_finish')
        self._mh.fire_event(ev)
        
    def run_test_groups(self):
        """Method runs requested test groups

        Args:
           none

        Returns:
           void

        """
        
        result = {}
        for group in self._groups:
            if (group in self._test_groups):
                result[group] = self.run_test_group(group)
            else:
                self._mh.demsg('htk_on_debug_info', self._mh._trn.msg('benchmark_unknown_group', group), self._mh.fromhere())

        self.gen_report(result)
            
    def run_test_group(self, group):
        """Method runs requested test group

        Args:
           group (str): test group

        Returns:
           dict: result

        """
        
        self._mh.demsg('htk_on_debug_info', self._mh._trn.msg('benchmark_group_start', group), self._mh.fromhere())

        mod = self._test_groups[group]
        lmod = import_module(mod)

        result = {}
        for test in lmod.tests:
            result[test] = self.run_test(mod, test)

        self._mh.demsg('htk_on_debug_info', self._mh._trn.msg('benchmark_group_finish', group), self._mh.fromhere())

        return result

    def run_test(self, mod, test):
        """Method runs requested test

        Args:
           mod (str): test group module
           test (str): test method

        Returns:
           list: result

        """

        self._mh.demsg('htk_on_debug_info', self._mh._trn.msg('benchmark_test_start', test), self._mh.fromhere())

        setup = 'from {0} import {1}'.format(mod, test)
        if (self._enable_gc):
            setup += '; gc.enable()'
        timer = Timer(test + '()', setup=setup)

        result = []
        for i in range(self._cycles):
            r = timer.timeit(1)
            result.append(round(r * 1000, 3))

        self._mh.demsg('htk_on_debug_info', self._mh._trn.msg('benchmark_test_finish', test), self._mh.fromhere())

        return result

    def gen_report(self, result):
        """Method prepares report

        Args:
           result (dict): test results

        Returns:
           void

        """

        data = 'Group,Test,Mean,Median,Min,Max,Variance,Std deviation,1st quartile,3rd quartile\n'
        raw_data = []

        for group, tests in sorted(result.items()):
            for test, values in sorted(tests.items()):
                data += '{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n'.format(group, test, *self.calc_stats(values))
                raw_data.append(values)

        if (self._outfile != None):
            try:

                data_rows = data.splitlines()
                report = '{0},{1}\n'.format(data_rows[0], ','.join(['Value'] * self._cycles))

                for i in range(len(raw_data)):
                    report += '{0},{1}\n'.format(data_rows[i + 1], ','.join(map(str, raw_data[i])))

                with open(self._outfile, 'w') as f:
                    f.write(report)

            except Exception as ex:
                self._mh.demsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())

        self.print_report(data)

    def calc_stats(self, values):
        """Method calculates statistic parameters

        Args:
           values (list): test executions in ms

        Returns:
           tuple: mean, median, min, max, var, stddev, quartile1, quartile3

        """

        values = sorted(values)
        cnt = len(values)
        
        mean = sum(values) / cnt
        vmin = round(min(values), 3)
        vmax = round(max(values), 3)
        
        diff = []
        for val in values:
            diff.append((val - mean) ** 2)
        var = round(sum(diff) / cnt, 3)
        stddev = round(sqrt(var), 3)
        
        if (cnt % 2 == 1):
            idx = int(cnt / 2)
            median = values[idx]
            half1, half2 = values[:idx], values[idx + 1:]
            idx = int(idx / 2)
            quartile1 = (half1[idx] + half1[idx + 1]) / 2
            quartile3 = (half2[idx] + half2[idx + 1]) / 2
        else:    
            idx = int(cnt / 2) 
            median = (values[idx] + values[idx + 1]) / 2
            half1, half2 = values[:idx], values[idx:]
            idx = int(idx / 2)
            quartile1 = (half1[idx] + half1[idx + 1]) / 2
            quartile3 = (half2[idx] + half2[idx + 1]) / 2

        return round(mean, 3), round(median, 3), vmin, vmax, var, stddev, round(quartile1, 3), round(quartile3, 3)

    def print_report(self, data):
        """Method prints report in table form

        Args:
           data (str): test results in CSV form

        Returns:
           void

        """

        max_widths = []
        max_indent = 0
        for line in reader(StringIO(data)):
            widths = [len(s.strip()) + 2 for s in line]
            max_widths = list(map(max, izip_longest(max_widths, widths, fillvalue=0)))
            indent = len(line[0]) - len(line[0].lstrip())
            max_indent = max(max_indent, indent)

        result = StringIO()
        for line in reader(StringIO(data)):
            result.write(' ' * max_indent)

            last_column = len(line) - 1
            for value, max_width, column in zip(line, max_widths, count()):
                value = value.strip()
                result.write('' + value)
                if (column != last_column):
                    result.write(' ')
                    result.write(' ' * (max_width - len(value)))

            result.write('\n')

        print(result.getvalue())
