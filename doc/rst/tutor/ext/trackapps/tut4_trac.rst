.. _tutor_trackapps_tut4_trac:

Tutorial 4: Trac
================

Trac interface supports operations with tickets. 
You can read, create, update and delete them.

Command line
^^^^^^^^^^^^

It is controlled via command track with following options.

Mandatory:

* --tr-app <name>: application, use trac
* --tr-action <name>: action, read|create|update|delete

Optional:

* --tr-input <path>: filename, content is written to ticket description, supported for actions: create|update
* --tr-output <path>: filename, action output is written, supported for action: read
* --tr-url <string>: url, configurable
* --tr-user <string>: username, configurable
* --tr-passw <string>: password, configurable
* --tr-project <string>: project, configurable
* --tr-id <num>: record id, optional for action: read, mandatory for action: update|delete
* --tr-fields <list>: request record fields, configurable, list form - name1,name2, supported for action: read
* --tr-query <string>: query, Trac specific expression, supported for action: read
* --tr-params <dict>: record params, dictionary form - name1:value,name2:value, supported for actions create|update

Configuration
^^^^^^^^^^^^^

Use section trac in configuration file.

* url: Trac server url, used as --tr-url option
* user: username, used as --tr-user option
* passw: password, used as --tr-passw option
* project: project, used as --tr-project option                                                                                                  
* return_fields: record fields returned within read (all by default), used as --tr-fields option, use list form, name1,name2,name3                                      
* required_fields: required fields to create new record, user will be asked if not provided in --tr-params option, use list form, name1,name2,name3                                     
* default_values: default field values to create new record, used both for required and optional fields, use dictionary form, name: value                                      
* lov: list of values for required fields, list will be offered to user within create, use dictionary form, name: value1,value2,value3

  .. note::
  
     Parameters provided as command options override configured values.

Example

  .. code-block:: yaml
  
     TrackApps:
       trac:
         url: url
         user: username
         passw: password
         project: project1
         return_fields: summary,type,priority,description
         required_fields: summary,description
         default_values:
           type: defect
           priority: major
         lov:  
         
Examples
^^^^^^^^ 

Some parameters are configured to make command examples shorter.

  .. code-block:: bash      
     
     # read tickets
     # tickets which are not closed, configured fields are returned
     $ htk --tr-app trac --tr-action read --tr-query "status!=closed" track   
     
     [{'priority': 'major', 'type': 'enhancement', 'description': 'make it better', 'summary': 'Make i2 better'}, 
      {'priority': 'major', 'type': 'defect', 'description': 'This is a test', 'summary': 'Testing Trac opening a ticket'}, 
      {'priority': 'major', 'type': 'enhancement', 'description': u'masse am schati \xfcberpr\xfcfen', 'summary': 'neues ticket'}, 
      {'priority': 'major', 'type': 'defect', 'description': u'La pantalla de monitoreo no est\xe1 mostrando los datos que quedamos: n\xfamero de serie, fecha de fabricaci\xf3n.', 'summary': 'Pantalla monitoreo'}, 
      {'priority': 'major', 'type': 'defect', 'description': 'make it better', 'summary': 'Make i2 better'}, 
      {'priority': 'major', 'type': 'defect', 'description': 'make it better', 'summary': 'Make i2 better'}, 
      {'priority': 'major', 'type': 'defect', 'description': 'make it better', 'summary': 'Make i2 better'}, 
      {'priority': 'major', 'type': 'defect', 'description': 'make it better', 'summary': 'Make i2 better'}, 
      {'priority': 'major', 'type': 'defect', 'description': 'make it better', 'summary': 'Make i2 better'}, 
      {'priority': 'major', 'type': 'defect', 'description': 'test2', 'summary': 'test2'}, 
      {'priority': 'major', 'type': 'defect', 'description': 'test', 'summary': 'test'}, 
      {'priority': 'major', 'type': 'defect', 'description': 'test', 'summary': 'test'}, 
      {'priority': 'major', 'type': 'defect', 'description': 'update ticket\n\n\nupdate tiket\n', 'summary': 'test'}]         
     
     # create ticket
     # required fields are provided or have configured default value
     htk --tr-app trac --tr-action create --tr-params "summary:hydra test,description:hydra desc" track
     
     Record 16 created     
     
     # update ticket
     # id=16, field keywords is updated
     htk --tr-app trac --tr-action update --tr-id 16 --tr-params "keywords:hydratk" track
     
     Record 16 updated 
     
     # delete ticket
     # id=6
     $ htk --tr-app trac --tr-action delete --tr-id 6 track 
     
     Record 6 deleted    
     
  .. note::
  
     More examples are available in QC tutorial.  
     
API
^^^

This section shows several examples how to use Trac interface as API in your extensions/libraries.
API uses HydraTK core functionalities so it must be running.

Methods

* connect: connect to Trac, params: url, user, passw, project
* read: read tickets, params: id, fields, query
* create: create ticket, params:  params
* update: update ticket, params: id, params
* delete: delete ticket, params: id

Examples    

  .. code-block:: python
  
     # import client
     from hydratk.extensions.trackapps.trac import Client
     c = Client()
     
     # connect
     res = c.connect(url, user, passw, project)
     
     # read tickets
     res, rec = c.read(query='status!=closed')
     
     # create ticket
     params = {'summary': 'hydra test', 'description': 'hydra desc'}
     id = c.create(params) 
     
     # update ticket
     res = c.update(id, {'keywords': 'hydratk'})
     
     # delete ticket
     res = c.delete(id)           