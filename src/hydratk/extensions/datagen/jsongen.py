# -*- coding: utf-8 -*-
"""Module for sample JSON generation from JSON schema

.. module:: datagen.jsongen
   :platform: Unix
   :synopsis: Module for sample JSON generation from JSON schema
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
jsongen_before_import_spec
jsongen_after_import_spec
jsongen_before_write
jsongen_after_write

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from jsonlib2 import read, dump
from os import path

class JSONGen():
    """Class JSONGen
    """
    
    _mh = None
    _path = None
    _schema = None
    
    def __init__(self):
        """Class constructor
        
        Called when object is initialized
        
        Args:
           none              
                
        """          
        
        self._mh = MasterHead.get_head()
    
    @property
    def path(self):
        """ path property getter """
        
        return self._path
    
    @property
    def schema(self):
        """ schema property getter """
        
        return self._schema
    
    def import_schema(self, filename):
        """Method imports schema
        
        Args:
            filename (str): filename
            
        Returns:
            bool: result
        
        Raises:
            event: jsongen_before_import_spec
            event: jsongen_after_import_spec     
                
        """     
    
        try:
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('datagen_jsongen_import_spec', filename), self._mh.fromhere()) 
            ev = event.Event('jsongen_before_import_spec', filename)
            if (self._mh.fire_event(ev) > 0):
                filename = ev.argv(0)    
    
            if (ev.will_run_default()):     
                if (path.exists(filename)):
                    self._path = path.dirname(path.abspath(filename))           
                    with open(filename, 'r') as f:                                         
                        self._schema = read(f.read())            
                else:
                    raise ValueError('File {0} not found'.format(filename))
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('datagen_jsongen_spec_imported'), self._mh.fromhere())   
            ev = event.Event('jsongen_after_import_spec')
            self._mh.fire_event(ev)            
            
            return True
            
        except ValueError, ex:
            print ex
            return False            
        except Exception, ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False             
        
    def tojson(self, outfile=None):
        """Method creates sample json file
        
        Args:
            outfile (str): output filename, default sample.json

        Returns:
            bool: result
        
        Raises:
            error: ValueError    
            event: jsongen_before_write
            event: jsongen_after_write 
                
        """  

        try:
    
            if (self._schema == None):
                raise ValueError('Schema is not imported yet') 
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('datagen_jsongen_write_sample'), self._mh.fromhere()) 
            ev = event.Event('jsongen_before_write', outfile)
            if (self._mh.fire_event(ev) > 0):
                outfile = ev.argv(0) 
                
            if (ev.will_run_default()):                               
                doc = self._tojson_rec()                
                outfile = 'sample.json' if (outfile == None) else outfile
                with open(outfile, 'w') as f: 
                    dump(doc, f, indent=4)
    
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('datagen_jsongen_sample_written', outfile), self._mh.fromhere())   
            ev = event.Event('jsongen_after_write')
            self._mh.fire_event(ev)            
            
            return True    
    
        except Exception, ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False          
    
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