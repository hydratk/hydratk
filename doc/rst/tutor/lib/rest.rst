.. REST

====
REST
====

Library hydratk.lib.network.rest.client provides rest client.

**Supported protocols**:

- HTTP

**Methods**:

- **send_request** - send request to server
- **get_header** - get response header
- **get_body** - get response body

Examples
========

See following examples for HTTP, HTTPS protocols.

  .. code-block:: python
  
     # import library
     import hydratk.lib.network.rest.client as rest
    
     # initialize client
     client = rest.RESTClient()
     
     # send HTTP GET request 
     # returns status 200 and HTML body
     status, body = client.send_request('google.com')
     
     # send HTTP GET request with URL param
     status, body = client.send_request('http://metalopolis.net/art_downtown.asp', 
                                         params={'id2': '7871'})  
                  
     # send HTTP POST request to submit form                       
     status, body = client.send_request('http://metalopolis.net/fastsearch.asp', method='POST', 
                                         params={'verb': 'motorhead', 'submit': '>>>'}) 
      
     # send HTTPS GET request with authentication                                    
     status, body = client.send_request('https://trac.hydratk.org/hydratk/login', 
                                         user='aaa', passw='bbb')  
                                         
     # send HTTP POST request with JSON body 
     data = r'{"userId": 1, "id": 101, "title": "bowman", "body": "bowman"}'
     status, body = client.send_request('http://jsonplaceholder.typicode.com/posts', method='POST', body=data,
                                         content_type='json')     
                                         
     # send HTTP GET request to receive JSON body
     status, body = client.send_request('http://jsonplaceholder.typicode.com/posts/100', method='GET') 
     
     # send HTTP GET request to receive XML body
     status, body = client.send_request('http://httpbin.org/xml', method='GET')                                     