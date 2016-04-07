.. TrackApps

=========
TrackApps
=========

TrackApps extension provides interface to bugtracking and test management applications.

Following applications are supported:

- **Quality Center** - bugtracking, test management 
- **Bugzilla** - bugtracking
- **Mantis** - bugtracking
- **Trac** - bugtracking
- **Jira** - bugtracking
- **TestLink** - test management

Installation
============

1. Download extension from https://git.hydratk.org/trackapps.git.
2. Install extension using command python setup.py install.
3. Check that extension was installed using command htk list-extensions.

Configuration
=============

Configuration file is stored in /etc/hydratk/conf.d/hydratk-ext-trackapps.conf.
Each application has own configuration block.

Commands
========

Extensions provides following commands:

- **track**: trackapps command line interface

Individual applications support only subset of command options.

Quality Center
==============

Methods
^^^^^^^

- **connect**: connect to QC, params: url, user, passw, domain, project
- **disconnect**: disconnect from QC
- **read**: read entities, params: id, entity, fields, query, order_by, limit, offset 
- **create**: create entity, params: entity, params
- **update**: update entity, params: id, entity, params
- **delete**: delete entity, params: id, entity
- **read_test_folder**: read tests under test folder, params: path, entity
- **create_test_folder**: create test folder, params: path, name, entity
- **read_test_set**: read test sets under test set, params: id
- **create_test_set**: create test set in test folder, params: path, params
- **create_test**: create test in test folder, params: path, params

Command options
^^^^^^^^^^^^^^^

- **--app**: application, use qc
- **--action**: actions, read|create|update|delete
- **[--type]**: entity type, default defect, defect|test-folder|test|test-set-folder|test-set|test-instance
- **[--input]**: filename, content is written to defect description, supported for actions: create|update
- **[--output]**: filename, action output is written, supported for action: read
- **[--url]**: url, configurable
- **[--user]**: username, configurable
- **[--passw]**: password, configurable
- **[--domain]**: domain, configurable
- **[--project]**: project, configurable
- **[--id]**: record id, optional for action: read, mandatory for actions: update|delete
- **[--fields]**: request record fields, configurable, list form - name1,name2,... , supported for action: read
- **[--query]**: query, QC specific expression, supported for action: read
- **[--order-by]**: record ordering, dictionary form - name1:direction|name2:direction,... , direction asc|desc, supported for action: read
- **[--limit]**: record limit, supported for action: read
- **[--offset]**: record offset, supported for action: read
- **[--params]**: record params, dictionary form - name1:value,name2:value,... , supported for actions create|update
- **[--path]**: directory path, dir1/di2/... , mandatory for use cases: read/create test folder|read/create test set, create test

Configuration
^^^^^^^^^^^^^

All parameters are optional.
QC interface supports multiple entities, entity must be specified within parameter.
Entities defect|test|test-set|test-instance are configurable.

- **url**: url, used in method: connect, --url command option
- **user**: username, used in method: connect, --user command option
- **passw**: password, used in method: connect, --passw command option 
- **domain**: domain, used in method: connect, --domain command option
- **project**: project, used in method: connect, --project command option                                                                                                    
- **return_fields**: record fields returned by read operation                                 
                     use list form, name1,name2,name3                                      
- **required_fields**: required fields to create new record, user will be prompted            
                       use list form, name1,name2,name3                                     
- **default_values**: default field values to create new record                               
                      use dictionary form, name: value                                      
- **lov**: list of values for required fields, list will be offered to the user within create action               
           use dictionary form, name: value1,value2,value3

**Sample**

  .. code-block:: yaml
  
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

**API**

Defects

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
    
Tests    
     
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

**Command line**    

Defect

  .. code-block:: bash
  
     # read defect by id, return given fields, output is printed
     htk --app qc --action read --id 8594 --fields "summary,project" track
     
     # read defects by query, output is written to file
     htk --app qc --action read --query "{name[CRM*]}" --output defects.txt track
     
     # read with specified connection parameters
     # they are mandatory, if they are missing and not configured, user will be prompted
     htk --app qc --action read --url --user user --passw passw --domain dom --project proj --id 8594 track   
     
     # create defect with provided mandatory fields, id is printed
     # if some mandatory field is missing and configured, user will be prompted (including lov)
     htk --app qc --action create --params "name:hydra,description:hydra desc" track

     # create defect with description in file
     htk --app qc --action create --params "name:hydra" --input defect.txt track
     
     # update defect
     # id is mandatory, user will be prompted if missing
     htk --app --action update --id 8595 --params "status:Closed" track
     
     # delete defect
     # id is mandatory, user will be prompted if missing
     htk --app --action delete --id 8595 track
     
