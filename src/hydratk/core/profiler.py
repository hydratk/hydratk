# -*- coding: utf-8 -*-
"""HydraTK core integrated profiler

.. module:: core.profiler
   :platform: Unix
   :synopsis: HydraTK core integrated profiler
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import cProfile
import sys
import os
from hydratk.lib.profiling.profiler import Profiler as HTKProfiler

sort_by_keys = [
           'calls',      #call count
           'cumulative', #cumulative time
           'cumtime',    #cumulative time
           'file',       #file name
           'filename',   #file name
           'module',     #file name
           'ncalls',     #call count
           'pcalls',     #primitive call count 
           'line',       #line number
           'name',       #function name
           'nfl',        #name/file/line
           'stdname',    #standard name
           'time',       #internal time
           'tottime'     #internal time      
           ]
class Profiler(HTKProfiler,object):
    """Class Profiler
    """

    def __init__(self):
        """Class constructor

        Called when object is initialized

        Args:
           none

        """        
        super(Profiler, self).__init__()
        
        self._pr = cProfile.Profile()
        self._configure_profiler_options()
    
    def check_profile_param(self):
        """Method checks for home parameter presence --home or -h to replace htk_root_dir location
        
        Args:
           none
        
        Returns:            
           bool: htk_root_changed 
        
        """
        
        import re    
        i = 0        
        for o in sys.argv:                    
            if o in ('-p','--profiler'):            
                return (True, sys.argv[i + 1])
            else:            
                m = re.match(r"--profiler\=(.*)", o)
                if m:                
                    return (True, m.group(1).strip())
            i = i + 1
        return (False,None)
    
    def start(self):
        """Method starts profiler

        Args:
           none

        Returns:            
           void

        """
        self._pr.enable()

    def finish(self):
        """Method stops profiler

        Args:
           none

        Returns:            
           void

        """
        self._pr.disable()

    def _configure_profiler_options(self):
        """Method sets profiler command line configuration (options -p, --profile)

        Args:
           none

        Returns:            
           void

        """
        pass

    def create_profiler_stats(self, stats_file=None):               
        import StringIO
        import pstats
        from hydratk.core.masterhead import MasterHead
        from hydratk.lib.system.fs import file_put_contents
        from hydratk.lib.console.commandlinetool import CommandlineTool
        
        if stats_file not in (None,''):
            self._output_file = stats_file
        mh = MasterHead.get_head()
        sortby = CommandlineTool.get_input_option('pstats-sort-by')
        strip_dirs = CommandlineTool.get_input_option('pstats-strip-dirs')        
        s = StringIO.StringIO()
        if sortby == False:
            sortby = 'cumulative'
        else:
            sortby = sortby.split(',')
        mh.demsg('htk_on_debug_info', "Sorting stats using column(s): {0}".format(','.join(sortby)), mh.fromhere())
        if type(sortby).__name__ == 'str':
            ps = pstats.Stats(self._pr, stream=s).sort_stats(sortby)
        elif type(sortby).__name__ == 'list':
            ps = pstats.Stats(self._pr, stream=s).sort_stats(*sortby)                                           
        mh.demsg('htk_on_debug_info', "Writing profiler stats output to {0}".format(self._output_file), mh.fromhere())
        ps.dump_stats(self._output_file)
        if strip_dirs:
            ps.strip_dirs()
        ps.print_stats()        
        file_put_contents(self._output_file+'.log', s.getvalue())                   
