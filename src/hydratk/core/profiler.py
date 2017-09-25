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
        
        result = False
        i = 0        
        for o in sys.argv:            
            if o == '-p' or o == '--profile':
                if sys.argv.index(o) < (len(sys.argv) - 1):
                    self._output_file = sys.argv[i + 1]
                    result = True
            i = i + 1
        return result
    
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

        from hydratk.core import commandopt
        commandopt.long_opt['htk'].append('profile')
        commandopt.short_opt['htk'].append('p')
        commandopt.d_opt['htk'].append('profile')
        commandopt.opt['htk']['-p'] = {
            'd_opt': 'profile',
            'has_value': True,
            'allow_multiple': False
        }
        commandopt.opt['htk']['--profile'] = {
            'd_opt': 'profile',
            'has_value': True,
            'allow_multiple': False
        }

    def create_profiler_stats(self):       
        import StringIO
        import pstats
        from hydratk.core.masterhead import MasterHead
        from hydratk.lib.system.fs import file_put_contents
        mh = MasterHead.get_head()
        s = StringIO.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(self._pr, stream=s).sort_stats(sortby)        
        if self.check_profile_param():
            mh.dmsg('htk_on_debug_info', "Writing profiler stats output to {0}".format(self._output_file), mh.fromhere())
            ps.dump_stats(self._output_file)
            ps.print_stats()
            file_put_contents(self._output_file+'.log', s.getvalue())
        else:
            mh.dmsg('htk_on_debug_info', "Writing profiler stats outpout to screen", mh.fromhere())
            ps.strip_dirs()
            ps.print_stats()
            print s.getvalue()           
