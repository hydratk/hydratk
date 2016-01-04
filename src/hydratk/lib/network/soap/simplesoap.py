# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit library

.. module:: network.soap.simplesoap
   :platform: Unix
   :synopsis: Pycurl wrapped object oriented soap client solution
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
import pycurl
import pytz
import datetime


from hydratk.lib.data.xml import XMLValidate
from hydratk.lib.system import fs
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

curl_info_map  = {
                       'effective_url'           : 'EFFECTIVE_URL',
                       'response_code'           : 'RESPONSE_CODE',
                       'http_connectcode'        : 'HTTP_CONNECTCODE',
                       'filetime'                : 'INFO_FILETIME',
                       'total_time'              : 'TOTAL_TIME',
                       'namelookup_time'         : 'NAMELOOKUP_TIME',
                       'connect_time'            : 'CONNECT_TIME',
                       'appconnect_time'         : 'APPCONNECT_TIME',              
                       'pretransfer_time'        : 'PRETRANSFER_TIME',
                       'starttransfer_time'      : 'STARTTRANSFER_TIME',
                       'redirect_time'           : 'REDIRECT_TIME',
                       'redirect_count'          : 'REDIRECT_COUNT',
                       'redirect_url'            : 'REDIRECT_URL',
                       'size_upload'             : 'SIZE_UPLOAD',
                       'size_download'           : 'SIZE_DOWNLOAD',
                       'speed_download'          : 'SPEED_DOWNLOAD',
                       'speed_upload'            : 'SPEED_UPLOAD',
                       'header_size'             : 'HEADER_SIZE',
                       'request_size'            : 'REQUEST_SIZE',
                       'ssl_verify_result'       : 'SSL_VERIFY_RESULT',
                       'ssl_engines'             : 'SSL_ENGINES',
                       'content_length_download' : 'CONTENT_LENGTH_DOWNLOAD',
                       'content_length_upload'   : 'CONTENT_LENGTH_UPLOAD',
                       'content_type'            : 'CONTENT_TYPE',
                       'private'                 : 'PRIVATE',
                       'httpauth_avail'          : 'HTTPAUTH_AVAIL',
                       'proxyauth_avail'         : 'PROXYAUTH_AVAIL',
                       'os_errno'                : 'OS_ERRNO',
                       'num_connects'            : 'NUM_CONNECTS',
                       'primary_ip'              : 'PRIMARY_IP',
                       'primary_port'            : 'PRIMARY_PORT',
                       'local_ip'                : 'LOCAL_IP',
                       'local_port'              : 'LOCAL_PORT',                       
                       'lastsocket'              : 'LASTSOCKET',
                       'activesocket'            : 'ACTIVESOCKET',                       
                       'tls_session'             : 'TLS_SESSION',                                                   
}

HTTP_AUTH_BASIC = pycurl.HTTPAUTH

class SoapResponse(object):
    _msg          = None
    _resp_headers = []
    _resp_code    = 0    
    _info         = {}
    
    @property
    def response_code(self):
        return self._resp_code
    
    @property
    def info(self):
        return self._info
    
    @property
    def headers(self):
        return self._resp_headers
        
    
    @property
    def msg(self):
        return self._msg   
                     
    @property
    def message(self):
        return self._msg
 
    def _extract_info(self, curl_obj):
        for info_key, curl_opt in curl_info_map.items():                                                
            if hasattr(curl_obj, curl_opt): 
                curl_val = curl_obj.getinfo(getattr(curl_obj, curl_opt))
                self._info[info_key] = curl_val
           
    def _apply_info(self):
        self._resp_code = self._info['response_code']
                    
    def __init__(self, curl_obj):
        self._extract_info(curl_obj)
        self._apply_info()
        
        
class SoapRequest(object):
    _msg         = None
    _req_url     = None
    _req_method  = pycurl.POST
    _req_headers = [
                     "Content-type: text/xml; charset=utf-8"
                   ]
    
    
    def __init__(self, request_url = None):
        self._req_url = request_url      
    
    @property
    def url(self):
        return self._req_url
    
    @url.setter
    def url(self, url):
        self._req_url = url
            
    @property
    def headers(self):
        return self._req_headers
    
    @headers.setter
    def headers(self, header):
        self._req_headers = header
    
    @property
    def msg(self):
        return self._msg
    
    @msg.setter
    def msg(self, msg):
        self._msg = msg   
                     
    @property
    def message(self):
        return self._msg
    
    @message.setter
    def message(self, msg):
        self._msg = msg
         

class SoapResponseMessage(object):
    _content = None
    
    def __init__(self, content=None):
        if content is not None:
            self._content = content
            
    @property
    def content(self):
        return self._content
    
    @content.setter
    def content(self, content):
        self._content = content


class SoapRequestMessage(XMLValidate):
    _bind_lchr = '['
    _bind_rchr = ']'
    _content   = None
    
    def __init__(self, content=None, source='file'):
        if content is not None:
            if source == 'file':
                self.load_from_file(content)
            if source == 'str':
                self._content = content  
                
    @property
    def content(self):        
        return self._content
    
    @content.setter
    def content(self, content):
        self._content = content
    
    def load_from_file(self,msg_file):
        self._content = fs.file_get_contents(msg_file)             
        
    def bind_var(self,*args,**kwargs):
        if self._content is not None:
            content = str(self._content)
            for bdata in args:
                for var,value in bdata.items():
                    bind_var = '{bind_lchr}{var}{bind_rchr}'.format(bind_lchr=self._bind_lchr,var=var,bind_rchr=self._bind_rchr)                
                    content = content.replace(str(bind_var), str(value))
            for var, value in kwargs.items():
                bind_var = '{bind_lchr}{var}{bind_rchr}'.format(bind_lchr=self._bind_lchr,var=var,bind_rchr=self._bind_rchr)                
                content = content.replace(str(bind_var), str(value))                
            self._content = content       
    
    
    def xsd_validate(self):
        import lxml        
        result = True
        msg    = None
        try:
            XMLValidate.xsd_validate(self, self._content)
        except lxml.etree.DocumentInvalid as e:
            msg    = e
            result = False
            
        return (result, msg)
           
class SoapClient():
    
    _connection_timeout = 30
    _request            = None    
    _response           = None
    _curl               = None

    @property
    def request(self):
        return self._request
    
    @request.setter
    def request(self, req):
        self._request = req
    
    @property
    def response(self):
        return self._response    
             
    def __init__(self):
        self._curl = pycurl.Curl()
    
    def set_auth(self, username, password, auth_type = HTTP_AUTH_BASIC):
        self._curl.setopt(self._curl.HTTPAUTH, auth_type)
        if auth_type == HTTP_AUTH_BASIC:
            self._curl.setopt(self._curl.USERPWD, "{username}:{password}".format(username=username,password=password))                   
    
    def send(self, timeout = _connection_timeout):        
        
        buff = BytesIO()                
        self._curl.setopt(self._curl.URL, self.request.url)
        self._curl.setopt(self._curl.HTTPHEADER, self.request.headers)
        self._curl.setopt(self._curl.POSTFIELDS, str(self.request.msg.content))
        self._curl.setopt(self._curl.WRITEDATA, buff)
        
        self._curl.perform()        
        self._response = SoapResponse(self._curl)
        self._response.msg = SoapResponseMessage(buff.getvalue())
        self._curl.close()

         
def xml_timestamp(location = 'Europe/Prague'):
    return datetime.datetime.now(pytz.timezone(location)).isoformat()