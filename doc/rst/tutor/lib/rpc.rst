.. RPC

===
RPC
===

Library hydratk.lib.network.dbi.client provides rpc client.
Method RPCClient is factory method which requires attribute engine to create 
proper RPCClient object instance. Additional attributes are passed as args, kwargs. 

**Supported providers**:

- RMI - module rmi_client

**Methods**:

- **init_proxy**: - initialize proxy to remote object
- **call_method**: - call method on remote object
- **close** - stop JVM

Examples
========

  .. code-block:: python
  
     # import library
     from hydratk.lib.network.rpc.client import RPCClient
     
     # initialize client
     client = RPCClient('rmi')
     
     # initialize proxy
     client.init_proxy('rmi://localhost:2004/server') 
     
     # call remote method
     client.call_method('callRemote', 'xxx')
     
     # stop JVM
     client.close()      