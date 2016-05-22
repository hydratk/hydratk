.. _tutor_trackapps_tut5_jira:

Tutorial 5: Jira
================

Jira interface supports operations with issues. 
You can read, create and update them.

Command line
^^^^^^^^^^^^

It is controlled via command track with following options.

Mandatory:

* --app <name>: application, use jira
* --action <name>: action, read|create|update

Optional:

* --input <path>: filename, content is written to issue description, supported for actions: create|update
* --output <path>: filename, action output is written, supported for action: read
* --url <string>: url, configurable
* --user <string>: username, configurable
* --passw <string>: password, configurable
* --project <string>: project, configurable
* --id <num>: record id, optional for action: read, mandatory for action: update|delete
* --fields <list>: request record fields, configurable, list form - name1,name2, supported for action: read
* --query <string>: query, Jira specific expression, supported for action: read
* --limit <num>: record limit, supported for action: read
* --offset <num>: record offset, supported for action: read
* --params <dict>: record params, dictionary form - name1:value,name2:value, supported for actions create|update

Configuration
^^^^^^^^^^^^^

Use section jira in configuration file.

* url: Jira server url, used as --url option
* user: username, used as --user option
* passw: password, used as --passw option
* project: project, used as --project option                                                                                                  
* return_fields: record fields returned within read (all by default), used as --fields option, use list form, name1,name2,name3                                      
* required_fields: required fields to create new record, user will be asked if not provided in --params option, use list form, name1,name2,name3                                     
* default_values: default field values to create new record, used both for required and optional fields, use dictionary form, name: value                                      
* lov: list of values for required fields, list will be offered to user within create, use dictionary form, name: value1,value2,value3

  .. note::
  
     Parameters provided as command options override configured values.

Example

  .. code-block:: yaml
  
     TrackApps:
       jira:
         url: url
         user: username
         passw: password
         project: DEMO
         return_fields: summary,description,id,status,priority
         required_fields: summary,description,priority
         default_values:                    
           priority: {'name': 'Minor'}
         lov: 
         
Examples
^^^^^^^^ 

Some parameters are configured to make command examples shorter.

  .. code-block:: bash      
     
     # create issue
     # required fields are provided or have configured default value
     $ htk --app jira --action create --params "summary:hydra test,description:hydra desc" track
     
     Record 8595 created
     
     # read created issue
     # id=8595, configured fields are returned
     $ htk --app jira --action read --id 8594 --fields "id,status,creator,description" track  
     
     [{u'summary': u'hydra test', u'description': u'hydra desc', u'id': u'8595', u'status': u'New', u'priority': u'Minor'}]    
     
     # update issue
     # id=8595, field summary is updated
     $ htk --app jira --action update --id 8595 --params "summary:test hydra 2" track  
     
  .. note::
  
     More examples are available in QC tutorial.   
     
API
^^^

This section shows several examples how to use Jira interface as API in your extensions/libraries.
API uses HydraTK core functionalities so it must be running.

Methods

* connect: connect to Jira, params: url, user, passw, project
* disconnect: disconnect from Jira
* read: read issues, params: id, fields, query, limit, offset
* create: create issue, params: params
* update: update issue, params: id, params

Examples    
            
  .. code-block:: python
  
     # import client
     from hydratk.extensions.trackapps.jira import Client
     c = Client()
     
     # connect
     res = c.connect(url, user, passw, project)
     
     # read issue
     id = 8594
     fields = ['id', 'status', 'creator', 'description']
     res, records = c.read(id, fields)
     
     # create issue
     params = {'summary': 'hydra test', 'description': 'hydra desc', 'priority': {'name': 'Minor'}}
     id = c.create(params) 
     
     # update issue
     params = {'summary': 'test hydra 2'}
     res = c.update(id, params)                