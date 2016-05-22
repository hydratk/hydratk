# -*- coding: utf-8 -*-
"""Extension for data generators

.. module:: datagen.datagen
   :platform: Unix
   :synopsis: Extension for data generators
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from hydratk.core import extension
from hydratk.lib.console.commandlinetool import CommandlineTool

class Extension(extension.Extension):
    """Class Extension
    """
    
    def _init_extension(self):
        """Method initializes extension
        
        Args:            
           none
           
        Returns:
           void    
                
        """         
        
        self._ext_id   = 'datagen'
        self._ext_name = 'Datagen'
        self._ext_version = '0.1.0'
        self._ext_author = 'Petr Rašek <bowman@hydratk.org>'
        self._ext_year = '2016'  
        
    def _register_actions(self):
        """Method registers actions
        
        Commands gen-asn1, gen-json, gen-xml
        
        Args:
           none            
           
        Returns:
           void    
                
        """          
        
        self._mh.match_cli_command('gen-asn1')
        self._mh.match_cli_command('gen-json') 
        self._mh.match_cli_command('gen-xml')
         
        hook = [
                {'command' : 'gen-asn1', 'callback' : self.gen_asn1},
                {'command' : 'gen-json', 'callback' : self.gen_json},
                {'command' : 'gen-xml', 'callback' : self.gen_xml}
               ]  
        self._mh.register_command_hook(hook)  
        
        self._mh.match_long_option('spec', True)  
        self._mh.match_long_option('input', True)
        self._mh.match_long_option('output', True)
        self._mh.match_long_option('action', True)  
        self._mh.match_long_option('element', True) 
        self._mh.match_long_option('envelope', False)   
        
    def gen_asn1(self):
        """Method handles command gen-asn1
        
        Encode text file, decode binary file according to ASN.1 specification
        
        Args:
           none
        
        Returns:
           void                 
                
        """         
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('datagen_received_cmd', 'gen-asn1'), self._mh.fromhere())
        
        action = CommandlineTool.get_input_option('--action')  
        spec = CommandlineTool.get_input_option('--spec') 
        element = CommandlineTool.get_input_option('--element') 
        input = CommandlineTool.get_input_option('--input') 
        output = CommandlineTool.get_input_option('--output')        
        
        if (not action):
            print ('Missing option action')            
        elif (action not in ['encode', 'decode']):
            print ('Action not in encode|decode')                         
        elif (not spec):
            print ('Missing option spec')             
        elif (not element):
            print ('Missing option element')                          
        elif (not input):
            print ('Missing option input') 
        else:                       
        
            from hydratk.extensions.datagen.asn1codec import ASN1Codec
        
            codec = ASN1Codec()
            if (codec.import_spec(spec)):
                output = None if (not output) else output
                if (action == 'encode'):
                    result = codec.encode(input, element, output)
                elif (action == 'decode'):  
                    result = codec.decode(input, element, output) 
                    
                if (not result):
                    print ('{0} error'.format(action)) 
                else:
                    print ('{0} finished'.format(action))                          
            else:
                print ('Import specification error')                         
        
    def gen_json(self):
        """Method handles command gen-json
        
        Generate sample JSON file according to JSON specification  
        
        Args:
           none
        
        Returns:
           void                 
                
        """         
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('datagen_received_cmd', 'gen-json'), self._mh.fromhere())
        
        spec = CommandlineTool.get_input_option('--spec') 
        output = CommandlineTool.get_input_option('--output') 
        
        if (not spec):
            print ('Missing option spec')
        else:     
        
            from hydratk.extensions.datagen.jsongen import JSONGen 
        
            gen = JSONGen()
            if (gen.import_schema(spec)):
                output = None if (not output) else output
                if (not gen.tojson(output)):
                    print ('Generation error')
                else:
                    print ('Sample generated')                     
            else:
                print ('Import specification error')    
            
    def gen_xml(self):
        """Method handles command gen-xml
        
        Generate sample XML file according to WSDL/XSD specification 
        
        Args:
           none
        
        Returns:
           void                  
                
        """         
        
        self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('datagen_received_cmd', 'gen-xml'), self._mh.fromhere())
        
        spec = CommandlineTool.get_input_option('--spec') 
        element = CommandlineTool.get_input_option('--element') 
        output = CommandlineTool.get_input_option('--output')
        envelope = CommandlineTool.get_input_option('--envelope')  
        
        if (not spec):
            print ('Missing option spec')
        elif (not element):
            print ('Missing option element')
        else:           
        
            from hydratk.extensions.datagen.xmlgen import XMLGen 
           
            gen = XMLGen()
            if (gen.import_spec(spec)):                
                output = None if (not output) else output
                if (not gen.toxml(element, output, envelope)):
                    print ('Generation error')  
                else:
                    print ('Sample generated')   
            else:
                print ('Import specification error')                                   