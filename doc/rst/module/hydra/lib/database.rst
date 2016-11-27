.. _module_hydra_lib_database:

database
========

This sections contains module documentation of database modules.

dbo
^^^

Module provides class DBO as general database interface.

Supported drivers:

* sqlite - implemented in hydratk
* mssql - implemented in hydratk-lib-network
* mysql - implemented in hydratk-lib-network
* oracle - implemented in hydratk-lib-network
* pgsql - implemented in hydratk-lib-network

**Attributes** :

* _dbo_driver - reference to DBODriver
* _driver_name - name of database driver

**Properties (Getters)** :

* driver_name - returns _driver_name

**Methods** :

* __init__

Method imports and initializes requested DBODriver implemented by different driver modules.
It extracts driver name from DSN and raises DBOException when driver is not implemented.

* _import_dbo_driver

Method imports driver module.

* _get_driver_from_dsn

Method extracts driver name from DSN (driver:...).

**Class DBOException**

Custom exception class with attributes (_error_info, _code, _message, _code, _file, _line).

dbodriver
^^^^^^^^^

Module provides class DBODriver as abstract class to be extended by each driver.

**Attributes** :

* _cursor - database cursor
* _dbcon - database connection
* _result_as_dict - bool, return query output in dictionary form
* _dsn - database DSN
* _driver_options - driver configuration
* _username - username
* _password - password

**Properties (Getters)** :

* dbcon - returns _dbcon
* cursor - returns _cursor

**Methods** :

* __init__

Method sets driver attributes and connects to database if allowed (parameter autoconnect).

**Abstract methods** :

Drivers implement some of them.

* connect
* close
* commit
* error_code
* error_info
* qexec
* get_attribute
* in_transaction
* last_insert_id
* prepare
* query
* quote
* rollback
* set_attribute
* table_exists
* database_exists
* remove_database

sqlite
^^^^^^

Module driver provides class DBODriver which impletements client SQLite database using standard module 
`sqlite3 <https://docs.python.org/3.6/library/sqlite3.html>`_.
Unit tests available at hydratk/lib/database/dbo/sqlite/01_methods_ut.jedi 

**Attributes** :

* _mode - FILE or MEMORY
* _dbfile - database file
* _driver_options - configuration dictionary (timeout, factory, ...)

**Methods** :

* _detect_mode

Method sets _mode according to dsn FILE (contains :) or MEMORY (contains ::). 

* _parse_dsn

Method parses dsn (connection string). Sets _db_file.

  .. code-block:: python
  
     from hydratk.lib.database.dbo.dbo import DBO
     
     dsn = 'sqlite:/var/local/hydratk/test.db3'
     c = DBO(dsn)
     res = d._parse_dsn(dsn)     

* _apply_driver_options

Method updates driver options.

  .. code-block:: python
  
     opt = {'timeout': 10}
     d._apply_driver_options(opt)

* connect

Method connects to server using sqilite3 method connect. Parameters are already set by method _parse_dsn.
When database file not exists the method creates it.

  .. code-block:: python
  
     dsn = 'sqlite:/var/local/hydratk/test.db3'
     c = DBO(dsn)
     d.connect()  

* close

Method disconnects from server using sqlite3 method close.

* commit

Method commits transaction using sqlite3 method commit.

* execute

Method executes query using sqlite3 method execute and returns cursor (results must be extracted i.e. using method fetchall).

  .. code-block:: python
   
     # read query
     res = d.execute('SELECT count(*) FROM customer').fetchall()
     
     # write query 
     d.execute('INSERT INTO lov_status VALUES (4, \'test\')')
     
     # variables binding
     res = d.execute('SELECT * FROM lov_status WHERE id = %s', [4]).fetchall()

* rollback

Method rollbacks transaction using sqlite3 method rollback.

* __getitem__

Method gets given psycopg2 attribute if exists.

* __getattr__

Method gets given connection or psycopg2 attribute if exists.

* table_exists

Method checks if given table exists in database. It executes special query
SELECT count(*) found FROM sqlite_master where type='table' and tbl_name=?.

  .. code-block:: python
  
     res = d.table_exists('customer')
     
* database_exists

Method checks whether database file is created and not empty.

  .. code-block:: python
  
     res = d.database_exists() 
     
* remove_database

Method deletes database file.

  .. code-block:: python
  
     res = d.remove_database()              

* erase_database

Method drops all tables in database. It executes special query select name from sqlite_master where type is 'table'. 
Then it drops them using query.

* result_as_dict

Method sets row factory to return query result in dictionary form.

  .. code-block:: python
  
     # no dictionary
     d.result_as_dict(False)
     recs = d.execute('SELECT * FROM lov_status').fetchall()    
     # access recs[0][1]
     
     # dictionary
     d.result_as_dict(True)
     recs = d.execute('SELECT * FROM lov_status').fetchall()
     # access recs[0]['title']      