Test

  .. code-block:: bash
  
     # read tests under test folder (test plan), output is printed
     # path is mandatory, user will be prompted if missing
     htk --app qc --action read --type test-folder --path "Subject/.Trash/VAS" track
     
     # read test
     htk --app qc --action read --type test --id 1234 track
     
     # create test folder
     # path contains also new folder name
     htk --app qc --action create --type test-folder --path "Subject/.Trash/VAS/hydra" track
     
     # create test with provided mandatory fields
     htk --app qc --action create --type test --path "Subject/.Trash/VAS/hydra" --params "name:test,subtype-id:MANUAL" track
     
     # update test
     htk --app qc --action update --type test --id 1235 --params "name:test 2" track
     
     # read test sets under test set folder (test lab), output is written to file
     htk --app qc --action read --type test-set-folder --path "Root/.Trash/VAS" --output sets.txt track
     
     # create test set folder
     # path contains also new folder name
     htk --app qc --action create --type test-set-folder --path "Root/.Trash/VAS/hydra" track
     
     # create test set with provided mandatory fields, id is printed
     htk --app qc --action create --type test-set --qc-path "Root/.Trash/VAS/hydra" --params "name:set1,'subtype-id:hp.qc.test-set.default'" track
     
     # create test instance (assign test to test set) with provided mandatory fields
     htk --app qc --action create --type test-instance --params "cycle-id:1236,test-id:1235,test-order:1,subtype-id:hp.qc.test-instance.MANUAL" track
     
     # update test instance
     htk --app qc --action update --type test-instance --id 1237 --params "status:Closed" track

Bugzilla
========

Methods
^^^^^^^

- **connect**: connect to Bugzilla, params: url, user, passw
- **disconnect**: disconnect from Bugzilla
- **read**: read bugs, params: id, fields, query, limit, offset
- **create**: create bug, params: params
- **update** update bug, params, id: params

Command options
^^^^^^^^^^^^^^^

- **--app**: application, use bugzilla
- **--action**: actions, read|create|update
- **[--input]**: filename, content is written to bug description, supported for actions: create|update
- **[--output]**: filename, action output is written, supported for action: read
- **[--url]**: url, configurable
- **[--user]**: username, configurable
- **[--passw]**: password, configurable
- **[--id]**: record id, optional for action: read, mandatory for action: update
- **[--fields]**: request record fields, configurable, list form - name1,name2,... , supported for action: read
- **[--query]**: query, Bugzilla specific expression, supported for action: read
- **[--limit]**: record limit, supported for action: read
- **[--offset]**: record offset, supported for action: read
- **[--params]**: record params, dictionary form - name1:value,name2:value,... , supported for actions create|update

Configuration
^^^^^^^^^^^^^

Parameters are explained in QC section.
Bugzilla interface supports bug entity only, parameters are not distinguished per entity.

**Sample**

  .. code-block:: yaml
  
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

**API**

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

**Command line**  

More examples are available in QC section.

  .. code-block:: bash
  
     # read issue
     htk --app bugzilla --action read --id 40 --fields "creator,severity,summary,product" track
     
     # create issue
     htk --app bugzilla --action create --params "summary:test hydra,version:1" track
     
     # update issue
     htk --app bugzilla --action update --id 8595 --params "summary:test hydra 2" track      

Mantis
======

Methods
^^^^^^^

- **connect**: connect to Mantis, params: url, user, passw, project
- **read**: read issues, params: id, fields, page, per_page
- **create**: create issue, params: params
- **update**: update issue, params, id: params
- **delete**: delete issue, params: id 

Command options
^^^^^^^^^^^^^^^

- **--app**: application, use mantis
- **--action**: actions, read|create|update|delete
- **[--input]**: filename, content is written to issue description, supported for actions: create|update
- **[--output]**: filename, action output is written, supported for action: read
- **[--url]**: url, configurable
- **[--user]**: username, configurable
- **[--passw]**: password, configurable
- **[--project]**: project, configurable
- **[--id]**: record id, optional for action: read, mandatory for action: update|delete
- **[--fields]**: request record fields, configurable, list form - name1,name2,... , supported for action: read
- **[--page]**: record page, supported for action: read
- **[--per-page]**: records per page, supported for action: read
- **[--params]**: record params, dictionary form - name1:value,name2:value,... , supported for actions create|update

Configuration
^^^^^^^^^^^^^

Parameters are explained in QC section.
Mantis interface supports issue entity only, parameters are not distinguished per entity.

**Sample**

  .. code-block:: yaml
  
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

