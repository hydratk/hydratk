.. TestEnv

=======
TestEnv
=======

TestEnv extension provides testing environment to practise creation of automated testing together with Yoda extensions.

Testenv contains simple CRM application with following interfaces:

- **DB** interface to SQLite database
- **REST** interface to REST services on web server
- **SOAP** interface to SOAP services on web server

Installation
============

1. Download extension from https://git.hydratk.org/testenv.git.
2. Install extension using command python setup.py install.
3. Check that extension was installed using command htk list-extensions.
4. Check that directory /var/local/hydratk/testenv was created, is writable and contains files: install_db.sql, crm.wsdl, crm.xsd.
5. Check that directory /etc/hydratk/conf.d/ contains configuration file hydratk-ext-testenv.conf. 

Configuration
=============

Configuration file is stored in /etc/hydratk/conf.d/hydratk-ext-testenv.conf.

Default configuration parameters are:

- **server_ip**: 0.0.0.0 (web server is started on localhost)
- **server_port**: 8888 (TCP port)
- **ext_dir**: /var/local/hydratk/testenv (directory where extensions application files are stored, it is recommended to be kept)
- **db_file**: testenv.db3 (database filename)

Commands
========

Extensions provides following commands:

- **te-start**: Start testing environment. 
  It will start web server on 0.0.0.0:8888 and install database if not already installed. 
- **te-install-db**: Install database using script install_db.sql. Database will be stored in file /var/local/hydratk/testenv/testenv.db3.
  If database file already exists it will be deleted and replaced with clear installation.

DB interface
============

Sample Yoda script is located in /var/local/hydratk/yoda/yoda-tests/testenv/db.yoda.

Important snippets are commented.

Connect to database
  .. code-block:: python
  
     # import helpers
     import testenv_helpers as hlp
    
     # create DB client instance and connect
     client = hlp.db()
     res = client.connect() # returns bool
     
Disconnect from database
  .. code-block:: python
  
     # returns bool
     client.disconnect()     

Customer operations
  .. code-block:: python
  
     # create customer
     name = 'Vince Neil'
     status = 'active'
     segment = 2
     birth_no = '700101/0001'
     reg_no = '12345'
     tax_no = 'CZ12345'
     
     # returns generated id
     cust = client.create_customer(name, segment, status, birth_no, reg_no, tax_no)
     
     # read created customer, returns Customer object
     print client.read_customer(cust) 
     # id:1|name:Vince Neil|status:active|segment:2|birth_no:700101/0001|reg_no:12345|tax_no:CZ12345
     
     # change customer
     name = 'Charlie Bowman'
     status = 'suspend'
     segment = 3
     birth_no = '700101/0002'
     reg_no = '1234'
     tax_no = 'CZ1234'
     
     # returns bool
     res = client.change_customer(cust, name, status, segment, birth_no, reg_no, tax_no)   
     
Payer operations
  .. code-block:: python
  
     # create payer
     name = 'Vince Neil'
     status = 'active'
     billcycle = 1
     bank_account = '123456/0100'
     customer = cust
     
     # returns generated id
     pay = client.create_payer(name, billcycle, customer, status, bank_account) 
     
     # read created payer, returns Payer object
     print client.read_payer(pay)
     # id:1|name:Vince Neil|status:active|billcycle:1|bank_account:123456/0100|customer:1
     
     # change payer
     name = 'Charlie Bowman'
     status = 'suspend'
     billcycle = 2
     bank_account = '654321/0800'
     
     # returns bool
     res = client.change_payer(pay, name, status, billcycle, bank_account)  
     
