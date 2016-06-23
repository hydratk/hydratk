.. _tutor_trackapps_tut1_qc:

Tutorial 1: Quality Center
==========================

QC interface supports operations with defects and test entities (test, folder, set, instance). 
You can read, create, update and delete them.

Command line
^^^^^^^^^^^^

It is controlled via command track with following options.

Mandatory:

* --tr-app <name>: application, use qc
* --tr-action <name>: action, read|create|update|delete

Optional:

* --tr-type <name>: entity type, default defect, defect|test-folder|test|test-set-folder|test-set|test-instance
* --tr-input <path>: filename, content is written to defect description, supported for actions: create|update
* --tr-output <path>: filename, action output is written, supported for action: read
* --tr-url <string>: url, configurable
* --tr-user <string>: username, configurable
* --tr-passw <string>: password, configurable
* --tr-domain <string>: domain, configurable
* --tr-project <string>: project, configurable
* --tr-id <num>: record id, optional for action: read, mandatory for actions: update|delete
* --tr-fields <list>: request record fields, configurable, list form - name1,name2, supported for action: read
* --tr-query <string>: query, QC specific expression, supported for action: read
* --tr-order-by <dict>: record ordering, dictionary form - name1:direction|name2:direction, direction asc|desc, supported for action: read
* --tr-limit <num>: record limit, supported for action: read
* --tr-offset <num>: record offset, supported for action: read
* --tr-params <dict>: record params, dictionary form - name1:value,name2:value, supported for actions create|update
* --tr-path <string>: directory path, dir1/di2, mandatory for use cases: read/create test folder|read/create test set, create test

Configuration
^^^^^^^^^^^^^

Use section qc in configuration file.

* url: QC server url, used as --tr-url option
* user: username, used as --tr-user option
* passw: password, used as --tr-passw option
* domain: domain, used as --tr-domain option
* project: project, used as --tr-project option                                                                                                  
* return_fields: record fields returned within read (all by default), used as --tr-fields option, use list form, name1,name2,name3                                      
* required_fields: required fields to create new record, user will be asked if not provided in --tr-params option, use list form, name1,name2,name3                                     
* default_values: default field values to create new record, used both for required and optional fields, use dictionary form, name: value                                      
* lov: list of values for required fields, list will be offered to user within create, use dictionary form, name: value1,value2,value3

QC interface supports multiple entities, entity must be specified within parameter.
Entities defect|test|test-set|test-instance are configurable.

  .. note::
  
     Parameters provided as command options override configured values.

Example

  .. code-block:: yaml
  
     TrackApps:
       qc:
         url: url
         user: username
         passw: password
         domain: RELEASE
         project: SimpleOnlineCompany  
         return_fields: 
           defect: name,owner,project,status,description
           test: name,subtype-id,owner,user-04,user-01,user-05,description
         required_fields:
           defect:
           test: name,subtype-id,owner,user-04,user-01,user-05,description,name
           test-set: subtype-id
           test-instance: cycle-id,test-id,test-order,subtype-id
         default_values:
           defect:
           test:
             subtype-id: MANUAL
             owner: x0549396
             user-05: xxx
           test-set:
             subtype-id: 'hp.qc.test-set.default'
           test-instance:
             test-order: 1
             subtype-id: 'hp.qc.test-instance.MANUAL'
         lov:
           defect:
           test:
             user-04: 31604_PoP CRM,31413_UDR User Data Repository
             user-01: 1-Urgent,2-Very High,3-High,4-Medium,5-Low
             
Examples
^^^^^^^^ 

Some parameters are configured to make command examples shorter.

Defects

  .. code-block:: bash
  
     # read defect 
     # id=8594, two fields are returned
     $ htk --tr-app qc --tr-action read --tr-id 8594 --tr-fields "summary,project" track
     
     [{u'summary': u'hydra test', u'project': u'SimpleOnlineCompany'}]
     
     # read defects 
     # query name starts with CRM, output is written to text file 
     $ htk --tr-app qc --tr-action read --tr-query "{name[CRM*]}" --tr-output defects.txt track
     
     # read defect
     # id=8594, connection parameters are provided
     # they are mandatory, if they are missing and not configured, user will be prompted
     $ htk --tr-app qc --tr-action read --tr-url --tr-user user --tr-passw passw --tr-domain dom --tr-project proj --tr-id 8594 track   
     
     # create defect 
     # required fields are provided or have configured default value
     # if some required field is missing and configured, user will be prompted (including lov if configured)
     $ htk --tr-app qc --tr-action create --tr-params "name:hydra,description:hydra desc" track

     Record 8595 created

     # create defect 
     # description is read from text file
     # required fields are provided or have configured default value
     $ htk --tr-app qc --tr-action create --tr-params "name:hydra" --tr-input defect.txt track
     
     Record 8595 created
     
     # update defect
     # id=8595, id is mandatory, user will be prompted if missing
     $ htk --tr-app qc --tr-action update --tr-id 8595 --tr-params "status:Closed" track
     
     Record 8595 updated
     
     # delete defect
     # id=8595, id is mandatory, user will be prompted if missing
     $ htk --tr-app --tr-action delete --tr-id 8595 track
     
     Record 8595 deleted             
     
