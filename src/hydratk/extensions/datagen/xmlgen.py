# -*- coding: utf-8 -*-
"""Module for sample XML generation from WSDL/XSD

.. module:: datagen.xmlgen
   :platform: Unix
   :synopsis: Module for sample XML generation from WSDL/XSD
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
xmlgen_before_import_spec
xmlgen_after_import_spec
xmlgen_before_write
xmlgen_after_write

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
from suds.client import Client, TypeNotFound
from lxml.etree import Element, SubElement, tostring
from os import path
from re import search
from logging import getLogger, CRITICAL

getLogger('suds.resolver').setLevel(CRITICAL)

''' WSDL template '''
wsdl_tmpl = """
<wsdl:definitions targetNamespace="{0}" xmlns:tns="{1}" xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/" 
                  xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/">
   <wsdl:types>
      <xsd:schema attributeFormDefault="qualified" targetNamespace="{2}">
      <xsd:include schemaLocation="{3}"/>      
      </xsd:schema>
   </wsdl:types>
   <wsdl:portType name="dummyPort">
   </wsdl:portType>
   <wsdl:binding name="dummyBinding" type="tns:dummyPort">
   </wsdl:binding>
   <wsdl:service name="dummy">
      <wsdl:port name="dummyPort" binding="tns:dummyBinding">
         <soap:address location="http://localhost/dummy"/>
      </wsdl:port>
   </wsdl:service>