Subscriber operations
  .. code-block:: python
  
     # create subscriber
     name = 'Vince Neil'
     msisdn = '773592179'
     status = 'active'
     market = 1
     tariff = 433
     customer = cust
     payer = pay
     
     # returns generated id
     subs = client.create_subscriber(name, msisdn, market, tariff, customer, payer, status)
     
     # read created subscriber, returns Subscriber object
     print client.read_subscriber(subs)                             
     # id:1|name:Vince Neil|msisdn:773592179|status:active|market:1|tariff:433|customer:1|payer:1
     
     # change subscriber
     name = 'Charlie Bowman'
     msisdn = '603404746'
     status = 'suspend'
     market = 2
     tariff = 434
     
     # returns bool
     res = client.change_subscriber(subs, name, msisdn, status, market, tariff)
     
Contact operations
  .. code-block:: python
  
     # create contact
     name = 'Vince Neil'
     phone = '12345'
     email = 'aaa@xxx.com'
     
     # returns generated id
     con = client.create_contact(name, phone, email)
     
     # read created contact, returns Contact object
     client.read_contact(con)  
     # id:1|name:Vince Neil|phone:12345|email:aaa@xxx.com|roles#
     
     # change contact
     name = 'Charlie Bowman'
     phone = '123456'
     email = 'bbb@xxx.com'
     
     # returns bool
     res = client.change_contact(con, name, phone, email) 
     
     # assign contact role
     # returns bool
     client.assign_contact_role(con, 'contract', customer=cust)  
     client.assign_contact_role(con, 'invoicing', payer=pay) 
     client.assign_contact_role(con, 'contact', subscriber=subs)    
     
     # read contact with roles
     print client.read_contact(con)
     # id:1|name:Charlie Bowman|phone:123456|email:bbb@xxx.com|roles#id:1|title:contract|customer:1|payer:None|subscriber:None
       #id:1|title:invoicing|customer:None|payer:1|subscriber:None#id:1|title:contact|customer:None|payer:None|subscriber:1# 
       
     # revoke contact role
     # returns bool
     client.revoke_contact_role(con, 'contract', customer=cust)  
     client.revoke_contact_role(con, 'invoicing', payer=pay) 
     client.revoke_contact_role(con, 'contact', subscriber=subs) 
     
Address operations:
  .. code-block:: python
  
     # create address
     street = 'Tomickova'
     street_no = '2144/1'
     city = 'Praha'
     zip = 14900
     
     # returns generated id
     addr = client.create_address(street, street_no, city, zip)  
     
     # read cread address, returns Address object
     # id:1|street:Tomickova|street_no:2144/1|city:Praha|zip:14900|roles#
     
     # change address
     street = 'Babakova'
     street_no = '2152/6'
     city = 'Praha 4'
     zip = 14800
     
     # returns bool
     client.change_address(addr, street, street_no, city, zip)  
     
     # assign address role
     # returns bool
     client.assign_address_role(addr, 'contract', customer=cust)  
     client.assign_address_role(addr, 'invoicing', payer=pay) 
     client.assign_address_role(addr, 'contact', subscriber=subs) 
     client.assign_address_role(addr, 'delivery', contact=con)    
     
     # read address with roles
     print client.read_address(addr)
     # id:1|street:Babakova|street_no:2152/6|city:Praha 4|zip:14800|roles#id:1|title:contract|contact:None|customer:1|payer:None|subscriber:None
       #id:1|title:invoicing|contact:None|customer:None|payer:1|subscriber:None#id:1|title:contact|contact:None|customer:None|payer:None|subscriber:1
       #id:1|title:delivery|contact:1|customer:None|payer:None|subscriber:None#   
       
     # revoke address role
     # returns bool
     client.revoke_address_role(addr, 'contract', customer=cust)  
     client.revoke_address_role(addr, 'invoicing', payer=pay) 
     client.revoke_address_role(addr, 'contact', subscriber=subs)  
     client.revoke_address_role(addr, 'delivery', contact=con)  
     
