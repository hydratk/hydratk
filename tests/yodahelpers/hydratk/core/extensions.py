from hydratk.core.extension import Extension

class DummyExtension(Extension):
    
    def _init_extension(self):    
    
        self._ext_id = 'test_01'
        self._ext_name = 'test_ext'
        self._ext_version = '0.1.0'
        self._ext_author = 'bowman@hydratk.org'
        self._ext_year = '2016'
        self._wrap_hydra_attrs = True

    def _check_dependencies(self):
        
        self._deps = True
    
    def _register_actions(self):
        
        self._actions = True
    
    def _do_imports(self):
        
        self._imports = True