# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.extensions.benchmark.translation.cs.help
   :platform: Unix
   :synopsis: Czech language translation for Benchmark extension help generator
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
language = {
  'name' : 'Čeština',
  'ISO-639-1' : 'cs'
} 

''' Benchmark Commands '''
help_cmd = {
    'start-benchmark' : 'Spustí benchmark'
}

''' Benchmark Options '''
help_opt = { 
    'details' : { '{h}--details{e}' : { 'description' : 'zobrazi podrobnejsi informace o testech', 'commands' : ('start-benchmark')}}
}