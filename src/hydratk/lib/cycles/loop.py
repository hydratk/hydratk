# -*- coding: utf-8 -*-
"""Module with functions for cyclic data manipulation and verification

.. module:: lib.data.loop
   :platform: Unix
   :synopsis: Module with functions for cyclic data manipulation and verification
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
import time


def do_until(call, until_call_result, delay=1, until_max_attempts=10, until_duration=None, until_exact_time=None):
    """Function emulates do..until condition loop
     
    Args:
       call (tuple): function call in format (callable, param1, param2 ..)              
       until_call_result (mixed): function call result stop loop value
       delay (mixed): int, float, None - delay between cycles   
       until_max_attempts(mixed): int, None - max call attempts stop loop value
       until_duration(mixed): int, float, None - callback repeating duration limit stop loop value
       until_exact_time(mixed): int, float, None - callback repeating till exact time stop loop value
       
    Returns:
       void
       
    Raises:
       error: ValueError
   
    Example:
     
    .. code-block:: python  
     
         from hydratk.lib.cycles.loop import do_until                                                    
         import random
         
         def test(x,y):
             rv = random.randint(x,y)
             print("Random value {0}".format(rv))
             return rv
             
         do_until(
            call               = (test,0,5),
            delay              = None,
            until_call_result  = 1,
            until_max_attempts = 30,
            until_duration     = 10
         )
        
         
    """
    if type(call).__name__ != 'tuple': raise ValueError('callback: function or tuple expected')
    if not callable(call[0]): raise ValueError('callback tuple: callable parameter expected')
    if type(delay).__name__ not in ('int','float', 'NoneType') : raise ValueError('delay: integer,float or None expected')
    if type(until_max_attempts).__name__ not in ('int', 'NoneType') : raise ValueError('delay: integer or None expected')
    if type(until_duration).__name__ not in ('int', 'float','NoneType'): raise ValueError('until_duration: integer, float or None expected, got {0}'.format(until_duration))
    if type(until_exact_time).__name__ not in ('int', 'float','NoneType'): raise ValueError('until_exact_time: integer, float or None expected, got {0}'.format(until_exact_time))
    if until_duration is not None: 
        till_time = time.time() + until_duration
    attempts = 1    
    while True:
        if until_call_result == call[0](*call[1:]):            
            break
        if until_max_attempts is not None:
            if attempts >= until_max_attempts:                
                break
            else: attempts += 1
        if until_duration is not None:
            if time.time() >= till_time:                
                break
        if until_exact_time is not None:
            if time.time() >= until_exact_time:                
                break                     
        if delay is not None:
            time.sleep(delay)

