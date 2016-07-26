.. _tutor_trackapps_tut6_testlink:

Tutorial 6: TestLink
====================

TestLink interface supports operations with test entities (test, suite, plan, build). 
You can read, create and update them.

Command line
^^^^^^^^^^^^

It is controlled via command track with following options.

Mandatory:

* --tr-app <name>: application, use testlink
* --tr-action <name>: action, read|create|update

Optional:

* --tr-type <name>: entity type, test-suite|test|test-plan|build
* --tr-output <path>: filename, action output is written, supported for action: read
* --tr-url <string>: url, configurable
* --tr-dev-key <string>: developer key, configurable
* --tr-project <string>: project, configurable
* --tr-id <num>: record id, mandatory for actions: update, read (for use cases read test|read test plan)
* --tr-fields <list>: request record fields, configurable, list form - name1,name2, supported for action: read
* --tr-params <dict>: record params, dictionary form - name1:value,name2:value, supported for actions create|update
* --tr-path <string>: directory path, dir1/di2 , mandatory for use cases: read/create test suite|create test
* --tr-steps <dict>: test steps, steps delimited by pipe, step in dictionary form - name1:value,name2:value|name1:value,name2:value, supported for use case create test

Configuration
^^^^^^^^^^^^^

Use section testlink in configuration file.

* url: TestLink server url, used as --tr-url option
* dev_key: develope key, used as --tr-dev-key option
* project: project, used as --tr-project option                                                                                                  
* return_fields: record fields returned within read (all by default), used as --tr-fields option, use list form, name1,name2,name3                                      
* required_fields: required fields to create new record, user will be asked if not provided in --tr-params option, use list form, name1,name2,name3                                     
* default_values: default field values to create new record, used both for required and optional fields, use dictionary form, name: value                                      
* lov: list of values for required fields, list will be offered to user within create, use dictionary form, name: value1,value2,value3

TestLink supports multiple test entities, but configuration parameters (return_fields, required_fields, default_values, lov) are used 
for entity test only. 
Parameters for remaining entities must be provided by option --tr-params.

  .. code-block:: yaml
  
     TrackApps:
       testlink:
       url: url     
       dev_key: 3db69a303c75cdaa08c98b12d5f9f2aa
       project: hydra
       return_fields:
         casename,author_login,summary,id,full_tc_external_id,steps,tcase_id,tcase_name,exec_status,actions,expected_results
       required_fields:
         testcasename,authorlogin,summary
       default_values:
         authorlogin: admin
       lov:  
         exec_status: p,f
         
Examples
^^^^^^^^ 

Some parameters are configured to make command examples shorter.

  .. code-block:: bash
  
     # read test suite
     # type=test-suite
     # path is provided, user will be prompted if missing
     # returns tests under test suite, output is printed
     $ htk --tr-app testlink --tr-action read --tr-type test-suite --tr-path "suite 1/suite 3" track
     
     # read test
     # id=3, type=test
     $ htk --tr-app testlink --tr-action read --tr-type test --tr-id 3 track
     
     # create test suite
     # type=test-suite
     # path contains also new suite name (suite 1 is existing folder, suite 3 is new folder)
     $ htk --tr-app testlink --tr-action create --tr-type test-suite --tr-path "suite 1/suite 3" track
     
     Record 165 created
     
     # create test
     # entity=test
     # path is provided
     # required fields are provided or have configured default values
     $ htk --tr-app testlink --tr-action create --tr-type test --tr-path "suite 1/suite 3" --tr-params "testcasename:case3,authorlogin:admin,summary:test" track
     
     Record 3 created
     
     # create test with steps
     # entity=test
     # path is provided
     # required fields are provided or have configured default values     
     $ htk --tr-app testlink --tr-action create --tr-type test --tr-path "suite 1/suite 3" --tr-params "testcasename:case3,authorlogin:admin,summary:test" 
           --tr-steps "actions:act1,expected_results:res1|actions:act2,expected_results:res2" track
     
     Record 4 created
     
     # read test plan
     # id=166, type=test-plan
     # returns tests under test plan, output is written to text file
     $ htk --tr-app testlink --tr-action read --tr-type test-plan --tr-id 166 --tr-output tests.txt track
     
     # create test plan
     # type=test-plan
     # required fields are provided
     $ htk --tr-app testlink --tr-action create --tr-type test-plan --tr-params "name:plan 1" track
     
     Record 166 created
     
     # create build
     # type=build
     # required fields are provided
     $ htk --tr-app testlink --tr-action create --tr-type build --tr-params "plan:2,name:build 1" track
     
     Record 168 created
     
     # add test to plan
     # add test 3 to test plan 166, type=test-plan
     $ htk --tr-app testlink --tr-action update --tr-type test-plan --tr-id 166 --tr-params "test:3" track
     
     Record 166 updated
     
     # update test execution
     # id=3, type=test, add test to test plan 167, status false
     $ htk --tr-app testlink --tr-action update --tr-type test --tr-id 3 --tr-params "plan:167,status:f" track
     
     Record 3 updated   
     
     .. note::
     
        Use option --tr-type carefully    
        
API
^^^

This section shows several examples how to use TestLink interface as API in your extensions/libraries.
API uses HydraTK core functionalities so it must be running.

Methods

* connect: connect to TestLink, params: url, dev_key, project
* read_test_suite: read tests under test suite, params: path, steps, fields
* create_test_suite: create test suite, params: path, name, details
* read_test_plsn: read test under test plan, params: plan, plan_id, build_id, fields
* create_test_plan: create test plan, params: name, notes
* create_build: create build under plan, params: plan, name, notes
* read_test: read test, params: id, fields
* create_test: create test in test folder, params: path, params, steps
* add_test_to_plan: add test to plan, params: test, plan, plan_id
* update_test_execution: update test execution, params: test, status, notes, plan, plan_id, build_id

Examples           

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