Service operations
  .. code-block:: python
  
     # create service
     service = 615
     subscriber = subs
     status = 'active'
     params = {}
     params[121] = '123456'
     
     # returns bool
     client.create_service(service, subscriber=subscriber, status=status, params=params)     
     
     # read service, returns list of Service object
     print client.read_services(subscriber=subscriber)[0] 
     # id:615|name:Telefonni cislo|status:active|params#121:123456#
     
     # change service
     service = 615
     subscriber = subs
     status = 'deactive'
     params = {}
     params[121] = '603404746' 
     
     # returns bool
     client.change_service(service, subscriber=subscriber, status=status, params=params)                                             

REST interface
==============

Sample Yoda script is located in /var/local/hydratk/yoda/yoda-tests/testenv/rest.yoda.

The interface provides same methods as DB interface, so only the client initialiazation is described.

Create REST client
  .. code-block:: python
  
     # import helpers
     import testenv_helpers as hlp
    
     # create REST client instance
     client = hlp.rest() 
     
REST services are hosted on endpoint 0.0.0.0:8888/rs

Resources: /customer, /payer, /subscriber, /contact, /contact/role, /address, /address/role, /service       

SOAP interface
==============

Sample Yoda script is located in /var/local/hydratk/yoda/yoda-tests/testenv/soap.yoda.

The interface provides same methods as DB interface, so only the client initialiazation is described.

Create SOAP client
  .. code-block:: python
  
     # import helpers
     import testenv_helpers as hlp
    
     # create SOAP client instance
     client = client = hlp.soap()
     
SOAP services are hosted on endpoint 0.0.0.0:8888/ws/crm     

Service specification: crm?wsdl, crm?xsd

Data model
==========

Customer structure
^^^^^^^^^^^^^^^^^^

 .. graphviz::
   
   digraph customer_structure {
      graph [rankdir=TB]
      node [shape=box, style=filled, color=white, fillcolor=lightgrey]
    
      customer
      payer
      subscriber
      lov_status
      lov_segment
      lov_billcycle
      lov_market
      lov_lov_tariff
      
      customer -> payer
      customer -> subscriber
      payer -> subscriber
      lov_status -> customer
      lov_status -> payer
      lov_status -> subscriber
      lov_segment -> customer
      lov_billcycle -> payer
      lov_market -> subscriber
      lov_tariff -> subscriber

   }
   
Contact and address
^^^^^^^^^^^^^^^^^^^

 .. graphviz::
   
   digraph contact_and_address {
      graph [rankdir=TB]
      node [shape=box, style="filled", color=white, fillcolor=lightgrey]
    
      customer
      payer
      subscriber
      contact
      contact_role
      address
      address_role
      lov_contact_role
      lov_address_role
      
      contact -> contact_role
      customer -> contact_role
      payer -> contact_role
      subscriber -> contact_role
      address -> address_role
      contact -> address_role
      customer -> address_role
      payer -> address_role
      subscriber -> address_role
      lov_contact_role -> contact_role
      lov_address_role -> address_role
        
   }
   
Services
^^^^^^^^

 .. graphviz::
   
   digraph contact_and_address {
      graph [rankdir=TB]
      node [shape=box, style="filled", color=white, fillcolor=lightgrey]
    
      customer
      payer
      subscriber
      service
      service_params
      lov_service
      lov_service_params
      lov_status
      
      customer -> service
      payer -> service
      subscriber -> service
      service -> service_params
      lov_service -> service
      lov_service_param -> service_params
      lov_status -> service
        
   }   
   
Tables
^^^^^^

**customer**:

Storage of customers

===========  ======== ======== =============================
Column       Datatype Nullable Constraint 
===========  ======== ======== =============================
id           integer     N     primary key autoincrement
name         varchar     N
status       integer     N     foreign key to lov_status.id
segment      integer     N     foreign key to lov_segment.id
birth_no     varchar     Y
reg_no       varchar     Y
tax_no       varchar     Y
create_date  datetime    Y
modify_date  datetime    Y
===========  ======== ======== =============================

**payer**:

Storage of payers

