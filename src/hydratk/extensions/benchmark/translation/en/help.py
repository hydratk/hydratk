# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.extensions.benchmark.translation.en.help
   :platform: Unix
   :synopsis: English language translation for Benchmark extension help generator
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
language = {
    'name': 'English',
    'ISO-639-1': 'cs'
}

''' Benchmark Commands '''
help_cmd = {
    'benchmark': 'Run benchmark'
}

''' Benchmark Options '''
help_opt = {
    'bench-groups': {'{h}[--bench-groups <title>]{e}': {'description': 'test groups, grp1,grp2,... , default all', 'commands': ('benchmark')}},
    'bench-cycles': {'{h}[--bench-cycles <num>]{e}': {'description': 'count of measurement cycles, default 20', 'commands': ('benchmark')}},
    'bench-out': {'{h}[--bench-out <file>]{e}': {'description': 'output filename, default not generated', 'commands': ('benchmark')}},
    'bench-gc': {'{h}[--bench-gc]{e}': {'description': 'enable garbage collector, default False', 'commands': ('benchmark')}}
}
