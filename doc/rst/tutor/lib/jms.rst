.. JMS

===
JMS
===

Library hydratk.lib.network.jms.client provides jms client.

**Verified JMS providers**:

- WebLogic

**Methods**:

- **connect** - connect to JMS provider 
- **disconnect** - disconnect from JMS provider 
- **send** - send message to queue

Installation
============

Part of JMS client library is implemented in Java as a wrapper application which uses Java JMS API.
Python client library executes JVM and communicates via stdin, stdout streams with the wrapper.

Specific Java libraries are needed to access JMS providers (WebLogic, HornetQ, OpenMQ, ActiveMQ etc.). 
JMS API has no low level communication protocol specification so there is no universal client library.
These libraries are not bundled with hydra. 

After hydratk installation do following actions:

1. Check that directory /var/local/hydratk/java was created, is writable and contains files: JMSClient.java, JMSClient.class, javaee.jar
2. Store specific client jar file to same directory (i.e. weblogic.jar).

Examples
========

  .. code-block:: python
  
     # import library
     import hydratk.lib.network.jms.client as jms
    
     # initialize client
     client = jms.JMSClient()
     
     # connect to provider
     connection_factory = 'javax/jms/QueueConnectionFactory'
     initial_context_factory = 'weblogic.jndi.WLInitialContextFactory'
     provider_url = 't3://sxcipppr1.cz:8301'
     
     # returns bool
     client.connect(connection_factory, initial_context_factory, provider_url) 
     
     # send message
     destination = 'cipesb/gf/cip2ba/queue/request'
     jms_type = 'BA-GF.BillingCustomerManagement-2.0.manageCustomer.Request'
     message = '<ManageCustomer><id>1</id><name>Charlie Bowman</name></ManageCustomer>'
     correlation_id = 'hydratk-123456'
     
     # returns bool
     client.send(destination, jms_type, message, correlation_id)
     
     # disconnect from provider
     # returns bool
     client.disconnect()