============  ======== ======== ===============================
Column        Datatype Nullable Constraint 
============  ======== ======== ===============================
id            integer     N     primary key autoincrement
name          varchar     N
status        integer     N     foreign key to lov_status.id
billcycle     integer     N     foreign key to lov_billcycle.id
bank_account  varchar     Y
customer      integer     N     foreign key to customer.id
create_date   datetime    Y
modify_date   datetime    Y
============  ======== ======== ===============================

**subscriber**:

Storage of subscribers

===========  ======== ======== =============================
Column       Datatype Nullable Constraint 
===========  ======== ======== =============================
id           integer     N     primary key autoincrement
name         varchar     N
msisdn       varchar     N
status       integer     N     foreign key to lov_status.id
market       integer     N     foreign key to lov_segment.id
tariff       varchar     N     foreign key to lov_tariff.id
customer     integer     N     foreign key to customer.id
payer        integer     N     foreign key to payer.id
create_date  datetime    Y
modify_date  datetime    Y
===========  ======== ======== =============================

**contact**:

Storage of contacts

===========  ======== ======== =============================
Column       Datatype Nullable Constraint 
===========  ======== ======== =============================
id           integer     N     primary key autoincrement
name         varchar     N
phone        varchar     Y
email        varchar     Y
create_date  datetime    Y
modify_date  datetime    Y
===========  ======== ======== =============================

**contact_role**:

Storage of contact roles

============  ======== ======== ==================================
Column        Datatype Nullable Constraint 
============  ======== ======== ==================================
id            integer     N     primary key autoincrement
contact_role  integer     N     foreign key to lov_contact_role.id
contact       integer     N     foreign key to contact.id
customer      integer     Y     foreign key to customer.id
payer         integer     Y     foreign key to payer.id
subscriber    integer     Y     foreign key to subscriber.id
create_date   datetime    Y
============  ======== ======== ==================================

**addresss**:

Storage of addresses

===========  ======== ======== =============================
Column       Datatype Nullable Constraint 
===========  ======== ======== =============================
id           integer     N     primary key autoincrement
street       varchar     N
street_no    varchar     N
city         varchar     N
zip          integer     N
create_date  datetime    Y
modify_date  datetime    Y
===========  ======== ======== =============================

**address_role**:

Storage of address roles

============  ======== ======== ==================================
Column        Datatype Nullable Constraint 
============  ======== ======== ==================================
id            integer     N     primary key autoincrement
address_role  integer     N     foreign key to lov_address_role.id
address       integer     N     foreign key to address.id
contact       integer     Y     foreign key to contact.id
customer      integer     Y     foreign key to customer.id
payer         integer     Y     foreign key to payer.id
subscriber    integer     Y     foreign key to subscriber.id
create_date   datetime    Y
============  ======== ======== ==================================

**service**:

Storage of services

===========  ======== ======== =============================
Column       Datatype Nullable Constraint 
===========  ======== ======== =============================
id           integer     N     primary key autoincrement
service      integer     N     foreign key to lov_service.id
status       integer     N     foreign key to lov_status.id
customer     integer     Y     foreign key to customer.id
payer        integer     Y     foreign key to payer.id
subscriber   integer     Y     foreign key to subscriber.id
create_date  datetime    Y
modify_date  datetime    Y
===========  ======== ======== =============================

**service_params**:

Storage of service parameters

===========  ======== ======== ===================================
Column       Datatype Nullable Constraint 
===========  ======== ======== ===================================
id           integer     N     primary key autoincrement
param        integer     N     foreign key to lov_service_param.id
value        varchar     Y
service      integer     N     foreign key to lov_service.id
create_date  datetime    Y
modify_date  datetime    Y
===========  ======== ======== ===================================

**history**:

Auditing table, operation with every entity is logged.

