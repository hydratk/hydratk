"""This code is a part of Hydra Toolkit

.. module:: hydratk.extensions.wings
   :platform: Unix
   :synopsis: Web frontend functionality
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

from hydratk.core import extension;

class Extension(extension.Extension):    
    
    def _init_extension(self):
        self._ext_id      = 'wings';
        self._ext_name    = 'Wings';
        self._ext_version = '0.1.0';
        self._ext_author  = 'Petr Czaderna <pc@hydratk.org>';
        self._ext_year    = '2015';  
        
    def _check_dependencies(self):
        return True;
    
    def _do_imports(self):
        pass
    
    def _export_messages(self): 
        pass
    
    def _register_actions(self):
        hook = [
                #{'event' : 'h_^on_cmd_options', 'callback' : self.event_test },
                {'event' : '$htk_on_cmd_options', 'callback' : self.event_test },
                #{'event' : 'htk_on_cmd_options', 'callback' : self.event_test },                
                #{'event' : '^h_before_cmd_options', 'callback' : self.event_test },
                #{'event' : 'h_before_cmd_options', 'callback' : self.event_test },
                ];        
        self._mh.register_event_hook(hook);
        
    def event_test(self,ev):
        print('++++ got event %s, target %s' % (ev.id(),ev.get_data('target_event').id()));