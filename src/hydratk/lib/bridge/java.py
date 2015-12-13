# -*- coding: utf-8 -*-
"""This code is part of Hydra Toolkit library

.. module:: bridge.java
   :platform: Unix
   :synopsis: Bridge to Java virtual machine
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

"""
Events:
-------
java_before_start
java_after_start
java_before_stop
java_after_stop

"""

from hydratk.core.masterhead import MasterHead
from hydratk.core import event
import jpype
import os

java_types = {
  'byte'  : jpype.JByte,
  'short' : jpype.JShort,
  'int'   : jpype.JInt,
  'long'  : jpype.JLong,
  'float' : jpype.JFloat,
  'double': jpype.JDouble,
  'char'  : jpype.JChar,
  'string': jpype.JString,
  'bool'  : jpype.JBoolean
}

class JavaBridge:

    _mh = None
    _jvm_path = None
    _classpath = None
    _status = None
    
    def __init__(self, jvm_path=None, classpath=None):
        """Class constructor
           
        Called when the object is initialized
        
        Args:                   
           jvm_path (str): JVM location, default from configuration
           classpath (str): Java classpath, default from configuration
           
        """         
        
        self._mh = MasterHead.get_head()        
        
        if (jvm_path != None):
            self._jvm_path = jvm_path
        else: 
            cfg = self._mh.cfg['Libraries']['hydratk.lib.bridge.java']['jvm_path']
            self._jvm_path = cfg if (cfg != 'default') else jpype.get_default_jvm_path()
             
        self._classpath = self._set_classpath(classpath)   
        
    @property
    def jvm_path(self):
        
        return self._jvm_path
    
    @property
    def classpath(self):
        
        return self._classpath
    
    @property
    def status(self):
        
        return self._status                                                        
        
    def start(self, options=[]):
        """Method starts JVM 
        
        Args:
           options (list): JVM options

        Returns:
           bool: result
                
        """          
        
        try:
            
            if (self._status):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_java_already_started'), self._mh.fromhere())
                return False
            elif (jpype.isJVMStarted()):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_java_restart_tried'), self._mh.fromhere())
                return False
                                                      
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_java_starting_jvm', self._jvm_path,
                          self.classpath, options), self._mh.fromhere())
                
            ev = event.Event('java_before_start', options)
            if (self._mh.fire_event(ev) > 0):
                options = ev.argv[0]                
                
            if (ev.will_run_default()):                  
                if (self._classpath != None):
                    options.append('-Djava.class.path={0}'.format(self._classpath))
                
                jpype.startJVM(self._jvm_path, *options)
                    
                self._status = True
                result = True
                
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_java_started'), self._mh.fromhere()) 
            ev = event.Event('java_after_start')
            self._mh.fire_event(ev)                  
                
            return result
            
        except (RuntimeError, jpype.JavaException), ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return None         
    
    def stop(self):
        """Method stops JVM
            
        Returns:
           bool: result
                
        """          
        
        try:
            
            if (not self._status):
                self._mh.dmsg('htk_on_warning', self._mh._trn.msg('htk_java_not_started'), self._mh.fromhere())
                return False                
            
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_java_stopping_jvm'), self._mh.fromhere())
            ev = event.Event('java_before_stop')
            self._mh.fire_event(ev)
                        
            jpype.shutdownJVM()
            self._status = False
            result = True
                
            self._mh.dmsg('htk_on_debug_info', self._mh._trn.msg('htk_java_stopped'), self._mh.fromhere()) 
            ev = event.Event('java_after_stop')
            self._mh.fire_event(ev)                
                
            return result
          
        except (RuntimeError, jpype.JavaException), ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return None         
    
    def get_var(self, datatype, value):
        """Method creates Java variable
        
        Args:
           datatype (str): byte|short|int|long|float|double|char|string|bool
           value (str): initial value
            
        Returns:
           obj: Java variable
                
        """          
        
        try:
        
            if (not java_types.has_key(datatype)):
                self._mh.dmsg('htk_on_error', self._mh._trn.msg('htk_java_unknown_type', datatype), self._mh.fromhere())
                return None        
            else: 
                return java_types[datatype](value)
            
        except (RuntimeError, jpype.JavaException), ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return None            
        
    def get_class(self, name, *attrs):
        """Method creates Java class instance
        
        Args:
           name (str): class name
           attrs (args): constructor attributes
            
        Returns:
           obj: class instance
                
        """          
        
        try:

            return jpype.JClass(name)(*attrs)
        
        except (RuntimeError, jpype.JavaException), ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return None
        
    def desc_class(self, name):
        """Method describes Java class
        
        Args:
           name (str): class name
            
        Returns:
           tuple: attribute names, method names
                
        """         
        
        try:
            
            attrs = []
            methods = []
            
            for name, type in jpype.JClass(name).__dict__.items():
                if (type.__class__.__name__ == 'property'):
                    attrs.append(name)
                elif (type.__class__.__name__ == 'JavaMethod'):
                    methods.append(name)
            
            return attrs, methods
        
        except (RuntimeError, jpype.JavaException), ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return None     
        
    def init_hashmap(self, dictionary):
        """Method initializes Java hashmap
        
        Args:
           dictionary (dict): Python dictionary
            
        Returns:
           obj: Java hashmap
                
        """          
        
        try:
            
            hashmap = self.get_class('java.util.concurrent.ConcurrentHashMap')
            for key, value in dictionary.items():
                hashmap.put(str(key), str(value))   
                
            return hashmap 
        
        except (RuntimeError, jpype.JavaException), ex:
            self._mh.dmsg('htk_on_error', ex, self._mh.fromhere())
            return None   
        
    def _set_classpath(self, classpath=None):
        """Method sends command connect  
        
        Args:
           connection_factory: JMS connection factory
           properties (dict): JMS connection properties 

        Returns:
           bool: result
                
        """          
        
        cfg = self._mh.cfg['Libraries']['hydratk.lib.bridge.java']['classpath']
        if (classpath != None):
            cfg += ':' + classpath
          
        exp_classpath = ''             
        for entry in cfg.split(':'):
            
            if (os.path.isfile(entry)):
                exp_classpath += entry + ':'
            else:
                                
                for dirname, _, filelist in os.walk(entry):   
                    exp_classpath += dirname + ':'    
                    for filename in filelist:
                        if (filename.split('.')[1] == 'jar'):
                            exp_classpath += os.path.join(dirname, filename) + ':'
                            
        return exp_classpath[:-1]                                         