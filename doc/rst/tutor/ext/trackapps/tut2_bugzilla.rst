.. _tutor_trackapps_tut2_bugzilla:

Tutorial 2: Bugzilla
====================

Bugzilla interface supports operations with bugs. 
You can read, create and update them.

Command line
^^^^^^^^^^^^

It is controlled via command track with following options.

Mandatory:

* --tr-app <name>: application, use bugzilla
* --tr-action <name>: action, read|create|update

Optional:

* --tr-input <path>: filename, content is written to bug description, supported for actions: create|update
* --tr-output <path>: filename, action output is written, supported for action: read
* --tr-url <string>: url, configurable
* --tr-user <string>: username, configurable
* --tr-passw <string>: password, configurable
* --tr-id <num>: record id, optional for action: read, mandatory for action: update
* --tr-fields <list>: request record fields, configurable, list form - name1,name2, supported for action: read
* --tr-query <string>: query, Bugzilla specific expression, supported for action: read
* --tr-limit <num>: record limit, supported for action: read
* --tr-offset <num>: record offset, supported for action: read
* --tr-params <dict>: record params, dictionary form - name1:value,name2:value, supported for actions create|update

Configuration
^^^^^^^^^^^^^

Use section bugzilla in configuration file.

* url: Bugzilla server url, used as --tr-url option
* user: username, used as --tr-user option
* passw: password, used as --tr-passw option                                                                                                  
* return_fields: record fields returned within read (all by default), used as --tr-fields option, use list form, name1,name2,name3                                      
* required_fields: required fields to create new record, user will be asked if not provided in --tr-params option, use list form, name1,name2,name3                                     
* default_values: default field values to create new record, used both for required and optional fields, use dictionary form, name: value                                      
* lov: list of values for required fields, list will be offered to user within create, use dictionary form, name: value1,value2,value3

  .. note::
  
     Parameters provided as command options override configured values.

Example

  .. code-block:: yaml
  
     TrackApps:
       bugzilla:
         url: url
         user: username
         passw: password
         return_fields: product,component,summary,version,creator 
         required_fields: product,component,summary,version   
         default_values:
           product: FooBar
           component: Bar
         lov:
       
Examples
^^^^^^^^ 

Some parameters are configured to make command examples shorter.

  .. code-block:: bash  
     
     # create bug
     # required fields are provided or have configured default value
     $ htk --tr-app bugzilla --tr-action create --tr-params "summary:test hydra,version:1" track
     
     Record 1034 created
     
     # read created bug
     # id=1034, only 4 fields are returned
     $ htk --tr-app bugzilla --tr-action read --tr-id 1034 --tr-fields "creator,severity,summary,product" track
     
     [{u'product': u'FooBar', u'summary': u'test hydra', u'severity': u'<unspecified>', u'creator': u'demo@devzing.com'}]     
     
     # update bug
     # id=1034, field summary is updated
     $ htk --tr-app bugzilla --tr-action update --tr-id 1034 --tr-params "summary:test hydra 2" track 
     
     Record 1034 updated
     
     # read updated bug
     $ htk --tr-app bugzilla --tr-action read --tr-id 1034 --tr-fields "creator,severity,summary,product" track
     
     [{u'product': u'FooBar', u'summary': u'test hydra 2', u'severity': u'<unspecified>', u'creator': u'demo@devzing.com'}]
     
  .. note::
  
     More examples are available in QC tutorial.   
     
API
^^^

This section shows several examples how to use Bugzilla interface as API in your extensions/libraries.
API uses HydraTK core functionalities so it must be running.

Methods    

* connect: connect to Bugzilla, params: url, user, passw
* disconnect: disconnect from Bugzilla
* read: read bugs, params: id, fields, query, limit, offset
* create: create bug, params: params
* update update bug, params, id: params     

Examples

  .. code-block:: python
  
     # import client
     from hydratk.extensions.trackapps.bugzilla import Client
     c = Client()
     
     # connect
     res = c.connect(url, user, passw, project)
     
     # read issue
     id = 40
     fields = ['creator', 'severity', 'summary', 'product']
     res, records = c.read(id, fields=fields) 
     
     # create bug
     params = {'summary': 'test hydra', 'version': '1'}
     id = c.create(params)        
     
     # update bug
     params = {'summary': 'test hydra 2'}
     res = c.update(id, params) 
     
     # disconnect
     res = c.disconnect()     