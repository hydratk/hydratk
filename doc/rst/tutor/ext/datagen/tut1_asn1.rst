.. _tutor_datagen_tut1_asn1:

Tutorial 1: ASN.1
=================

ASN.1 codec provides encoder/decoder of text/binary file to binary/text file
according to ASN.1 specification. Text files use JSON format.

Command line
^^^^^^^^^^^^

It is controlled via command gen-asn1 with following options.

Mandatory:

* --gen-action <name>: encode|decode, encode from json to bin, decode from bin to json
* --gen-spec <path>: path to ASN.1 specification file
* --gen-element <name>: root element title
* --gen-input <path>: path to input json file for encode, bin file for decode

Optional: 

* --gen-output <path>: path to output file, output is written to file <input> with changed suffix by default

Specification
^^^^^^^^^^^^^

First create file spec.asn with sample specification in ASN.1 format.

  .. code-block:: cfg
  
     Test1 DEFINITIONS AUTOMATIC TAGS ::=
     BEGIN
    
       TestInt ::= INTEGER {un(1), deux(2)} (0..100, ...)
       TestEnum ::= ENUMERATED {un , deux, trois}
       TestBitStr ::= BIT STRING (SIZE(12..24, ...))
       TestOctetStr ::= OCTET STRING (SIZE(2..10))
       TestChoice ::= CHOICE {
         a TestInt,
         b TestEnum,
         c TestBitStr
       }
       TestSeqOf ::= SEQUENCE SIZE (1..4) OF TestInt
       TestSeq ::= SEQUENCE {
         a TestInt,
         b TestEnum OPTIONAL,
         c TestBitStr
       }
       TestSeqSeq ::= SEQUENCE {
         a TestSeq,
         b SEQUENCE OF TestSeq,
         c TestChoice
       }
       TestSeq2 ::= SEQUENCE {
         a TestInt,
         b BOOLEAN,
         c SEQUENCE {
           d BOOLEAN OPTIONAL,
           e TestOctetStr
         },
         f SET {
           g TestInt,
           h BOOLEAN
         }
       }        
     END
     
  .. note::
  
     ASN.1 specifications used in industry are more complicated than our sample.
     For example TAP specification (used in telecommunication) has around 1600 lines.
     
Encoder
^^^^^^^

Now create JSON file input.json with sample record compliant with TestSeq2 definition.     

  .. code-block:: javascript
   
     {
       "a": 20,
       "b": true,
       "c": {
         "d": false,
         "e": "xyz"
       },
       "f": {
         "g": 128,
         "h": true
       }
     }
     
Encode the file using command gen-asn1.     
     
  .. code-block:: bash
  
     $ htk --gen-action encode --gen-spec spec.asn --gen-input input.json --gen-element TestSeq2 --gen-output output.bin gen-asn1  
     
     encode finished
     
File output.bin contains hex text. 

  .. code-block:: cfg
  
     30198001148101FFA208800100810378797AA307800200808101FF

  .. note::
  
    Option output is optional. If not provided the output filename is based on input filename (input.bin in example).
    
Decoder
^^^^^^^

Now let's try to decode generated file output.bin.

  .. code-block:: bash
  
     $ htk --gen-action decode --gen-spec spec.asn --gen-input output.bin --gen-element TestSeq2 gen-asn1
     
     decode finished
     
Generated file output.json has same content as original file input.json.

Errors
^^^^^^

Following examples demonstrate several error situations caused by incorrect input. 
Messages with error detail are printed in debug mode.

* Unknown specification

 .. code-block:: bash
 
    $ htk --gen-action encode --gen-spec spec2.asn --gen-element TestSeq2 --gen-input input.json gen-asn1
    
    File spec2.asn not found
    Import specification error  
    
* Unknown element

  .. code-block:: bash
  
     $ htk --gen-action encode --gen-spec spec.asn --gen-element TestSeq3 --gen-input input.json gen-asn1
     
     Error: hydratk.extensions.datagen.asn1codec:encode:0: error: 'TestSeq3'     
     encode error
     
* Unknown input file     

  .. code-block:: bash
  
     $ htk --gen-action encode --gen-spec spec.asn --gen-element TestSeq2 --gen-input input2.json gen-asn1
  
     File input2.json not found
     encode error     
                     
* Invalid specification (invalid element)

  .. code-block:: bash
     
     $ htk --gen-action encode --gen-spec spec.asn --gen-element TestSeq2 --gen-input input.json gen-asn1
     
     unable to process 1 objects:
     TestSeq2
     can be a missing IMPORT directive, a circular reference or a self reference
     Error: hydratk.extensions.datagen.asn1codec:import_spec:0: error: bad reference... no luck 
     Import specification error
          
* Invalid input file

  .. code-block:: bash
  
     $ htk --gen-action encode --gen-spec spec.asn --gen-element TestSeq2 --gen-input input.json gen-asn1
  
     Error: hydratk.extensions.datagen.asn1codec:encode:0: error: TestSeq2.f: invalid SEQ / SET / CLASS value type 
     encode error

API
^^^

This section shows several examples how to use ASN.1 codec as API in your extensions/libraries.
API uses HydraTK core functionalities so it must be running.

Methods    

* import_spec: import ASN.1 schema, params: filename
* encode: encode JSON file, params: infile, element, outfile   
* decode: decode binary file, params: infile, element, outfile

Examples

  .. code-block:: python
  
     # import codec
     from hydratk.extensions.datagen.asn1codec import ASN1Codec
     g = ASN1Codec()
     
     # import schema
     res = g.import_schema('spec.asn')
     
     # encode
     res = g.encode('input.json', 'TestSeq2', 'output.bin') 
     
     # decode
     res = g.decode('input.bin', 'TestSeq2', 'output.json')       