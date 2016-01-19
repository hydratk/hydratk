.. Datagen

=======
Datagen
=======

Datagen extension provides utilities for data generation.

Datagen contains following generators:

- **ASN.1** encoder/decoder with ASN.1 specification
- **JSON** sample generator from JSON specification
- **XML** sample generator from WSDL/XSD specification

Installation
============

Extension is embedded to hydratk and enabled by default in configuration file.

Commands
========

Extensions provides following commands:

- **gen-asn1**: ASN.1 encoder/decoder
- **gen-json**: JSON generator
- **gen-xml**: XML generator 

ASN.1
=====

Command gen-xml provides following options:

- **--action**: encode|decode, encode for json->bin, decode for bin->json
- **--spec <path>**: path to ASN.1 specification file
- **--element**: root element title
- **--input <path>** path to input json file for encode, bin file for decode
- **[--output <path>]**: path to output file, output is written in <input> with changed suffix by default

Sample ASN.1 specification

  .. code-block:: xml
  
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
     
JSON file to encode

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

BIN file to decode

  .. code-block:: xml
  
     30198001148101FFA208800100810378797AA307800200808101FF 

JSON
====

Command gen-json provides following options:

- **--spec <path>**: path to JSON specification file
- **[--output <path>]**: path to output file, sample is written to file sample.json by default


Sample JSON specification
 
  .. code-block:: javascript
  
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
                  "$ref": "file://schema2.json"
              }
          },
          "required": ["id", "name", "price"]
        }
    }

    {
      "$schema": "http://json-schema.org/draft-04/schema#",
      "description": "A geographical coordinate",
      "type": "object",
      "properties": {
          "latitude": { "type": "number" },
          "longitude": { "type": "number" }
      }
    }

Generated sample file 

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
 
XML
===

Command gen-xml provides following options:

- **--spec <path>**: path to WSDL/XML specification file
- **--element**: root element title
- **--envelope**: include SOAP envelope, used for WSDL specification
- **[--output <path>]**: path to output file, sample is written to file sample.xml by default

Generated sample file

  .. code-block:: xml
  
     <?xml version='1.0' encoding='UTF-8'?>
     <ns0:Envelope xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/">
       <ns0:Header/>
       <ns0:Body>
         <ns0:CreateContactPersonRequest xmlns:ns0="http://cz.o2.com/systems/ONECRM/ONE-CRM_ContactPersonManagement/1.0">
           <ns0:requestHeader xmlns:ns0="http://cz.o2.com/cip/svc/IntegrationMessage-2.0">
             <ns0:messageId>?</ns0:messageId>
             <ns0:timestamp>?</ns0:timestamp>
             <ns0:correlationId>?</ns0:correlationId>
             <ns0:trackingInfo>
               <ns0:businessId>
                 <ns0:value>?</ns0:value>
                 <ns0:meaning>?</ns0:meaning>
               </ns0:businessId>
               <ns0:conversationId>
                 <ns0:value>?</ns0:value>
                 <ns0:meaning>?</ns0:meaning>
               </ns0:conversationId>
               <ns0:userId>
                 <ns0:value>?</ns0:value>
                 <ns0:meaning>?</ns0:meaning>
               </ns0:userId>
             </ns0:trackingInfo>
             <ns0:consumerId>?</ns0:consumerId>
             <ns0:providerId>?</ns0:providerId>
           </ns0:requestHeader>
           <ns0:requestBody>
             <ns0:contactEmail>?</ns0:contactEmail>
             <ns0:sfaCpExtId>?</ns0:sfaCpExtId>
             <ns0:contactPersonInfo>
               <ns0:firstName>?</ns0:firstName>
               <ns0:lastName>?</ns0:lastName>
               <ns0:contactNumberMobile>?</ns0:contactNumberMobile>
               <ns0:contactNumberFix>?</ns0:contactNumberFix>
               <ns0:contactEmailStatus>?</ns0:contactEmailStatus>
               <ns0:enhancedSecurity>?</ns0:enhancedSecurity>
             </ns0:contactPersonInfo>
             <ns0:mktAgreements>
               <ns0:mktLetter>?</ns0:mktLetter>
               <ns0:mktEmail>?</ns0:mktEmail>
               <ns0:mktTelemarketing>?</ns0:mktTelemarketing>
               <ns0:mktSmsMms>?</ns0:mktSmsMms>
               <ns0:mktEmailMedPartners>?</ns0:mktEmailMedPartners>
               <ns0:mktSmsMmsMedPartners>?</ns0:mktSmsMmsMedPartners>
             </ns0:mktAgreements>
           </ns0:requestBody>
         </ns0:CreateContactPersonRequest>
       </ns0:Body>
     </ns0:Envelope>  