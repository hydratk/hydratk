# -*- coding: utf-8 -*-
"""This code is part of Hydra Toolkit library

.. module:: database.dbo
   :platform: Unix
   :synopsis: Complex dabase interface inspired by PHP PDO
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
import importlib

dbo_drivers = {
               'mysql'  : 'hydratk.lib.database.dbo.drivers.mysql',
               'oracle' : 'hydratk.lib.database.dbo.drivers.oracle',
               'pgsql'  : 'hydratk.lib.database.dbo.drivers.pgsql',
               'sqlite' : 'hydratk.lib.database.dbo.drivers.sqlite'                
              }

class DBO(object):
    _dbo_driver  = None
    _driver_name = None
    
    def __init__(self, dsn, username=None, password=None, options={}):
        '''
        Args: 
           dsn (string): format: dbdriver:db_string
           username(string): username
           password(string): password 
           options(dict): driver specific options
           
        Returns:
           DBO: object on success 
           
        Raises:
           DBOException: on error                     
        '''
        
        driver_name = self._get_driver_from_dsn(dsn)
        if driver_name in dbo_drivers:
            self._driver_name = driver_name
            dbo_driver_mod_str = '{0}.driver'.format(dbo_drivers[driver_name])
            dbo_driver_mod = self._import_dbo_driver(dbo_driver_mod_str)
              
            
        else: raise DBOException('Not existing driver: {0}'.format(driver_name))
                
        try:
            self._dbo_driver = dbo_driver_mod.DBODriver(dsn, username, password, options)                        
        
        except Exception as e:
            print(e)     
    
    @property
    def driver_name(self):
        return self._driver_name
    
    def _import_dbo_driver(self, dbo_driver):        
        return importlib.import_module(dbo_driver)
    
    
    def _get_driver_from_dsn(self, dsn):
        return dsn.split(':')[0]
    
    def get_available_drivers(self):
        pass
    
    def __getattr__(self,name):
        return getattr(self._dbo_driver,name)
    
    def __getitem__(self, name):
        return getattr(self._dbo_driver, name)    

class DBOException():
    _error_info = {}
    _code       = None
    _message    = None
    _code       = None
    _file       = None
    _line       = None
    