**API**

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

**Command line**   

More examples are available in QC section.    

  .. code-block:: bash
  
     # read issue
     htk --app mantis --action read --id 6 track
     
     # create issue
     htk --app mantis --action create --params "summary:hydra test,description:hydra desc,category:!" track
     
     # update issue
     htk --app mantis --action update --id 8595 --params "summary:hydratk" track 
     
     # delete issue
     htk --app mantis --action delete --id 8595 track    

Trac
====

Methods
^^^^^^^

- **connect**: connect to Trac, params: url, user, passw, project
- **read**: read tickets, params: id, fields, query
- **create**: create ticket, params:  params
- **update**: update ticket, params: id, params
- **delete**: delete ticket, params: id

Command options
^^^^^^^^^^^^^^^

- **--app**: application, use trac
- **--action**: actions, read|create|update|delete
- **[--input]**: filename, content is written to ticket description, supported for actions: create|update
- **[--output]**: filename, action output is written, supported for action: read
- **[--url]**: url, configurable
- **[--user]**: username, configurable
- **[--passw]**: password, configurable
- **[--project]**: project, configurable
- **[--id]**: record id, optional for action: read, mandatory for action: update|delete
- **[--fields]**: request record fields, configurable, list form - name1,name2,... , supported for action: read
- **[--query]**: query, Trac specific expression, supported for action: read
- **[--params]**: record params, dictionary form - name1:value,name2:value,... , supported for actions create|update

Configuration
^^^^^^^^^^^^^

Parameters are explained in QC section.
Trac interface supports ticket entity only, parameters are not distinguished per entity.

**Sample**

  .. code-block:: yaml
  
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

**API**

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

**Command line**  

More examples are available in QC section.

  .. code-block:: bash
  
     # read tickets
     htk --app trac --action read --query "status!=closed" track
     
     # create ticket
     htk --app trac --action create --params "summary:hydra test,description:hydra desc" track
     
     # update ticket
     htk --app trac --action update --id 8595 --params "keywords:hydratk" track
     
     # delete ticket
     htk --app trac --action delete --id 8595 track     

Jira
====

Methods
^^^^^^^

- **connect**: connect to Jira, params: url, user, passw, project
- **disconnect**: disconnect from Jira
- **read**: read issues, params: id, fields, query, limit, offset
- **create**: create issue, params: params
- **update**: update issue, params: id, params

Command options
^^^^^^^^^^^^^^^

- **--app**: application, use jira
- **--action**: actions, read|create|update
- **[--input]**: filename, content is written to issue description, supported for actions: create|update
- **[--output]**: filename, action output is written, supported for action: read
- **[--url]**: url, configurable
- **[--user]**: username, configurable
- **[--passw]**: password, configurable
- **[--project]**: project, configurable
- **[--id]**: record id, optional for action: read, mandatory for action: update|delete
- **[--fields]**: request record fields, configurable, list form - name1,name2,... , supported for action: read
- **[--query]**: query, Jira specific expression, supported for action: read
- **[--limit]**: record limit, supported for action: read
- **[--offset]**: record offset, supported for action: read
- **[--params]**: record params, dictionary form - name1:value,name2:value,... , supported for actions create|update

Configuration
^^^^^^^^^^^^^

Parameters are explained in QC section.
Jira interface supports issue entity only, parameters are not distinguished per entity.

**Sample**

  .. code-block:: yaml
  
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

**API**
  
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

**Command line**

More examples are available in QC section.

  .. code-block:: bash
  
     # read issue
     htk --app jira --action read --id 8594 --fields "id,status,creator,description" track
     
     # create issue
     htk --app jira --action create --params "summary:hydra test,description:hydra desc" track
     
     # update issue
     htk --app jira --action update --id 8595 --params "summary:test hydra 2" track

TestLink
========

Methods
^^^^^^^

- **connect**: connect to TestLink, params: url, dev_key, project
- **read**: read entities, params: method, params, fields 
- **create**: create entity, params: method, params
- **update**: update entity, params: method, params
- **read_test_suite**: read tests under test suite, params: path, steps, fields
- **create_test_suite**: create test suite, params: path, name, details
- **read_test_plsn**: read test under test plan, params: plan, plan_id, build_id, fields
- **create_test_plan**: create test plan, params: name, notes
- **create_build**: create build under plan, params: plan, name, notes
- **read_test**: read test, params: id, fields
- **create_test**: create test in test folder, params: path, params, steps
- **add_test_to_plan**: add test to plan, params: test, plan, plan_id
- **update_test_execution**: update test execution, params: test, status, notes, plan, plan_id, build_id

