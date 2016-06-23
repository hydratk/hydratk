.. _tutor_datagen_tut3_xml:

Tutorial 3: XML
===============

XML generator creates samples from WSDL/XSD specification.

Command line
^^^^^^^^^^^^

It is controlled via command gen-xml with following options.

Mandatory:

* --gen-spec <path>: path to WSDL/XML specification file
* --gen-element <name>: root element title

Optional:

* --gen-envelope: include SOAP envelope, used for WSDL specification
* --gen-output <path>: path to output file, sample is written to file sample.xml by default

Specification
^^^^^^^^^^^^^

Create four specification files (1 WSDL, 3 XSD).
WSDL ONE-CRM_ContactPersonManagement imports XSD ONE-CRM_ContactPersonManagement which imports 
XSD IntegrationMessage and commonTypes.

  .. code-block:: xml
  
     # ONE-CRM_ContactPersonManagement.wsdl
     <?xml version="1.0" encoding="utf-8"?>
     <wsdl:definitions xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                       xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
                       xmlns:wsdlsoap="http://schemas.xmlsoap.org/wsdl/soap/"
                       xmlns:schema="http://cz.xx.com/systems/ONECRM/ONE-CRM_ContactPersonManagement/1.0"
                       xmlns:tns="http://cz.xx.com/systems/ONECRM/ONE-CRM_ContactPersonManagement/1.0"
                       name="ONE-CRM_ContactPersonManagement"
                       targetNamespace="http://cz.xx.com/systems/ONECRM/ONE-CRM_ContactPersonManagement/1.0">
                  
     <wsdl:types>
       <xsd:schema targetNamespace="http://cz.xx.com/systems/ONECRM/ONE-CRM_ContactPersonManagement/1.0"
                   elementFormDefault="qualified">
         <xsd:include schemaLocation="ONE-CRM_ContactPersonManagement.xsd" />
       </xsd:schema>
     </wsdl:types>
     <wsdl:message name="CreateContactPersonRequestMessage">
       <wsdl:part name="body"
                  element="schema:CreateContactPersonRequest" />
     </wsdl:message>
     <wsdl:message name="CreateContactPersonResponseMessage">
       <wsdl:part name="body"
                  element="schema:CreateContactPersonResponse" />
     </wsdl:message>
     <wsdl:portType name="ONE-CRM_ContactPersonManagementPortType">
       <wsdl:operation name="createContactPerson">
         <wsdl:input name="createContactPersonInput"
                     message="schema:CreateContactPersonRequestMessage" />
         <wsdl:output name="createContactPersonOutput"
                      message="schema:CreateContactPersonResponseMessage" />
       </wsdl:operation>
     </wsdl:portType>
     <wsdl:binding name="ONE-CRM_ContactPersonManagementBinding"
                   type="tns:ONE-CRM_ContactPersonManagementPortType">
       <wsdlsoap:binding style="document"
                         transport="http://schemas.xmlsoap.org/soap/http" />
       <wsdl:operation name="createContactPerson">
         <wsdlsoap:operation soapAction="http://cz.xx.com/systems/ONECRM/ONE-CRM_ContactPersonManagement/1.0/createContactPerson" />
           <wsdl:input name="createContactPersonInput">
             <wsdlsoap:body use="literal" />
           </wsdl:input>
           <wsdl:output name="createContactPersonOutput">
             <wsdlsoap:body use="literal" />
           </wsdl:output>
        </wsdl:operation>
     </wsdl:binding>
     <wsdl:service name="ONE-CRM_ContactPersonManagementService">
       <wsdl:port name="ONE-CRM_ContactPersonManagementPort"
                  binding="tns:ONE-CRM_ContactPersonManagementBinding">
       <wsdlsoap:address location="http://localhost/cz.xx.com/systems/ONECRM/ONE-CRM_ContactPersonManagement/1.0" />
       </wsdl:port>
     </wsdl:service>
    </wsdl:definitions>
    
    # ONE-CRM_ContactPersonManagement.xsd
    
    <?xml version="1.0" encoding="UTF-8"?>
    <xs:schema xmlns:ct="http://cz.xx.com/systems/ONECRM/commonTypes/1.0"
               xmlns:ns="http://cz.xx.com/systems/ONECRM/ONE-CRM_ContactPersonManagement/1.0"
               xmlns:im="http://cz.xx.com/cip/svc/IntegrationMessage-2.0"
               xmlns:xs="http://www.w3.org/2001/XMLSchema"
               targetNamespace="http://cz.xx.com/systems/ONECRM/ONE-CRM_ContactPersonManagement/1.0"
               elementFormDefault="qualified">
    <xs:import namespace="http://cz.xx.com/systems/ONECRM/commonTypes/1.0" schemaLocation="commonTypes.xsd"/>
    <xs:import namespace="http://cz.xx.com/cip/svc/IntegrationMessage-2.0" schemaLocation="IntegrationMessage.xsd"/>
    <xs:element name="CreateContactPersonRequest" type="ns:CreateContactPersonRequest"/>
    <xs:element name="CreateContactPersonResponse" type="ns:CreateContactPersonResponse"/>

    <xs:complexType name="CreateContactPersonRequest">
        <xs:complexContent>
            <xs:extension base="im:RequestMessage">
                <xs:sequence>
                    <xs:element name="requestBody" type="ns:CreateConPersonType" minOccurs="1" maxOccurs="1">
                    </xs:element>
                </xs:sequence>
            </xs:extension>
        </xs:complexContent>
    </xs:complexType>
    <xs:complexType name="CreateContactPersonResponse">
        <xs:complexContent>
            <xs:extension base="im:ResponseMessage">
                <xs:sequence>
                    <xs:element name="responseBody" type="ns:ResponseCreateBodyType" minOccurs="1" maxOccurs="1">
                    </xs:element>
                </xs:sequence>
            </xs:extension>
        </xs:complexContent>
    </xs:complexType>
    <xs:complexType name="ResponseCreateBodyType">
        <xs:sequence>
            <xs:element name="crmCpRefNo" type="xs:string"/>
            <xs:element name="responseMessage" type="ct:ResponseMessageType"/>
        </xs:sequence>
    </xs:complexType>
    <xs:complexType name="CreateConPersonType">
        <xs:sequence>
            <xs:element name="contactEmail" type="xs:string" minOccurs="0">
            </xs:element>
            <xs:element name="sfaCpExtId" type="xs:string" minOccurs="0">
            </xs:element>
            <xs:element name="contactPersonInfo" type="ns:ContactPersonInfoType" minOccurs="0"/>
            <xs:element name="mktAgreements" type="ns:MktAgreementsType" minOccurs="0"/>
        </xs:sequence>
    </xs:complexType>
    <xs:complexType name="ContactPersonInfoType">
        <xs:sequence>
            <xs:element name="firstName" type="xs:string" minOccurs="0"/>
            <xs:element name="lastName" type="xs:string" minOccurs="0"/>
            <xs:element name="contactNumberMobile" type="ct:MobilePhoneNumberType" minOccurs="0"/>
            <xs:element name="contactNumberFix" type="ct:FixPhoneNumberType" minOccurs="0"/>
            <xs:element name="contactEmailStatus" type="xs:string" minOccurs="0"/>
            <xs:element name="enhancedSecurity" type="ct:YesNoFlagType">
            </xs:element>
        </xs:sequence>
    </xs:complexType>
    <xs:complexType name="MktAgreementsType">
        <xs:sequence>
            <xs:element name="mktLetter" type="ct:YesNoFlagType">
            </xs:element>
            <xs:element name="mktEmail" type="ct:YesNoFlagType">
            </xs:element>
            <xs:element name="mktTelemarketing" type="ct:YesNoFlagType">
            </xs:element>
            <xs:element name="mktSmsMms" type="ct:YesNoFlagType">
            </xs:element>
            <xs:element name="mktEmailMedPartners" type="ct:YesNoFlagType">
            </xs:element>
            <xs:element name="mktSmsMmsMedPartners" type="ct:YesNoFlagType">
            </xs:element>
        </xs:sequence>
    </xs:complexType>
    </xs:schema>
    
    # IntegrationMessage.xsd
    
    <?xml version="1.0" encoding="utf-8"?>
    <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
               xmlns="http://cz.xx.com/cip/svc/IntegrationMessage-2.0"
               targetNamespace="http://cz.xx.com/cip/svc/IntegrationMessage-2.0"
               elementFormDefault="qualified"
               attributeFormDefault="unqualified">
    <xs:complexType name="RequestMessage">
      <xs:sequence>
        <xs:element name="requestHeader"
                    type="RequestHeader"></xs:element>
      </xs:sequence>
    </xs:complexType>
    <xs:complexType name="ResponseMessage">
      <xs:sequence>
        <xs:element name="responseHeader"
                    type="ResponseHeader"></xs:element>
      </xs:sequence>
    </xs:complexType>
    <xs:complexType name="Header"
                    abstract="true">
      <xs:sequence>
        <xs:element name="messageId"
                    type="xs:string"></xs:element>
        <xs:element name="timestamp"
                    type="xs:dateTime"></xs:element>
        <xs:element name="correlationId"
                    type="xs:string"
                    minOccurs="0"></xs:element>
        <xs:element name="trackingInfo"
                    type="TrackingInfo"
                    minOccurs="0"></xs:element>
      </xs:sequence>
    </xs:complexType>
    <xs:complexType name="RequestHeader">
    <xs:complexContent>
      <xs:extension base="Header">
        <xs:sequence>
          <xs:element name="consumerId"
                      type="xs:string"></xs:element>
          <xs:element name="providerId"
                      type="xs:string"
                      minOccurs="0"></xs:element>
        </xs:sequence>
      </xs:extension>
    </xs:complexContent>
    </xs:complexType>
    <xs:complexType name="ResponseHeader">
    <xs:complexContent>
      <xs:extension base="Header">
        <xs:sequence>
          <xs:element name="providerId"
                      type="xs:string"></xs:element>
          <xs:element name="consumerId"
                      type="xs:string"
                      minOccurs="0"></xs:element>
          <xs:element name="trackingStatus"
                      type="TrackingStatus"
                      minOccurs="0"></xs:element>
        </xs:sequence>
      </xs:extension>
    </xs:complexContent>
    </xs:complexType>
    <xs:complexType name="TrackingInfo">
      <xs:sequence>
        <xs:element name="businessId"
                    type="TrackingIInfoDetail"
                    minOccurs="0"></xs:element>
        <xs:element name="conversationId"
                    type="TrackingIInfoDetail"
                    minOccurs="0"></xs:element>
        <xs:element name="userId"
                    type="TrackingIInfoDetail"
                    minOccurs="0"></xs:element>
      </xs:sequence>
    </xs:complexType>
    <xs:complexType name="TrackingIInfoDetail">
      <xs:sequence>
        <xs:element name="value"
                    type="xs:string"></xs:element>
        <xs:element name="meaning"
                    type="xs:string"
                    minOccurs="0"></xs:element>
      </xs:sequence>
    </xs:complexType>
    <xs:complexType name="TrackingStatus">
      <xs:sequence>
        <xs:element name="code"
                    type="xs:string"></xs:element>
        <xs:element name="type"
                    type="xs:string"
                    minOccurs="0"></xs:element>
        <xs:element name="message"
                    type="xs:string"
                    minOccurs="0"></xs:element>
      </xs:sequence>
    </xs:complexType>
    <xs:complexType name="ErrorResponseMessageBody">
      <xs:sequence>
        <xs:element name="errorCode"
                    type="xs:string"></xs:element>
        <xs:element name="errorMessage"
                    type="xs:string"
                    minOccurs="0"></xs:element>
      </xs:sequence>
    </xs:complexType>
    <xs:complexType name="ErrorResponseMessage">
    <xs:complexContent>
      <xs:extension base="ResponseMessage">
        <xs:sequence>
          <xs:element name="responseBody"
                      type="ErrorResponseMessageBody"></xs:element>
        </xs:sequence>
      </xs:extension>
    </xs:complexContent>
    </xs:complexType>
    <xs:element name="errorResponse"
                type="ErrorResponseMessage"></xs:element>
    </xs:schema>
  
    # commonTypes.xsd
  
    <?xml version="1.0" encoding="utf-8"?>
    <xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
               elementFormDefault="qualified"
               targetNamespace="http://cz.xx.com/systems/ONECRM/commonTypes/1.0"
               xmlns="http://cz.xx.com/systems/ONECRM/commonTypes/1.0">
    <xs:simpleType name="LoginNameType" />
    <xs:simpleType name="UserTypeType" />
    <xs:simpleType name="PasswordType" />
    <xs:simpleType name="MobilePhoneNumberType" />
    <xs:simpleType name="FixPhoneNumberType" />
    <xs:simpleType name="YesNoFlagType" />
    <xs:simpleType name="ApplicationCodeType" />
    <xs:simpleType name="EmailStatus" />
    <xs:complexType name="ResponseMessageType">
      <xs:sequence>
        <xs:element name="resultCode"
                    type="xs:int" />
        <xs:element name="resultMessage"
                    type="xs:string" />
      </xs:sequence>
    </xs:complexType>
    </xs:schema>
  
