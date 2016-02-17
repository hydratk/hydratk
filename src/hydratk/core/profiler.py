# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit

.. module:: core.profiler
   :platform: Unix
   :synopsis: HydraTK core integrated profiler
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
import cProfile

class Profiler(object):
    _pr = None
    
    def __init__(self):
        self._pr = cProfile.Profile()
    
    def start(self):
        self._pr.enable()
    
    def finish(self):
        self._pr.disable()
    
    def _configure_profiler(self):
        from hydratk.core import commands
        commands.long_opts.append('profile')
        commands.short_opts += 'p'
        commands.getopt_long_opts.append('profile=')
        commands.getopt_short_opts += 'p:'

    def _create_profiler_stats(self):
        import StringIO, pstats
        s = StringIO.StringIO()
        sortby = 'cumulative'
        #ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        #ps.dump_stats(stats_file)