</wsdl:definitions>
"""

class XMLGen():
    """Class XMLGen
    """
    
    _mh = None
    _client = None
    
    def __init__(self):
        """Class constructor
        
        Called when object is initialized
        
        Args:   
           none           
                
        """          
        
        self._mh = MasterHead.get_head()
    
    @property
    def client(self):
        """ client property getter """
        
        return self._client
    
    def import_spec(self, filename):
        """Method imports specification
        
        Args:
           filename (str): filename
            
        Returns:
           bool: result
        
        Raises:
           event: xmlgen_before_import_spec
           event: xmlgen_after_import_spec     
                
        """     
    
        try:
    
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('datagen_xmlgen_import_spec', filename), self._mh.fromhere()) 
            ev = event.Event('xmlgen_before_import_spec', filename)
            if (self._mh.fire_event(ev) > 0):
                filename = ev.argv(0)    
    
            if (ev.will_run_default()): 
                if (path.exists(filename)):
                    spec_type = (filename.split('.')[-1]).upper()
                    filename = path.join(path.dirname(path.abspath(filename)), filename)
                
                    if (spec_type == 'WSDL'):
                        self._client = Client('file://'+filename, cache=None)
                    elif (spec_type == 'XSD'):
                        wsdl = self._create_dummy_wsdl(filename)
                        self._client = Client('file://'+wsdl, cache=None)
                    else:
                        raise ValueError('Unknown specification type: {0}'.format(spec_type))
                else:
                    raise ValueError('File {0} not found'.format(filename)) 
                
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('datagen_xmlgen_spec_imported'), self._mh.fromhere())   
            ev = event.Event('xmlgen_after_import_spec')
            self._mh.fire_event(ev)            
            
            return True                
        
        except ValueError, ex:
            print ex
            return False        
        except Exception, ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False         

    def toxml(self, root, outfile=None, envelope=False):
        """Method creates sample xml file
        
        Args:
           root (str): root element name
           outfile (str): output filename, default sample.xml
           envelope (bool): create SOAP envelope 

        Returns:
           bool: result
        
        Raises:
           event: xmlgen_before_write
           event: xmlgen_after_write    
                
        """  
    
        try:
    
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('datagen_xmlgen_write_sample'), self._mh.fromhere()) 
            ev = event.Event('jsongen_before_write', root, outfile, envelope)
            if (self._mh.fire_event(ev) > 0):
                root = ev.argv(0)
                outfile = ev.argv(1)
                envelope = ev.argv(2)     
    
            if (ev.will_run_default()): 
                if (self._client == None):
                    raise ValueError('Specification is not imported yet')        
            
                if (envelope): 
                    ns = '{%s}' % 'http://schemas.xmlsoap.org/soap/envelope/'
                    doc = Element(ns+'Envelope')
                    SubElement(doc, ns+'Header')
                    body = SubElement(doc, ns+'Body')
                    body.append(self._toxml_rec(root)) 
                else:
                    doc = self._toxml_rec(root)
                    
                outfile = 'sample.xml' if (outfile == None) else outfile
                with open(outfile, 'w') as f: 
                    f.write(tostring(doc, encoding='UTF-8', xml_declaration=True, pretty_print=True))
                    
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('datagen_xmlgen_sample_written', outfile), self._mh.fromhere())   
            ev = event.Event('xmlgen_after_write')
            self._mh.fire_event(ev)            
            
            return True                      
    
        except ValueError, ex:
            print ex
            return False       
        except Exception, ex:
            self._mh.dmsg('htk_on_error', 'error: {0}'.format(ex), self._mh.fromhere())
            return False     
    
    def _toxml_rec(self, root, obj=None):
        """Method creates sample xml document
        
        It is used in recursive traversal
        
        Args:
           root (str): root element name
           obj (obj): suds element object 

        Returns:
           xml: xml document
        
        Raises:
           error: ValueError     
                
        """          
        
        if (self._client == None):
            raise ValueError('Specification is not imported yet')          
         
        try:
                    
            if (obj == None):
                obj = self._client.factory.create(root)
                     
            ns = '{%s}' % self._get_element_ns(obj.__class__.__name__)   
            doc = Element(ns+root)    

            for key in obj.__keylist__:
        
                subelem = obj[key]        
                if (subelem == None):
                    SubElement(doc, ns+key).text = '?'
                elif (subelem == []):
                    inner_doc = self._toxml_rec(key, None)
                    if (inner_doc != None):
                        doc.append(inner_doc)                 
                else:
                    el_type = self._get_element_type(subelem.__class__.__name__)
                    if (el_type == 'Simple'):
                        SubElement(doc, ns+key).text = '?'
                    elif (el_type == 'Complex'):
                        inner_doc = self._toxml_rec(key, subelem)
                        if (inner_doc != None):
                            doc.append(inner_doc)                   
    
            return doc  
    
        except TypeNotFound:
            return None                     

    def _get_element_type(self, element):
        """Method gets element XSD type
        
        It is used to determine if element is Simple or Complex    
        
        Args:
           element (str): element name

        Returns:
           str: element type
            
        Raises:
           error: ValueError         
                
        """      
    
        if (self._client == None):
            raise ValueError('Specification is not imported yet')
 
        el_type = None
        for value in self._client.wsdl.schema.types.values():
            if (value.name == element):
                if ('Simple' in value.id):
                    el_type = 'Simple'
                elif ('Complex' in value.id):
                    el_type = 'Complex'
                break
        
        return el_type

    def _get_element_ns(self, element):
        """Method gets element XSD namespace 
    
        It is used to construct XML element with correct namespaces
        
        Args:
           element (str): element name

        Returns:
           str: element namespace    
        
        Raises:
           error: ValueError    
                
        """        
    
        if (self._client == None):
            raise ValueError('Specification is not imported yet')    
    
        ns = None
        for key in self._client.wsdl.schema.types.keys():
            if (key[0] == element):
                ns = key[1]
                break
        
        return ns

    def _create_dummy_wsdl(self, xsd):
        """Method creates dummy WSDL file
    
        Workaround method:
        Library suds is designed for SOAP and imports WSDL only
        Dummy WSDL imports given XSD and is parsed automatically
        File is stored in same folder as XSD file (with suffix .wsdl)
        
        Args:
           xsd (str): XSD filename

        Returns:
           str: WSDL filename 
        
        Raises:
           error: ValueError     
                
        """     
    
        if (path.exists(xsd)):        
            with open(xsd, 'r') as f:                   
                tns = search(r'targetNamespace="(.*)"', f.read()).group(1)
                if ('"' in tns):
                    tns = tns[: tns.index('"')]
                    
            filename = xsd.split('/')[-1]
            wsdl = path.abspath(xsd)[:-3]+'wsdl'
        
            with open(wsdl, 'w') as f:             
                f.write(wsdl_tmpl.format(tns, tns, tns, filename)) 
        
            return wsdl
            
        else:
            raise ValueError('File {0} not found'.format(xsd))       