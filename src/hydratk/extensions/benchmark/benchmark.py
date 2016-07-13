# -*- coding: utf-8 -*-
"""Benchmark extension for tuning and testing hydra toolkit performance

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
    """Class Extensions
    """
    
    _test_results  = {}
    _print_details = False
    _check_cycles  = 10
    
    def _init_extension(self):
        """Method initializes extension
        
        Args:      
           none      
           
        Returns:
           void    
                
        """        
          
        self._ext_id   = 'benchmark'
        self._ext_name = 'BenchMark'
        self._ext_version = '0.1.0'
        self._ext_author = 'Petr Czaderna <pc@hydratk.org>'
        self._ext_year = '2013 - 2016'  
        
    def _register_actions(self):
        """Method registers actions
        
        Callback for command start-benchmark
        
        Args:     
           none       
           
        Returns:
           void    
                
        """  
                
        self._mh.match_cli_command('start-benchmark')        
        hook = [{'command' : 'start-benchmark', 'callback' : self.start_bench_fc }]        
        self._mh.register_command_hook(hook)
        self._mh.match_long_option('details')
    
    def _setup_params(self):
        """Method sets parameters
        
        Command option --details
        
        Args:   
           none         
           
        Returns:
           void    
                
        """  
                
        self._print_details = True if CommandlineTool.get_input_option('--details') == True else False
            
    def start_bench_fc(self):
        """Method handles command start-benchmark
        
        Args:  
           none          
           
        Returns:
           void    
                
        """  
                
        self._mh.dmsg('htk_on_debug_info','received start benchmark command', self._mh.fromhere())
        self._setup_params()
        self._run_basic_tests()
        if (self._print_details):
            self._print_test_info()
            
    def _run_basic_tests(self):
        """Method runs basic tests
        
        Args: 
           none           
           
        Returns:
           void    
                
        """  
                
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
        """Method prints test results
        
        Args: 
           none           
           
        Returns:
           void    
                
        """  
                              
        for test_name, test_value in self._test_results.items():
            print(test_name + ": "+ test_value.__str__())        
    
    def event_test_cb1(self, oevent):  
     
        x = oevent.get_data('random')        
        return True
    
    def _event_thru_test(self):
        """Method tests event throughput
        
        Args:  
           none          
           
        Returns:
           void    
           
        Raises:
           event: benchmark_test_event1
                
        """  
                
        t_start = dt.datetime.now()
        hook = {}
        hook[0] = {'event' : 'benchmark_test_event1', 'callback' : self.event_test_cb1, 'unpack_args' : True}                      
        self._mh.register_event_hook(hook)
        
        '''figure out the xrange compatiblity'''
        rangefc = xrange if PYTHON_MAJOR_VERSION == 2 else range
            
        for i in rangefc(10000000):
            oevent = event.Event('benchmark_test_event1')
            num = random.randint(0,9)
            oevent.set_data('random', ('%s' % str(num)) * 1024)
            self._mh.fire_event(oevent)        
        t_end = dt.datetime.now()
        duration = (t_end - t_start)
        self._test_results['1Kb data Event througput(10 000 000)'] = duration.microseconds.__float__() / 1000000 
            
    def _factorial_test(self):   
        """Method tests factorial caluculation
        
        Args:  
           none          
           
        Returns:
           void    
                
        """ 
                          
        n            = 10000
        a            = 1
        delta_list   = []
        low          = None
        high         = None
        while(a <= self._check_cycles):            
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
        self._test_results['Factorial('+n.__str__()+')'] = sduration   
    
    def __fibcalc(self, n):
        """Method calculates Fibonacci number
        
        Args:         
           n (int): nth number   
           
        Returns:
           int: number    
                
        """ 
                
        a,b = 1,1
        for i in range(n-1):
            a,b = b,a+b
        return a
 
    def _fib_test(self):
        """Method tests Fibonacci calculation
        
        Args: 
           none           
           
        Returns:
           void    
                
        """ 
                
        delta_list   = []
        low          = None
        high         = None
        n            = 10000
        c            = 1
        while(c <= self._check_cycles):
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
        self._test_results['Fibonacci('+n.__str__()+')'] = sduration
        
        
    def _calc_flops_test(self):  
        """Method tests arithmetic operations with floating point
        
        Args: 
           none           
           
        Returns:
           void    
                
        """ 
                      
        delta_list      = []
        low             = None
        high            = None
        float_increment = 0.0000000000019346 # random
        c               = 1
        while(c <= self._check_cycles):
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
        self._test_results['1 GFLOP'] = sduration
        
