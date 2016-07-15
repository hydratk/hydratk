# -*- coding: utf-8 -*-
"""HydraTK extensions implementation class

.. module:: core.extension
   :platform: Unix
   :synopsis: HydraTK extensions implementation class
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

class Extension(object):
    """Class Extension
    """
    
    _ext_id            = 'Undefined'
    _ext_name          = 'Undefined'
    _ext_version       = 'Undefined'
    _ext_author        = 'Undefined'
    _ext_year          = 'Undefined'
    ''' MasterHead object reference '''           
    _mh                = None     
    
    def __getattr__(self, name):
        """Method gets required MasterHead attribute
        
        Subclass must have enabled attribute _wrap_hydra_attrs
        
        Args:     
           name (str): attribute name
           
        Returns:
           obj: attribute value
           
        Raises:
           error: AttributeError    
                
        """ 
                
        if hasattr(self, '_wrap_hydra_attrs') and self._wrap_hydra_attrs == True:
            if hasattr(self._mh, name):
                return self._mh.__dict__[name]
        raise AttributeError("'module' object has no attribute '{0}'".format(name))
      
    def __init__(self, core_instance=None):
        """Class constructor
        
        Called when object is initialized
        Set extensions metadata 
        If implemented in subclass - check dependencies, import modules, register actions
        
        Args:     
           core_instance (obj): CoreHead reference      
                
        """ 
                                  
        self._mh = core_instance
        self._init_extension()        
        
        if hasattr(self.__class__, '_check_dependencies') and callable(getattr(self.__class__, '_check_dependencies')):
            self._check_dependencies()
        
        if hasattr(self.__class__, '_do_imports') and callable(getattr(self.__class__, '_do_imports')):
            self._do_imports()        
        
        if hasattr(self.__class__, '_register_actions') and callable(getattr(self.__class__, '_register_actions')):
            self._register_actions()                   

    def get_ext_name(self):
        """Method gets extension name
        
        Args:     
           none
           
        Returns:
           str: name
                
        """ 
                
        return self._ext_name
    
    def get_ext_version(self):
        """Method gets extension version
        
        Args:   
           none  
           
        Returns:
           str: version
                
        """ 
                
        return self._ext_version
    
    def get_ext_author(self):
        """Method gets extension author
        
        Args:  
           none   
           
        Returns:
           str: author
                
        """ 
                
        return self._ext_author
    
    def get_ext_info(self):
        """Method gets extension summary info
        
        Args:
           none     
           
        Returns:
           str: info
                
        """ 
                
        return self._ext_name +' v'+ self._ext_version + ' (c) [' + self._ext_year + ' '+ self._ext_author + ']'    