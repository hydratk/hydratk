.. _tutor_trackapps_tut3_mantis:

Tutorial 3: Mantis
==================

Mantis interface supports operations with issues. 
You can read, create, update and delete them.

Command line
^^^^^^^^^^^^

It is controlled via command track with following options.

Mandatory:

* --app <name>: application, use mantis
* --action <name>: action, read|create|update|delete

Optional:

* --input <path>: filename, content is written to issue description, supported for actions: create|update
* --output <path>: filename, action output is written, supported for action: read
* --url <string>: url, configurable
* --user <string>: username, configurable
* --passw <string>: password, configurable
* --project <string>: project, configurable
* --id <num>: record id, optional for action: read, mandatory for action: update|delete
* --fields <list>: request record fields, configurable, list form - name1,name2, supported for action: read
* --page <num>: record page, supported for action: read
* --per-page <num>: records per page, supported for action: read
* --params <dict>: record params, dictionary form - name1:value,name2:value, supported for actions create|update

Configuration
^^^^^^^^^^^^^

Use section mantis in configuration file.

* url: Mantis server url, used as --url option
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
       mantis:
         url: url
         user: username
         passw: password
         project: Sample Project
         return_fields: category,summary,description,reporter,priority,severity
         required_fields: category,summary,description
         default_values:
           category: defect
         lov:
         
Examples
^^^^^^^^ 

Some parameters are configured to make command examples shorter.

  .. code-block:: bash      
     
     # create issue
     # required fields are provided or have configured default value
     $ htk --app mantis --action create --params "summary:hydra test,description:hydra desc" track
     
     Record 6 created
     
     # read created issue
     # id=6, configured fields are returned
     $ htk --app mantis --action read --id 6 track    
     
     [{u'category': u'defect', u'summary': u'hydra test', u'description': u'hydra desc', u'reporter': u'xx', u'priority': u'1', u'severity': u'1'}]    
     
     # update issue
     # id=6, field summary is updated
     $ htk --app mantis --action update --id 6 --params "summary:hydratk" track
     
     Record 6 updated 
     
     # delete issue
     # id=6
     $ htk --app mantis --action delete --id 6 track
     
     Record 6 deleted    
     
  .. note::
  
     More examples are available in QC tutorial. 
     
API
^^^

This section shows several examples how to use Mantis interface as API in your extensions/libraries.
API uses HydraTK core functionalities so it must be running.

Methods

* connect: connect to Mantis, params: url, user, passw, project
* read: read issues, params: id, fields, page, per_page
* create: create issue, params: params
* update: update issue, params, id: params
* delete: delete issue, params: id  

Examples  

  .. code-block:: python
  
     # import client
     from hydratk.extensions.trackapps.mantis import Client
     c = Client()
     
     # connect
     res = c.connect(url, user, passw, project)
     
     # read issue
     id = 6
     res, rec = c.read(id)
     
     # create issue
     params = {'summary': 'hydra test', 'description': 'hydra desc', 'category': '1'}
     id = c.create(params) 
     
     # update issue
     res = c.update(id, {'summary': 'hydratk'})
     
     # delete issue
     res = c.delete(id)              