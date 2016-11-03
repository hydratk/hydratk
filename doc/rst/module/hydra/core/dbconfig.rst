.. _module_hydra_core_dbconfig:

dbconfig
========

This sections contains module documentation of dbconfig module.

dbconfig
^^^^^^^^

Module provides class DBConfig with configuration database client.
Unit tests available at hydratk/core/dbconfig/01_methods_ut.jedi

Database has simple structure with one table.

**config**:

==========  ======== ======== ==========
Column      Datatype Nullable Constraint 
==========  ======== ======== ==========
grp         varchar     N     
obj         varchar     N
key         varchar     N     
value       varchar     Y     
enabled     integer     Y
lvl4_key    varchar     Y
lvl4_value  varchar     Y
lvl5_key    varchar     Y
lvl5_value  varchar     Y
==========  ======== ======== ==========

**Attributes** :

* _db_file - database file
* _conn - database connection

**Methods** :

* __init__

Method sets _db_file.

* connect

Method connects to database and sets _conn.

* write_db

Method stores dictionary configuration to database table config.

* cfg2db

Method transforms dictionary configuration (multiple levels) to form which is directly writable to database.

* db2cfg

Method reads configuration from database and returns cursor output. It can read only active records if enabled (by default False).