Generator
^^^^^^^^^

Create sample for element CreateContactPersonRequest including SOAP envelope from WSDL, SOAP request in other words.

  .. code-block:: bash
  
     $ htk --gen-spec ONE-CRM_ContactPersonManagement.wsdl --gen-element CreateContactPersonRequest --gen-envelope --gen-output output.xml gen-xml
      
     Sample generated  
     
Generated file contains sample with ``?`` placeholders.

  .. code-block:: xml
  
     <?xml version='1.0' encoding='UTF-8'?>
     <ns0:Envelope xmlns:ns0="http://schemas.xmlsoap.org/soap/envelope/">
       <ns0:Header/>
       <ns0:Body>
         <ns0:CreateContactPersonRequest xmlns:ns0="http://cz.xx.com/systems/ONECRM/ONE-CRM_ContactPersonManagement/1.0">
           <ns0:requestHeader xmlns:ns0="http://cz.xx.com/cip/svc/IntegrationMessage-2.0">
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
     
  .. note::
  
    Option output is optional. If not provided the output filename is sample.json.   
    
Create sample for element RequestMessage from XSD, ordinary xml in other words (no relation to SOAP)

  .. code-block:: bash
  
     $ htk --gen-spec IntegrationMessage.xsd --gen-element RequestMessage gen-xml
     
     Sample generated
     
  .. code-block:: xml
  
     <?xml version='1.0' encoding='UTF-8'?>
     <ns0:RequestMessage xmlns:ns0="http://cz.xx.com/cip/svc/IntegrationMessage-2.0">
       <ns0:requestHeader>
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
     </ns0:RequestMessage>
     
  .. note::
  
     If you create sample from XSD, dummy WSDL xsd_filename.wsdl is created. 
     You can delete it, it imports original XSD only to be parsed.    
     
