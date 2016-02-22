# -*- coding: utf-8 -*-
"""This code is a part of Benchmark extension

.. module:: benchmark.benchmark
   :platform: Unix
   :synopsis: Benchmark extension for tuning and testing hydra toolkit performance.
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

from hydratk.core import extension
from hydratk.core import event
from hydratk.core.masterhead import PYTHON_MAJOR_VERSION
from hydratk.lib.console.commandlinetool import CommandlineTool
from hydratk.lib.console.commandlinetool import rprint
from hydratk.lib.compat import utils
import datetime as dt
import pprint
import sys
import random

class Extension(extension.Extension):
    __test_results  = {}
    __print_details = False
    
    def _init_extension(self):
        self._ext_id   = 'benchmark'
        self._ext_name = 'BenchMark'
        self._ext_version = '0.1.0'
        self._ext_author = 'Petr Czaderna <pc@hydratk.org>'
        self._ext_year = '2013'  
        
    def _register_actions(self):
        self._mh.match_cli_command('start-benchmark')        
        hook = [{'command' : 'start-benchmark', 'callback' : self.start_bench_fc }]        
        self._mh.register_command_hook(hook)
        self._mh.match_long_option('details')
    
    def _setup_params(self):
        self.__print_details = True if CommandlineTool.get_input_option('--details') == True else False
            
    def start_bench_fc(self):
        self._mh.dmsg('htk_on_debug_info','received start benchmark command', self._mh.fromhere())
        self._setup_params()
        self._run_basic_tests()
        if (self.__print_details):
            self._print_test_info()
        
        
    def _run_basic_tests(self):
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('benchmark_basic_test_run'), self._mh.fromhere())        
        rprint(self._mh._trn.msg('benchmark_single_cpu_calculations'))        
        self._factorial_test()
        rprint('.')
        self._fib_test()
        rprint('.')
        self._calc_flops_test()
        rprint(".")
        self._event_thru_test()
        rprint(".\n")
        
    def _print_test_info(self):                
        for test_name, test_value in self.__test_results.items():
            print(test_name + ": "+ test_value.__str__())        
    
    def event_test_cb1(self, oevent):        
        x = oevent.get_data('random')        
        return True
    
    def _event_thru_test(self):
        t_start = dt.datetime.now()
        hook = {}
        hook[0] = {'event' : 'benchmark_test_event1', 'callback' : self.event_test_cb1, 'unpack_args' : True}                      
        self._mh.register_event_hook(hook)
        
        '''figurout the xrange compatiblity'''
        rangefc = xrange if PYTHON_MAJOR_VERSION == 2 else range
            
        for i in rangefc(10000000):
            oevent = event.Event('benchmark_test_event1')
            num = random.randint(0,9)
            oevent.set_data('random', ('%s' % str(num)) * 1024)
            self._mh.fire_event(oevent)        
        t_end = dt.datetime.now()
        duration = (t_end - t_start)
        self.__test_results['1Kb data Event througput(10 000 000)'] = duration.microseconds.__float__() / 1000000 
            
    def _factorial_test(self):             
        n            = 10000
        a            = 1
        check_cycles = 10
        delta_list   = []
        low          = None
        high         = None
        while(a <= check_cycles):            
            base = 1
            t_start = dt.datetime.now()
            for i in range(n,0,-1):
                base = base * i
            t_end = dt.datetime.now()
            duration = (t_end - t_start)
            delta_list.append(duration)
            if high == None and low == None:
                high = duration
                low = duration
            else:
                if duration > high: high = duration
                elif duration < low: low = duration
             
            a = a+1
        avg   = sum(delta_list, dt.timedelta()) / len(delta_list)    
        savg  = (avg.seconds.__float__() + (avg.microseconds.__float__() / 1000000)).__str__()
        shigh = (high.seconds.__float__() + (high.microseconds.__float__() / 1000000)).__str__()
        slow  = (low.seconds.__float__() + (low.microseconds.__float__() / 1000000)).__str__()         
        sduration = self._mh._trn.msg('benchmark_factorial_results',savg, shigh, slow)
        self.__test_results['Factorial('+n.__str__()+')'] = sduration   
    
    def __fibcalc(self, n):
        a,b = 1,1
        for i in range(n-1):
            a,b = b,a+b
        return a
 
    def _fib_test(self):
        check_cycles = 10
        delta_list   = []
        low          = None
        high         = None
        n            = 10000
        c            = 1
        while(c <= check_cycles):
            t_start = dt.datetime.now()
            result = self.__fibcalc(n)               
            t_end = dt.datetime.now()
            duration = (t_end - t_start)
            delta_list.append(duration)
            if high == None and low == None:
                high = duration
                low = duration
            else:
                if duration > high: high = duration
                elif duration < low: low = duration
            c = c+1
        avg   = sum(delta_list, dt.timedelta()) / len(delta_list)    
        savg  = (avg.seconds.__float__() + (avg.microseconds.__float__() / 1000000)).__str__()
        shigh = (high.seconds.__float__() + (high.microseconds.__float__() / 1000000)).__str__()
        slow  = (low.seconds.__float__() + (low.microseconds.__float__() / 1000000)).__str__()                
        sduration = self._mh._trn.msg('benchmark_fibonacci_results',savg, shigh, slow)
        self.__test_results['Fibonacci('+n.__str__()+')'] = sduration
        
        
    def _calc_flops_test(self):        
        delta_list      = []
        low             = None
        high            = None
        check_cycles    = 10
        float_increment = 0.0000000000019346 # random
        c               = 1
        while(c <= check_cycles):
            t_start = dt.datetime.now()            
            start = 57.240000 # random
            floating_point = start          
            for i in utils.range(1000000000):                            
                floating_point += float_increment
                  
            t_end = dt.datetime.now()
            duration = (t_end - t_start)
            delta_list.append(duration)
            if high == None and low == None:
                high = duration
                low = duration
            else:
                if duration > high: high = duration
                elif duration < low: low = duration
            c = c+1
        avg   = sum(delta_list, dt.timedelta()) / len(delta_list)    
        savg  = (avg.seconds.__float__() + (avg.microseconds.__float__() / 1000000)).__str__()
        shigh = (high.seconds.__float__() + (high.microseconds.__float__() / 1000000)).__str__()
        slow  = (low.seconds.__float__() + (low.microseconds.__float__() / 1000000)).__str__()      
        sduration = self._mh._trn.msg('benchmark_flops_results',savg, shigh, slow)
        self.__test_results['1 GFLOP'] = sduration
        
