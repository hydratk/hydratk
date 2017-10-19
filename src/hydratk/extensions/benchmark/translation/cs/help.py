# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.extensions.benchmark.translation.cs.help
   :platform: Unix
   :synopsis: Czech language translation for Benchmark extension help generator
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
language = {
    'name': 'Čeština',
    'ISO-639-1': 'cs'
}

''' Benchmark Commands '''
help_cmd = {
    'benchmark': 'Spustí benchmark'
}

''' Benchmark Options '''
help_opt = {
    'bench-groups': {'{h}[--bench-groups <title>]{e}': {'description': 'skupiny testů grp1,grp2,... , default all', 'commands': ('benchmark')}},
    'bench-cycles': {'{h}[--bench-cycles <num>]{e}': {'description': 'počet cyklů měření, default 20', 'commands': ('benchmark')}},
    'bench-out': {'{h}[--bench-out <file>]{e}': {'description': 'název výstupního souboru, default negenerován', 'commands': ('benchmark')}},
    'bench-gc': {'{h}[--bench-gc]{e}': {'description': 'zapnout garbage collector, default False', 'commands': ('benchmark')}}
}
