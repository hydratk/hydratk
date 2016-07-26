.. _tutor_network_tut1_dbi:

Tutorial 1: Database
====================

This sections shows several examples how to use database client.

API
^^^

Module hydratk.lib.network.dbi.client.

Method DBClient is factory method which requires attribute engine to create 
proper DBClient object instance. Additional attributes are passed as args, kwargs. 

Supported engines:

* SQLite - module sqlite_client
* Oracle - module oracle_client
* MySQL - module mysql_client
* PostgreSQL - module postgresql_client
* JDBC - module jdbc_client

Methods:

* connect: connect to database file (SQLite) or database server (Oracle, MySQL, PostgreSQL, JDBC)  
* disconnect: disconnect from database
* exec_query: execute query, prepared statements with variable bindings are supported (use ? character)
* call_proc: call procedure (has no return param) or function (has return param), supported for Oracle, MySQL
* commit: commit transaction
* rollback: rollback transaction
* close: stop JVM, supported for JDBC

  .. note::
   
     API uses HydraTK core functionalities so it must be running.

SQLite
^^^^^^

  .. code-block:: python
  
     # import library
     from hydratk.lib.network.dbi.client import DBClient
     
     # initialize client
     client = DBClient('sqlite')
     
     # connect to database
     # returns bool
     client.connect(db_file='/home/lynus/hydratk/testenv.db3')
     
     # select records from table
     # returns bool, list of rows
     res, rows = client.exec_query('SELECT * FROM LOV_STATUS')
     
     for row in rows:
         print row 
     
     # insert record to table
     client.exec_query('INSERT INTO LOV_STATUS (id, title) VALUES (4, \'pokus\')')
     
     # delete record from table
     client.exec_query('DELETE FROM LOV_STATUS WHERE id = 4;')
     
     # insert record using prepared statement with variable binding
     client.exec_query('INSERT INTO LOV_STATUS (id, title) VALUES (?, ?)', [4, 'pokus 2'])
     
     # delete record using prepared statement with variable binding
     client.exec_query('DELETE FROM LOV_STATUS WHERE id = ?', [4])
     res, rows = client.exec_query('SELECT title FROM LOV_STATUS')
     
     # disconnect from database
     # returns bool
     client.disconnect()
     
Oracle
^^^^^^

Oracle client is not bundled with HydraTK and must be installed individually.

  .. code-block:: python
  
     # import library
     import hydratk.lib.network.dbi.client as db
    
     # initialize client
     client = db.DBClient('oracle')  
     
     # connect to database
     client.connect(host='localhost', port=49161, sid='XE', user='crm', passw='crm')   
     
     # call function
     param_names = ['id', 'name', 'status', 'segment', 'birth_no', 'reg_no', 'tax_no', 'err']
     input_values = {'name': 'Charlie Bowman', 'status': 'active', 'segment': 2,
                     'birth_no': '840809/0009', 'reg_no': '12345', 'tax_no': 'CZ12345'}
     output_types = {'id': 'int', 'err': 'string'}
     result_type = 'int'
     
     # returns result, output param values dictionary
     res, params = client.call_proc('crm.customer_pck.f_create', param_names, input_values, output_types, 'func', result_type)
                      
     # call procedure
     param_names = ['id', 'name', 'status', 'segment', 'birth_no', 'reg_no', 'tax_no', 'err']
     input_values = {'id': id}
     output_types = {'name': 'string', 'status': 'string', 'segment': 'int',
                     'birth_no': 'string', 'reg_no': 'string', 'tax_no': 'string', 'err': 'string'}
                     
     # returns output param values dictionary                     
     params = client.call_proc('crm.customer_pck.p_read', param_names, input_values, output_types, 'proc')
     
     # disconnect from database
     # returns bool
     client.disconnect() 
     
JDBC
^^^^

Part of JDBC client library is implemented in Java as a wrapper application which uses Java JDBC API.
Python client library uses Java bridge to create Java object instance. 
Specific Java libraries are needed to access database via JDBC, they are not bundled with hydratk.
 
After installation do following actions:
1. Check that directory /var/local/hydratk/java was created and contains files: DBClient.java, DBClient.class.
2. Store specific client jar file to same directory (i.e. ojdbc6.jar).

  .. code-block:: python
  
     # import library
     import hydratk.lib.network.dbi.client as db
    
     # initialize client
     client = db.DBClient('jdbc', True)  
     
     # connect to database
     client.connect(driver='oracle.jdbc.driver.OracleDriver', conn_str='jdbc:oracle:thin:@localhost:49161/XE', user='crm', passw='crm')   
     
     # select records from table
     # returns bool, list of rows
     res, rows = client.exec_query('SELECT * FROM LOV_STATUS')
     
     for row in rows:
         print row 
     
     # insert record to table
     client.exec_query('INSERT INTO LOV_STATUS (id, title) VALUES (4, \'pokus\')')
                     
     # returns output param values dictionary                     
     params = client.call_proc('crm.customer_pck.p_read', param_names, input_values, output_types, 'proc')
     
     # disconnect from database
     # returns bool
     client.disconnect() 
     
     # stop JVM
     client.stop()
     
MySQL
^^^^^

MySQL client is similar to Oracle and no specific examples are shown here.

PostgreSQL
^^^^^^^^^^   

PostgreSQL client is similar to Oracle and no specific examples are shown here.  