===========  ======== ======== =========================
Column       Datatype Nullable Constraint 
===========  ======== ======== =========================
id           integer     N     primary key autoincrement
event_date   datetime    N
table_name   varchar     N
table_id     integer     N
event        varchar     N
log          clob        Y
===========  ======== ======== =========================

**lov_status**:

List of statuses

===========  ======== ======== ===========
Column       Datatype Nullable Constraint 
===========  ======== ======== ===========
id           integer     N     primary key
title        varchar     N
===========  ======== ======== ===========

Following statuses are configured

== ========
id title
== ========
1  active
2  deactive
3  suspend
== ========

**lov_segment**:

List of customer segments

===========  ======== ======== ===========
Column       Datatype Nullable Constraint 
===========  ======== ======== ===========
id           integer     N     primary key
title        varchar     N
===========  ======== ======== ===========

Following segment are configured

== =====
id title
== =====
2  RES
3  VSE
4  SME
5  LE
== =====

**lov_billcycle**:

List of payer billcycles

===========  ======== ======== ===========
Column       Datatype Nullable Constraint 
===========  ======== ======== ===========
id           integer     N     primary key
title        varchar     N
===========  ======== ======== ===========

Following billcycles are configured

== =====
id title
== =====
1  51
2  52
3  53
4  54
== =====

**lov_market**:

List of subscriber markets

===========  ======== ======== ===========
Column       Datatype Nullable Constraint 
===========  ======== ======== ===========
id           integer     N     primary key
title        varchar     N
===========  ======== ======== ===========

Following statuses are configured

== =====
id title
== =====
1  GSM
2  DSL
3  FIX
== =====

**lov_tariff**:

List of subscriber tariffs

===========  ======== ======== ===========
Column       Datatype Nullable Constraint 
===========  ======== ======== ===========
id           integer     N     primary key
title        varchar     N
segment      integer     Y
market       integer     Y
monthly_fee  integer     Y
===========  ======== ======== ===========

Following tariffs are configured

=== ========================================
id  title
=== ========================================
433 S nami sit nesit
459 S nami sit nesit bez zavazku
434 S nami sit nesit v podnikani
460 S nami sit nesit v podnikani bez zavazku
=== ========================================

**lov_contact_role**:

List of contact roles

===========  ======== ======== ===========
Column       Datatype Nullable Constraint 
===========  ======== ======== ===========
id           integer     N     primary key
title        varchar     N
===========  ======== ======== ===========

Following roles are configured

== =========
id title
== =========
1  contact
2  contract
3  invoicing
== =========

**lov_address_role**:

List od address roles

===========  ======== ======== ===========
Column       Datatype Nullable Constraint 
===========  ======== ======== ===========
id           integer     N     primary key
title        varchar     N
===========  ======== ======== ===========

Following roles are configured

== =========
id title
== =========
1  contact
2  contract
3  invoicing
4  delivery
== =========

**lov_service**:

List of services

===========  ======== ======== ===========
Column       Datatype Nullable Constraint 
===========  ======== ======== ===========
id           integer     N     primary key
title        varchar     N
monthly_fee  integer     Y
customer     integer     Y
payer        integer     Y
subscriber   integer     Y
===========  ======== ======== ===========

Following services are configured

=== =============== ======== ===== ==========
id  title           customer payer subscriber
=== =============== ======== ===== ==========
615 Telefonni cislo    0       0       1 
619 SIM karta          0       0       1
=== =============== ======== ===== ==========

**lov_service_param**:

List of service parameters

=============  ======== ======== =============================
Column         Datatype Nullable Constraint 
=============  ======== ======== =============================
id             integer     N     primary key
title          varchar     N
service        integer     N     foreign key to lov_service.id
default_value  varchar     Y
mandatory      integer     Y
=============  ======== ======== =============================

Following parameters are configured

Following statuses are configured

=== ======== ======= =========
id  title    service mandatory
=== ======== ======= =========
121 MSISDN   615         1
122 ICCID    619         1
123 IMSI     619         1
=== ======== ======= =========