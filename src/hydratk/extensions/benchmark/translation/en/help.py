# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.extensions.benchmark.translation.en.help
   :platform: Unix
   :synopsis: English language translation for Benchmark extension help generator
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
language = {
  'name' : 'English',
  'ISO-639-1' : 'cs'
} 

''' Benchmark Commands '''
help_cmd = {
    'start-benchmark' : 'starts benchmark'
}

''' Benchmark Options '''
help_opt = { 
    'details' : { '{h}--details{e}' : { 'description' : 'displays detailed information about tests', 'commands' : ('start-benchmark')}}
}

