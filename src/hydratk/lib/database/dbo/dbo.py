dbo_drivers = {
               'mysql'  : 'hydratk.lib.database.dbo.drivers.mysql',
               'oracle' : 'hydratk.lib.database.dbo.drivers.oracle',
               'pgsql'  : 'hydratk.lib.database.dbo.drivers.pgsql',
               'sqlite' : 'hydratk.lib.database.dbo.drivers.sqlite'                
              }

class DBO(object):
    _dbi = None
    
    def __init__(self, dsn, username=None, password=None, options=None):
        '''
        Args: 
           dsn (string): format: dbdriver:db_string        
           
        '''
        def __getattr__(self,name):        
            if hasattr(self._mh, name):
                return self._mh[name]