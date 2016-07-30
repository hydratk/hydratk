# -*- coding: utf-8 -*-
"""HydraTK core integrated profiler

.. module:: core.profiler
   :platform: Unix
   :synopsis: HydraTK core integrated profiler
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
import cProfile

class Profiler(object):
    """Class Profiler
    """
    
    _pr = None
    
    def __init__(self):
        """Class constructor
        
        Called when object is initialized
        
        Args:
           none

        """
                
        self._pr = cProfile.Profile()
        self._configure_profiler()
    
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
    
    def _configure_profiler(self):
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
                                        'd_opt'          : 'profile',
                                        'has_value'      : True,
                                        'allow_multiple' : False                           
                                      }
        commandopt.opt['htk']['--profile'] = {
                                        'd_opt'          : 'profile',
                                        'has_value'      : True,
                                        'allow_multiple' : False                           
                                      }         

    def _create_profiler_stats(self):
        import StringIO, pstats
        s = StringIO.StringIO()
        sortby = 'cumulative'
        #ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        #ps.dump_stats(stats_file)