Test entities

  .. code-block:: bash
  
     # read test folder
     # returns test under folder (test plan), output is printed
     # type=test-folder
     # path is mandatory, user will be prompted if missing
     $ htk --tr-app qc --tr-action read --tr-type test-folder --tr-path "Subject/.Trash/VAS" track
     
     # read test
     # id=1234, type=test
     $ htk --tr-app qc --tr-action read --tr-type test --tr-id 1234 track
     
     # create test folder
     # type=test-folder
     # path contains also new folder name (Subject/.Trash/VAS/ is existing folder, hydra is new folder)
     $ htk --tr-app qc --tr-action create --tr-type test-folder --tr-path "Subject/.Trash/VAS/hydra" track
     
     Record 1238 created
     
     # create test
     # type=test
     # required fields are provided or have configured default values
     $ htk --tr-app qc --tr-action create --tr-type test --tr-path "Subject/.Trash/VAS/hydra" --tr-params "name:test,subtype-id:MANUAL" track
     
     Record 1235 created
     
     # update test
     # type=test
     $ htk --tr-app qc --tr-action update --tr-type test --tr-id 1235 --tr-params "name:test 2" track
     
     Record 1235 updated
     
     # read test set folder 
     # type=test-set-folder
     # returns test sets under folder (test lab), output is written to text file
     # path is provided (folder id is not used)
     $ htk --tr-app qc --tr-action read --tr-type test-set-folder --tr-path "Root/.Trash/VAS" --tr-output sets.txt track
     
     # create test set folder
     # type=test-set-folder
     # path contains also new folder name (Root/.Trash/VAS is existing folder, hydra is new folder)
     $ htk --tr-app qc --tr-action create --tr-type test-set-folder --tr-path "Root/.Trash/VAS/hydra" track
     
     Record 1239 created
     
     # create test set
     # type=test-set
     # path is provided
     # required fields are provided or have configured default values
     $ htk --tr-app qc --tr-action create --tr-type test-set --tr-qc-path "Root/.Trash/VAS/hydra" --tr-params "name:set1,'subtype-id:hp.qc.test-set.default'" track
     
     Record 1236 created
     
     # create test instance 
     # type=test-instance
     # assign test 1235 to test set 1236 
     # required fields are provided or have configured default values
     $ htk --tr-app qc --tr-action create --tr-type test-instance --tr-params "cycle-id:1236,test-id:1235,test-order:1,subtype-id:hp.qc.test-instance.MANUAL" track
     
     Record 1237 created
     
     # update test instance
     # type=test-instance (test run)
     # id=1237, close it
     $ htk --tr-app qc --tr-action update --tr-type test-instance --tr-id 1237 --tr-params "status:Closed" track
     
     Record 1237 updated  
     
     .. note::
     
        Use option --type carefully. If not provided, defect is used by default.  
        
API
^^^

This section shows several examples how to use QC interface as API in your extensions/libraries.
API uses HydraTK core functionalities so it must be running.

Methods

* connect: connect to QC, params: url, user, passw, domain, project
* disconnect: disconnect from QC
* read: read entities, params: id, entity, fields, query, order_by, limit, offset 
* create: create entity, params: entity, params
* update: update entity, params: id, entity, params
* delete: delete entity, params: id, entity
* read_test_folder: read tests under test folder, params: path, entity
* create_test_folder: create test folder, params: path, name, entity
* read_test_set: read test sets under test set, params: id
* create_test_set: create test set in test folder, params: path, params

Examples

  .. code-block:: python
  
     # import client
     from hydratk.extensions.trackapps.qc import Client
     c = Client()
     
     # connect
     res = c.connect(url, user, passw, domain, project)
     
     # read defect
     entity = 'defect'
     query = '{ID[=100]}'
     fields = ['name', 'owner', 'user-04', 'user-05']
     res, records = c.read(entity=entity, fields=fields, query=query)  
     
     # create defect
     params = {'name': 'test', 'owner': 'x0549396', 'user-04': 'General', 'Status': 'New',
               'Detected on Date': '2016-03-07', 'Environment': 'Preproduction', 'Detected By': 'x0549396',
               'Defect Reason': '6 - Others', 'Severity': '5-Low', 'user-05': 'Other application',
               'Test Type': 'Sys-int Test', 'Description': 'Test'}
     id = c.create(entity, params)       
     
     # update defect
     params = {'name': 'test 2', 'Status': 'Closed'}
     res = c.update(id, entity, params) 
     
     # delete defect
     res = c.delete(id, entity)
     
     # disconnect
     res = c.disconnect()
     
Test entities

  .. code-block:: python  
  
     # import client
     from hydratk.extensions.trackapps.qc import Client
     c = Client()
     
     # connect
     res = c.connect(url, user, passw, domain, project)
     
     # read test
     entity = 'test'
     id = 49528
     res, records = c.read(id=id, entity=entity)  
     
     # read test folder
     path = 'Subject/02 SYSINTTEST/31604_PoP_CRM/01_Drop_1/03 Customer mngt/CUSTM001 Authentication'
     res, tests = c.read_test_folder(path)             
     
     # create test folder
     id = c.create_test_folder('Subject/.Trash/VAS', 'test')
     
     # create test
     params = {'name': 'test', 'subtype-id': 'MANUAL', 'owner': 'x0549396', 'user-04': '31604_PoP CRM',
               'user-01': '5-Low', 'user-05': 'xxx'}
     id = c.create_test('Subject/.Trash/VAS/test', params)      
     
     # disconnect
     res = c.disconnect()                   