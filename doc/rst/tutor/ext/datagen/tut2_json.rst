.. _tutor_datagen_tut2_json:

Tutorial 2: JSON
================

JSON generator creates samples from JSON specification.

Command line
^^^^^^^^^^^^

It is controlled via command gen-json with following options. 

Mandatory:

* --gen-spec <path>: path to JSON specification file

Optional:

* --gen-output <path>: path to output file, sample is written to file sample.json by default

Specification
^^^^^^^^^^^^^

First create two files spec.json and spec2.json with sample schema specifications.
Second specification is referenced from the first.

  .. code-block:: javascript
  
     # spec.json
     {
       "$schema": "http://json-schema.org/draft-04/schema#",
       "title": "Product set",
       "type": "array",
       "items": {
           "title": "Product",
           "type": "object",
           "properties": {
               "id": {
                   "description": "The unique identifier for a product",
                   "type": "number"
               },
               "name": {
                   "type": "string"
               },
               "price": {
                   "type": "number",
                   "minimum": 0,
                   "exclusiveMinimum": true
               },
               "tags": {
                   "type": "array",
                   "items": {
                       "type": "string"
                   },
                   "minItems": 1,
                   "uniqueItems": true
               },
               "dimensions": {
                   "type": "object",
                   "properties": {
                       "length": {"type": "number"},
                       "width": {"type": "number"},
                       "height": {"type": "number"}
                   },
                   "required": ["length", "width", "height"]
               },
               "warehouseLocation": {
                  "description": "Coordinates of the warehouse with the product",
                  "$ref": "file://spec2.json"
               }
           },
           "required": ["id", "name", "price"]
         }
     }

     # spec2.json
     {
       "$schema": "http://json-schema.org/draft-04/schema#",
       "description": "A geographical coordinate",
       "type": "object",
       "properties": {
           "latitude": { "type": "number" },
           "longitude": { "type": "number" }
       }
     }
     
  .. note::
  
     Sample is generated from root element. It is not supported to choose any subelement.
    
Generator
^^^^^^^^^

  .. code-block:: bash
  
     $ htk --gen-spec spec.json --gen-output output.json gen-json  
     
     Sample generated
     
Generated file contains sample with ``?`` placeholders.     
     
  .. code-block:: javascript
  
     [
         {
             "dimensions": {
                 "width": "?",
                 "length": "?",
                 "height": "?"
         },
         "tags": [
             "?"
         ],
         "price": "?",
         "warehouseLocation": {
             "latitude": "?",
             "longitude": "?"
         },
         "id": "?",
         "name": "?"
         }
    ] 
      
  .. note::
  
    Option output is optional. If not provided the output filename is sample.json.    
    
Errors
^^^^^^

Following examples demonstrate several error situations caused by incorrect input. 
Messages with error detail are printed in debug mode.

* Unknown specification

 .. code-block:: bash
 
    $ htk --gen-spec spec3.json gen-json
    
    File spec3.json not found
    Import specification error     
    
* Invalid specification (invalid element)

  .. code-block:: bash
     
     $ htk --gen-spec spec.json gen-json    
    
     JSON parsing error at line 1, column 6 (position 5): Unterminated object.
     Import specification error 
     
* Invalid specification (bad schema reference)

  .. code-block:: bash
  
     $ htk --gen-spec spec.json gen-json    
  
     Error: hydratk.extensions.datagen.jsongen:tojson:0: error: File /home/lynus/hydratk/spec3.json not found 
     Generation error     
     
API
^^^

This section shows several examples how to use JSON generator as API in your extensions/libraries.
API uses HydraTK core functionalities so it must be running.

Methods    

* import_schema: import JSON schema, params: filename
* tojson: generate sample json file, params: outfile   

Examples

  .. code-block:: python
  
     # import generator
     from hydratk.extensions.datagen.jsongen import JSONGen
     g = JSONGen()
     
     # import schema
     res = g.import_schema('spec.json')
     
     # generate file
     res = g.tojson('output.json')     