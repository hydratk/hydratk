# -*- coding: utf-8 -*-
"""This code is a part of Wings extension

.. module:: wings.wings
   :platform: Unix
   :synopsis: Web frontend functionality
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

from hydratk.core import extension

class Extension(extension.Extension):    
    _http_service_status      = None
    _http_service_parent_conn = None
    
    def _init_extension(self):
        self._ext_id      = 'wings'
        self._ext_name    = 'Wings'
        self._ext_version = '0.1.0'
        self._ext_author  = 'Petr Czaderna <pc@hydratk.org>'
        self._ext_year    = '2015'  
        
    def _check_dependencies(self):
        return True
    
    def _do_imports(self):
        pass    
    
    def _register_actions(self):
        pass
        #hook = [
                #{'event' : 'h_^on_cmd_options', 'callback' : self.event_test },
                #{'event' : '$htk_on_cmd_options', 'callback' : self.event_test },
                #{'event' : 'htk_on_cmd_options', 'callback' : self.event_test },                
                #{'event' : '^h_before_cmd_options', 'callback' : self.event_test },
                #{'event' : 'h_before_cmd_options', 'callback' : self.event_test },
        #        ]        
        #self._mh.register_event_hook(hook)
        
    
    def _reg_signal_hooks(self):        
        hook = {}                
        hook[0] = {'event' : 'htk_on_sigpipe', 'callback' : self.check_pipe } 
        hook[1] = {'event' : 'htk_on_sigint', 'callback' :  self.stop_service }
        hook[2] = {'event' : 'htk_on_sigterm', 'callback' : self.stop_service }           
        self._mh.register_event_hook(hook)

    def stop_service(self, oevent):
        cherrypy.engine.exit()
        
    def wings_http_service(self, service_status, parent_conn):        
        self._mh.dmsg('htk_on_debug_info', "Start operating", self._mh.fromhere())
        self._http_service_status       = service_status  
        self._http_service_status.value = const.SERVICE_STATUS_STARTED
        self._http_service_parent_conn  = parent_conn
        self._reg_signal_hooks()
        wsrv = WebServer.get_instance()
        self._http_service_set_config(wsrv)        
        wsrv.init()    
        
        while(self.__service_status.value == const.SERVICE_STATUS_STARTED):
            cherrypy.engine.start()
            cherrypy.engine.block()
            
        self._mh.dmsg('h_on_debug_info', "Stopping service", self._mh.fromhere())