.. _index:

=======
HydraTK
=======

`HydraTK <www.hydratk.org>`_ is pythonic, object oriented application toolkit.
It is oriented to development of applications, currently mostly for automated software testing.

It allows you to develop specific extensions and libraries that can use embedded core functionalities.

Main functionalities are:

* Extensibility: Develop own extensions/libraries from prepared skeletons.  
* Events hooks: Intercept system events and react to them, it is also possible to configure own events.
* Command line interface: Configure own commands and options. 
* Parallel processing: Execute you application in parallel mode. 
* Internalization: Configure application texts for multiple languages.
* Services:
* Signals: Intercept POSIX signals and react to them.
* Messaging:
* Debugging: Fill your application with unified debug messages, different levels and languages are supported. 
* Profiling: Execute application in profiler mode to discover performance bottlenecks.

Several extensions and libraries are already available to download. Only the most interesting ones are highlighted.
Check complete list of extensions and libraries.

Extensions:

* Yoda: Engine for execution of automated test scripts. Extension defines own script format with hierarchical structure and embedded Python code. It also provides reporting database.

Libraries:

* Network: Clients for most of protocols and interfaces which are used to communicate with contemporary enterprise applications. Database, email, FTP, JMS, HTTP REST, Selenium API, SOAP, SSH, TCP/IP.

If you would like to try HydraTK, read installation instructions. 
In order to learn how to use HydraTK, it is recommended to follow tutorials which will demonstrate basic features using simple examples. 
Once done, you can browse through module documentation to find out what features are available and how it works. 
When you would like to develop own application or extend existing module, browse programmer's guide and reference manual. 

HydraTK is open source project and contributions are welcome. 
If you are interested, please read `development <www.hydratk.org/development>`_ section on project's web site.

.. toctree::
   :hidden:
   
   rst/install
   rst/tutor
   rst/module
   rst/progguide
   rst/refman