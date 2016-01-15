# -*- coding: utf-8 -*-
"""This code is a part of Datagen extension

.. module:: datagen.asn1.codec
   :platform: Unix
   :synopsis: Module for ASN.1 codec
              Libraries for ASN.1 were taken from https://github.com/mitshell/libmich
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
asn1_before_import_spec
asn1_after_import_spec
asn1_before_encode
asn1_after_encode
asn1_before_decode
asn1_after_decode

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from libmich.asn1.processor import process_modules
from libmich.asn1.ASN1 import ASN1Obj
from libmich.asn1.BER import BER
from os import path
from jsonlib2 import read, dump
from collections import OrderedDict

class ASN1Codec():
    
    _mh = None
    _spec = None
    _elements = None
    
    def __init__(self):
        
        self._mh = MasterHead.get_head()
    
    @property
    def spec(self):
        
        return self._spec
    
    @property
    def elements(self):
        
        return self._elements
    
    def __str__(self):
        
        return self._spec._text_def 
    
    def import_spec(self, filename):
        """Method imports specification
        
        Args:
            filename (str): filename
            
        Returns:
            bool: result
        
        Raises:
            error: ValueError  
            event: asn1_before_import_spec
            event: asn1_after_import_spec   
                
        """     
    
        try:
    
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('datagen_asn1_import_spec', filename), self._mh.fromhere()) 
            ev = event.Event('asn1_before_import_spec', filename)
            if (self._mh.fire_event(ev) > 0):
                filename = ev.argv(0)
                
            if (ev.will_run_default()):        
                if (path.exists(filename)):
                    with open(filename, 'r') as f:                                         
                        self._spec = process_modules(f.read())  
                        self._elements = self._spec[0]['TYPE']._dict
                        
                        ASN1Obj._SAFE = True
                        ASN1Obj._RET_STRUCT = True
                        ASN1Obj.CODEC = BER                                                 
                else:
                    raise ValueError('File {0} not found'.format(filename))      
                
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('datagen_asn1_spec_imported'), self._mh.fromhere())   
            ev = event.Event('asn1_after_import_spec')
            self._mh.fire_event(ev)
                    
            return True                             
        
        except Exception, ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False
        
    def encode(self, infile, element, outfile=None):
        """Method encodes json file to binary 
        
        Args:
            infile (str): input filename
            element (str): element name
            outfile (str): output filename, default infile with suffix bin
            
        Returns: 
            bool: result
        
        Raises:
            error: ValueError   
            event: asn1_before_encode
            event: asn1_after_encode  
                
        """         
        
        try:
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('datagen_asn1_encode', infile), self._mh.fromhere()) 
            ev = event.Event('asn1_before_encode', infile, outfile)
            if (self._mh.fire_event(ev) > 0):
                infile = ev.argv(0)
                outfile = ev.argv(1)        
        
            if (ev.will_run_default()): 
                if (path.exists(infile)):
                    self._path = path.dirname(path.abspath(infile))           
                    with open(infile, 'r') as f: 
                        objects = read(f.read())
                        if (objects.__class__.__name__ == 'list'):
                            input = []
                            for record in objects:
                                input.append(self._update_datatypes(record))
                        else:                                        
                            input = [self._update_datatypes(objects)]     
                                     
                    outfile = infile.split('.')[0]+'.bin' if (outfile == None) else outfile               
                    with open(outfile, 'wb') as f:
                        for record in input:
                            output = self._elements[element].encode(record)
                            f.write(str(output()))                                                         
                else:
                    raise ValueError('File {0} not found'.format(infile))
                
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('datagen_asn1_encoded', outfile), self._mh.fromhere())   
            ev = event.Event('asn1_after_encode')
            self._mh.fire_event(ev)
                    
            return True                 
        
        except Exception, ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())   
            return False     
        
    def decode(self, infile, element, outfile=None):
        """Method decodes binary file to json
        
        Args:
            infile (str): input filename
            element (str): element name
            outfile (str): output filename, default infile with suffix json
            
        Returns:
            bool: result
        
        Raises:
            error: ValueError
            event: asn1_before_decode
            event: asn1_after_decode     
                
        """         
        
        try:
        
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('datagen_asn1_decode', infile), self._mh.fromhere()) 
            ev = event.Event('asn1_before_decode', infile, outfile)
            if (self._mh.fire_event(ev) > 0):
                infile = ev.argv(0)
                outfile = ev.argv(1)           
        
            if (ev.will_run_default()): 
                if (path.exists(infile)):
                    self._path = path.dirname(path.abspath(infile))           
                    with open(infile, 'rb') as f:                                         
                        input = f.read()
                
                    outfile = infile.split('.')[0]+'.json' if (outfile == None) else outfile     
                    with open(outfile, 'w') as f:                       
                        records = self._split_records(input)

                        if (len(records) > 1):
                            output = []
                            for record in records:
                                self._elements[element].decode(record)
                                output.append(self._create_dict(self._elements[element]))
                        else:             
                            self._elements[element].decode(records[0])
                            output = self._create_dict(self._elements[element])
                        dump(output, f, indent=4)                                                      
            else:
                raise ValueError('File {0} not found'.format(infile)) 
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('datagen_asn1_decoded', outfile), self._mh.fromhere())   
            ev = event.Event('asn1_after_decode')
            self._mh.fire_event(ev)
                    
            return True              
        
        except ValueError, ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())  
            return False             
        
    def _update_datatypes(self, obj):
        """Method updates datatypes
        
        It is used in encoder, some datatypes can't be encoded
        The object is traversed recursively
        
        Args:
            obj (json): particular json object  
            
        Returns:
            json: json object
                
        """           

        for key, value in obj.items():
            
            classname = value.__class__.__name__
            if (classname == 'long'):
                obj[key] = int(value) 
            elif (classname == 'unicode'):
                obj[key] = str(value)
            elif (classname == 'dict'):
                obj[key] = self._update_datatypes(obj[key])
                
        return obj  
    
    def _split_records(self, input):
        """Method splits records from input file
        
        Args:
            input (str): file contents
            
        Returns:
            list: list of records
                
        """           
        
        records = []
        input = bytearray(input)
        
        i = 0
        while (i < len(input)):
            rec_size = input[i+1]
            idx = i+rec_size+2
            records.append(str(input[i:idx]))
            i = idx
         
        return records
    
    def _create_dict(self, obj, val=None, output=None):
        """Method creates dictionary according to spec
        
        It is used in decoder, objects are ordered as specified
        The object is traversed recursively
        
        Args:
            obj (obj): particular ASN1 object
            val (obj): element value
            output (dict): particular output
            
        Returns:
            dict: ordered dictionary object 
                
        """          
        
        if (val == None):
            val = obj._val 
        if (output == None):
            output = OrderedDict()   
                  
        if (obj._type in ('SEQUENCE', 'SET')):
            for key in obj._cont._index:
                output[key] = OrderedDict()
                output[key] = self._create_dict(obj._cont._dict[key], val[key], output[key])
        else:
            output = val 
            
        return output  