.. _tutor_network_tut12_term:

Tutorial 12: Terminal
=====================

This sections shows several examples how to use terminal client.

API
^^^

Module hydratk.lib.network.term.client
Method TermClient is factory method which requires attribute engine to create 
proper TermClient object instance. Additional attributes are passed as args, kwargs.

Supported protocols:

* SSH: module ssh_client

Methods:

* connect: connect to server
* disconnect: disconnect from server
* exec_command: execute command on server

  .. note::
   
     API uses HydraTK core functionalities so it must be running.

SSH
^^^

  .. code-block:: python
  
     # import library
     import hydratk.lib.network.term.client as term
    
     # initialize client
     client = term.TermClient()
     
     # connect to SSH server
     # returns bool
     client.connect(host='lxocrmgf401vm.cz', user='aaa', passw='bbb')   
     
     # execute commands
     # returns bool, stdout lines or stderr lines
     
     # print working directory
     print client.exec_command('pwd')
     
     # make directory
     client.exec_command('mkdir pokus')
     
     # create file
     client.exec_command('touch evil')
     
     # delete file in interactive mode
     # Y is sent to stdin
     client.exec_command('rm -i evil', 'Y')
     
     # execute script
     client.exec_command('./pok.sh')
     
     # disconnect from server
     # returns bool
     client.disconnect() 