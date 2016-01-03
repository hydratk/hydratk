# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit library

.. module:: lib.data.jsongen
   :platform: Unix
   :synopsis: Module for sample JSON generation from JSON schema
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from jsonlib2 import read, write
from os import path

class JSONGen():
    
    _path = None
    _schema = None
    
    @property
    def path(self):
        
        return self._path
    
    @property
    def schema(self):
        
        return self._schema
    
    def import_schema(self, filename):
        """Method imports schema
        
        Args:
            filename (str): filename
        
        Raises:
            error: ValueError     
                
        """     
    
        if (path.exists(filename)):
            self._path = path.dirname(path.abspath(filename))           
            with open(filename, 'r') as f:                                         
                self._schema = read(f.read())            
        else:
            raise ValueError('File {0} not found'.format(filename)) 
        
    def tojson(self):
        """Method creates sample json

        Returns:
            str: sample json
        
        Raises:
            error: ValueError     
                
        """  
    
        if (self._schema == None):
            raise ValueError('Schema is not imported yet')                   
            
        doc = self._tojson_rec()
            
        return write(doc, indent = '    ')
    
    def _tojson_rec(self, schema=None):
        """Method creates sample json document
        
        It is used in recursive traversal
        
        Args:
            schema (json): json schema object

        Returns:
            str: sample json
        
        Raises:
            error: ValueError     
                
        """          
        
        if (self._schema == None):
            raise ValueError('Schema is not imported yet')     
        
        if (schema == None):
            schema = self._schema
        
        if (schema['type'] == 'object'):
            doc = {}
            for key, subelem in schema['properties'].items():
                
                if (subelem.has_key('$ref')):
                    subelem = self._import_ref_schema(subelem['$ref'])
                    
                if (subelem['type'] == 'array'):
                    doc[key] = []
                    doc[key].append(self._tojson_rec(subelem['items']))
                elif (subelem['type'] == 'object'):
                    doc[key] = self._tojson_rec(subelem)
                else:
                    doc[key] = '?'
        elif (schema['type'] == 'array'):
            doc = []
            doc.append(self._tojson_rec(schema['items']))
        else:
            doc = '?'
                            
        return doc  
    
    def _import_ref_schema(self, uri):
        """Method imports referenced schema    

        local schema is required, http is not supported

        Args:
           uri (str): file uri, absolute path or filename

        Returns:
            json: json schema
        
        Raises:
            error: ValueError     
                
        """          
        
        filename = uri if (not 'file://' in uri) else uri[7:]  
        if (not '/' in filename):
            filename = path.join(self._path, filename)
            
        if (path.exists(filename)):
            with open(filename, 'r') as f:                                         
                ref_schema = read(f.read())
               
            return ref_schema             
        else:
            raise ValueError('File {0} not found'.format(filename))    