Errors
^^^^^^

Following examples demonstrate several error situations caused by incorrect input. 
Messages with error detail are printed in debug mode.

* Unknown specification

 .. code-block:: bash
 
    $ htk --gen-spec IntegrationMessage.xsd2 --gen-element RequestMessage gen-xml
    
    File IntegrationMessage.xsd2 not found
    Import specification error  
    
* Unknown element

  .. code-block:: bash
  
     $ htk --gen-spec IntegrationMessage.xsd --gen-element RequestMessage2 gen-xml
     
     Error: hydratk.extensions.datagen.xmlgen:toxml:0: error: Type 'NoneType' cannot be serialized. 
     Generation error
                     
* Invalid specification (invalid XML tag)

  .. code-block:: bash
     
     $ htk --gen-spec IntegrationMessage.xsd --gen-element RequestMessage gen-xml
     
     Error: hydratk.extensions.datagen.xmlgen:import_spec:0: error: <unknown>:12:2: not well-formed (invalid token) 
     Import specification error
          
* Invalid specification (bad XSD import)

  .. code-block:: bash
  
     $ htk --gen-spec ONE-CRM_ContactPersonManagement.wsdl --gen-element CreateContactPersonRequest --gen-envelope --gen-output output.xml gen-xml
  
     Error: hydratk.extensions.datagen.xmlgen:import_spec:0: error: <urlopen error [Errno 2] No such file or directory: '/home/lynus/hydratk/ONE-CRM_ContactPersonManagement2.xsd'> 
     Import specification error
                              
API
^^^

This section shows several examples how to use XML generator as API in your extensions/libraries.
API uses HydraTK core functionalities so it must be running.

Methods    

* import_spec: import XML specification (WSDL/XSD), params: filename
* toxml: generate sample xml file, params: root, outfile, envelope   

Examples

  .. code-block:: python
  
     # import generator
     from hydratk.extensions.datagen.xmlgen import XMLGen
     g = XMLGen()
     
     # import specification
     res = g.import_schema('ONE-CRM_ContactPersonManagement.wsdl')
     
     # generate file
     res = g.tojson('CreateContactPersonRequest', 'output.xml', envelope=True)                                   