Command options
^^^^^^^^^^^^^^^

- **--app**: application, use testlink
- **--action**: actions, read|create|update
- **[--type]**: entity type, test-suite|test|test-plan|build
- **[--output]**: filename, action output is written, supported for action: read
- **[--url]**: url, configurable
- **[--dev-key]**: developer key, configurable
- **[--project]**: project, configurable
- **[--id]**: record id, mandatory for actions: update, read (for use cases read test|read test plan)
- **[--fields]**: request record fields, configurable, list form - name1,name2,... , supported for action: read
- **[--params]**: record params, dictionary form - name1:value,name2:value,... , supported for actions create|update
- **[--path]**: directory path, dir1/di2/... , mandatory for use cases: read/create test suite|create test
- **[--steps]**: test steps, steps delimited by |, step in dictionary form - name1:value,name2:value,...|name1:value,name2:value,... , supported for use case create test

Configuration
^^^^^^^^^^^^^

All parameters are optional.

- **url**: url, used in method: connect, --url command option
- **dev_key**: developer key, used in method: connect, --dev-key command option
- **project**: project, used in method: connect, --project command option                                                                                                    
- **return_fields**: test fields returned by read operation                                 
                     use list form, name1,name2,name3                                       
- **required_fields**: required test fields to create new record, user will be prompted            
                       use list form, name1,name2,name3                                      
- **default_values**: default test field values to create new record                               
                      use dictionary form, name: value                                       
- **lov**: list of values for required test fields, list will be offered to the user within create action               
           use dictionary form, name: value1,value2,value3

**Sample**

  .. code-block:: yaml
  
     testlink:
     url: url     
     dev_key: 3db69a303c75cdaa08c98b12d5f9f2aa
     project: hydra
     return_fields:
       test: casename,author_login,summary,id,full_tc_external_id,steps,tcase_id,tcase_name,exec_status,actions,expected_results
     required_fields:
       testcasename,authorlogin,summary
     default_values:
       authorlogin: admin
     lov:  
       exec_status: p,f
     
Examples
^^^^^^^^

**API**

  .. code-block:: python  
  
     # import client
     from hydratk.extensions.trackapps.testlink import Client
     c = Client()
     
     # connect
     res = c.connect(url, dev_key, project)
     
     # read test
     id = 3
     res, test = c.read_test(id) 
     
     # read test suite
     path = 'suite 1/suite 3'
     res, tests = c.read_test_suite(path)             
     
     # create test suite
     id = c.create_test_suite('suite 1/suite 3', 'suite 4', 'xxx')
     
     # create test
     params = {'testcasename': 'case 3', 'authorlogin': 'lynus', 'summary': 'hydratk'}
     steps = [{'actions': 'DO', 'expected_results': 'OK'}]
     test_id = c.create_test('suite 1/suite 3', params, steps)     
     
     # create test plan and build
     plan_id = c.create_test_plan('plan 1')
     build_id = c.create_build(plan_id, 'build 1')
     
     # add test to test plan
     res = c.add_test_to_plan(test_id, 'plan 1')
     
     # update test execution
     res = c.update_test_execution(test_id, status='p', plan='plan 1')   
     
     # read test plan
     res, tests = c.read_test_plan('plan 1') 

**Command line**    

  .. code-block:: bash
  
     # read tests under test folder (test plan), output is printed
     # path is mandatory, user will be prompted if missing
     htk --app testlink --action read --type test-suite --path "suite 1/suite 3" track
     
     # read test
     # id is mandatory
     htk --app testlink --action read --type test --id 3 track
     
     # create test suite
     # path contains also new suite name
     htk --app testlink --action create --type test-suite --path "suite 1/suite 3" track
     
     # create test with provided mandatory fields
     htk --app testlink --action create --type test --path "suite 1/suite 3" --params "testcasename:case3,authorlogin:admin,summary:test" track
     
     # create test with steps
     htk --app testlink --action create --type test --path "suite 1/suite 3" --params "testcasename:case3,authorlogin:admin,summary:test" 
         --steps "actions:act1,expected_results:res1|actions:act2,expected_results:res2" track
     
     # read tests under test plan, output is written to file
     htk --app testlink --action read --type test-plan --id 166 --output tests.txt track
     
     # create test plan
     htk --app testlink --action create --type test-plan --params "name:plan 1" track
     
     # create build
     htk --app testlink --action create --type build --params "plan:2,name:build 1" track
     
     # add test to plan
     htk --app testlink --action update --type test-plan --id 166 --params "test:3" track
     
     # update test execution
     htk --app testlink --action update --type test --id 3 --params "plan:167,status:f" track  