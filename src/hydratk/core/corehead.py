# -*- coding: utf-8 -*-
"""HydraTK core module

.. module:: core.corehead
   :platform: Unix
   :synopsis: HydraTK core module
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import os
import sys
import signal
import yaml
import multiprocessing
import importlib
import imp
import traceback
import pprint
import setproctitle
import time
import zmq
import threading
from os import makedirs

PYTHON_MAJOR_VERSION = sys.version_info[0]

if PYTHON_MAJOR_VERSION == 2:
    import ConfigParser as configparser    
    
if PYTHON_MAJOR_VERSION == 3:    
    import configparser     
  
from hydratk.core import const
from hydratk.core import hsignal
from hydratk.lib.console import cmdoptparser
from hydratk.core import commandopt
from hydratk.core import message
from hydratk.core.eventhandler import EventHandler
from hydratk.core import event
from hydratk.core.debugger import Debugger
from hydratk.core.logger import Logger
from hydratk.core.messagehead import MessageHead
from hydratk.core import messagerouter
from hydratk.lib.profiling.profiler import Profiler
from hydratk.lib.console.commandlinetool import CommandlineTool
from hydratk.lib.exceptions.inputerror import InputError
import hydratk.core.dbconfig as dbconfig
from hydratk.lib.translation import translator

class AsyncCallBackHandler(object):
    """Class AsyncCallBackHandler        
    """
        
    _hc = None
    
    def __init__(self, hc):
        self._hc = hc
             
    def cb_run(self, cb_obj):
        print("async: running request {0}".format(cb_obj.fn_id), cb_obj.args, cb_obj.kwargs)
        msg = {
       'type' : "async_fn_ex",
       'from' : 'htk_obsrv@core.raptor',
       'to'   : 'any@core.raptor',
       'data' : {
                 'fn_id'  : cb_obj.fn_id,
                 'args'   : cb_obj.args,
                 'kwargs' : cb_obj.kwargs
                }
        
        }
        self._hc.send_msg(msg)
    
    def cb_completed(self, req_id):
        pass           

    
class CoreHead(MessageHead, EventHandler, Debugger, Profiler, Logger):
    """Class CoreHead 
       
       Inherited from MessageHead, EventHandler, Debugger, Profiler, Logger        
    """
    
    _runlevel         = const.RUNLEVEL_SHUTDOWN
    _config           = None   
    _language         = const.DEFAULT_LANGUAGE 
    _config_file      = const.CONFIG_FILE
    _ext_confd        = const.EXT_CONFIG_DIR
    _use_extensions   = True
    '''Extensions'''
    _ext              = {} 
    _default_command  = 'short-help'
    _help_title       = '{h}' + const.APP_NAME + ' v' + const.APP_VERSION + '{e}'
    _cp_string        = '{u}' + const.CP_STRING + '{e}'   
    _command          = None
    _opt_profile      = 'htk'     
    _cmd_option_hooks = {}
    _event_hooks      = {}
    _cmd_hooks        = {}
    _fn_hooks         = {} 
    _msg_router_id    = 'raptor01'    
    _msg_router       = None  
    _app_status       = None
    _observer_status  = None
    '''Core thread pool'''
    _thr              = [] 
    '''Translator instance'''
    _trn              = None 
    _pid_file         = None
    _option           = {}
    _option_param     = {}

    '''Application services pool'''    
    _app_service      = []
    _run_mode         = const.CORE_RUN_MODE_SINGLE_APP
    
    '''Function callbacks'''
    _fn_cb            = {}
    
    '''Parallel processing'''
    _fn_cb            = {}
    _fn_cb_shared     = {}
    _async_fn_tickets = {}
    _cbm              = None  #Callback manager   
    _async_fn         = {}
    _async_fn_ex      = None
    

    def _bootstrap(self):
        """Method executes specific processing according to runlevel
        
        Callback for functionality h_bootstrap
        
        Args:    
           none        
           
        Returns:
           bool: True       
                
        """  
            
        if self._runlevel == const.RUNLEVEL_SHUTDOWN:
            self.run_fn_hook('h_runlevel_baseinit')                        
        if self._runlevel == const.RUNLEVEL_BASEINIT:
            self.run_fn_hook('h_runlevel_config')            
        if self._runlevel == const.RUNLEVEL_CONFIG:
            self.run_fn_hook('h_runlevel_extensions')
        if self._runlevel == const.RUNLEVEL_EXTENSIONS:
            self.run_fn_hook('h_runlevel_cli')
        if self._runlevel == const.RUNLEVEL_CLI:
            self.run_fn_hook('h_runlevel_core')
        if self._runlevel == const.RUNLEVEL_CORE:
            self.run_fn_hook('h_runlevel_appl')            
        else:
            pass #already running
        
        return True #required by fn_hook
        
    def _create_config_db(self):
        """Method creates configuration database
        
        Callback for command create-config-db
        Database filename is taken from option --config-db-file (prio 1), configuration System/DBConfig/db_file (prio 2)
         
        If database exists it can be recreated using option -f|--force, otherwise is kept   
        
        Args:            
           none
           
        Returns:
           bool: result       
                
        """          
        
        result = False
        force_cmd = True if CommandlineTool.get_input_option('force') == True else False
        db_file_param = CommandlineTool.get_input_option('config-db-file')
        cfg_db_file = self._config['System']['DBConfig']['db_file']
        if db_file_param not in (True,False) or cfg_db_file != '':
            create_db_file = db_file_param if db_file_param not in (True,False) else cfg_db_file
            dir_name = os.path.dirname(create_db_file)   
            if os.access(dir_name, os.W_OK):
                if os.path.isfile(create_db_file) == False: 
                    self.dmsg('htk_on_debug_info', self._trn.msg('htk_create_cfg_db', create_db_file), self.fromhere())
                    self._write_config_db(create_db_file)
                    result = True
                else:
                    if force_cmd == True:
                        self.dmsg('htk_on_debug_info', self._trn.msg('htk_remove_cfg_db'), self.fromhere())
                        os.remove(create_db_file)
                        self._write_config_db(create_db_file)
                        result = True
                    else:
                        self.dmsg('htk_on_debug_info', self._trn.msg('htk_cfg_db_exists'), self.fromhere())   
            else:
                self.dmsg('htk_on_error', self._trn.msg('htk_create_cfg_db_error', create_db_file), self.fromhere())
                print(os.access(create_db_file, os.W_OK))
        
        else:
            self.dmsg('htk_on_error', self._trn.msg('htk_cfg_db_not_spec'), self.fromhere())
        
        return result    
    
    def _get_asyn_req_ticket(self):
        pass
    
    def _c_observer(self):
        """Method creates observer process and watches it during its lifecycle
        
        When it is not active, application is stopped
        
        Configuration options:
        Core/MessageService/id 
        Core/MessageService/transport_type
        Core/MessageService/address
        Core/Service/pid_file  
        
        Args:
           none        
           
        Returns:
           void  
            
        Raises:
           event: htk_before_cw_activity_check    
           event: htk_on_cobserver_ctx_switch
                
        """           
        
        setproctitle.setproctitle('hydratk/c_observer') # mark process to be identified in list of processes
        
        # get message service id from configuration, otherwise stop application
        try:
            core_msg_service_id = self._config['Core']['MessageService']['id']
            if (core_msg_service_id != ''):
                self._core_msg_service_id = core_msg_service_id
            else:                    
                raise ValueError
        except configparser.NoOptionError:
            self.dmsg('htk_on_error', self._trn.msg('htk_conf_opt_missing', 'Core.MessageService', 'id'), self.fromhere())
            self._stop_app(True)            
        except ValueError as desc:
            self.dmsg('htk_on_error', self._trn.msg('htk_conf_opt_val_err', 'Core.MessageService', 'id', desc), self.fromhere())
            self._stop_app(True)                         
                
        try:
            # get message queue transport type and address from configuration, otherwise stop application
            cmsgq_transport_type = int(self._config['Core']['MessageService']['transport_type'])            
            if (cmsgq_transport_type != ''):
                options = {}
                if cmsgq_transport_type in(messagerouter.SERVICE_TRANSPORT_TYPE_ZMQ_IPC, messagerouter.SERVICE_TRANSPORT_TYPE_ZMQ_TCP):
                    cmsgq_address = self._config['Core']['MessageService']['address'] 
                    options = {                                                      
                           'address' : cmsgq_address                  
                    }
                try:
                    # register message service to queue
                    self._msg_router.register_service(self._core_msg_service_id, cmsgq_transport_type, options)
                    self.dmsg('htk_on_debug_info', self._trn.msg('htk_core_msg_service_add_ok', core_msg_service_id), self.fromhere())
                    self._observer_status = const.CORE_THREAD_WORK
                    current = multiprocessing.current_process()
                    current.status = const.CORE_THREAD_WORK
                   
                    # initialize process as message queue sender
                    try:
                        #current.msgq   = self._msg_router.get_queue(self._core_msg_service_id, messagerouter.MESSAGE_QUEUE_ACTION_BIND, {'socket_type' : zmq.PULL} )
                        #self.dmsg('htk_on_debug_info', "Message queue {0} : socket type zmq.PULL connected".format(self._core_msg_service_id), self.fromhere())
                        
                        #current.msgq = self._msg_router.get_queue(self._core_msg_service_id, messagerouter.MESSAGE_QUEUE_ACTION_CONNECT, {'socket_type' : zmq.PUSH} )
                        #self.dmsg('htk_on_debug_info', "Message queue {0} : socket type zmq.PUSH connected {1}".format(self._core_msg_service_id, type(current.msgq).__name__), self.fromhere())
                        context = zmq.Context()
                        sender = context.socket(zmq.PUSH)
                        #TODO workaround, will be changed in next version, by implementing new a message router
                        if not os.path.exists("/tmp/hydratk"):
                            makedirs("/tmp/hydratk")
                        sender.bind("ipc:///tmp/hydratk/core.socket")
                        current.msgq = sender
                                                     
                        self.dmsg('htk_on_debug_info', self._trn.msg('htk_core_msgq_init_ok', self._msg_router.get_service_address(self._core_msg_service_id)), self.fromhere())
                    except zmq.ZMQBindError as desc:
                        ex_type, ex, tb = sys.exc_info()
                        print(ex_type)
                        print(ex)
                        traceback.print_tb(tb)
                    ''' TODO process exceptions '''
                    
                    self.dmsg('htk_on_debug_info', self._trn.msg('htk_observer_init'), self.fromhere())
                    
                    # create PID file, get filename from configuration, otherwise stop application
                    try:
                        pid_file = self._config['Core']['Service']['pid_file']            
                        if (pid_file != ''):
                            core_pid = self._set_pid_file(pid_file)                            
                            self._pid_file = pid_file if core_pid > 0 else None
                            if self._pid_file == None:
                                self._stop_app(True)
                        else: raise ValueError                                                
                        self.dmsg('htk_on_debug_info', self._trn.msg('htk_pid_file_set', core_pid, pid_file), self.fromhere())                
                    except configparser.NoOptionError:                        
                        self.dmsg('htk_on_error', self._trn.msg('htk_conf_opt_missing', 'Core', 'pid_file'), self.fromhere())
                        self._stop_app(True)
                    except ValueError as desc:
                        self.dmsg('htk_on_error', self._trn.msg('htk_conf_opt_val_err', 'Core', 'pid_file', desc), self.fromhere())
                        self._stop_app(True) 
                        
                    # initialize worker threads                      
                    self.init_core_threads()
                    self._reg_self_signal_hooks()
                    
                    self.run_fn_hook('h_runlevel_appl') #inlining RUNLEVEL_APPL
                    
                    next_cw_activity_check = time.time() + const.CORE_THREAD_ACTIVITY_CHECK_TIME

                    # continuous thread status check during application run
                    # application will be stopped if process is not active
                    while (current.status > const.CORE_THREAD_ALIVE and self._observer_status >= const.CORE_THREAD_ALIVE):
                        
                        # check thread activity, event htk_before_cw_activity_check is fired first
                        if (time.time() >= next_cw_activity_check):                                                          
                            ev = event.Event('htk_before_cw_activity_check')    
                            self.fire_event(ev)                            
                            if ev.will_run_default():
                                self._check_cw_activity()
                                
                            next_cw_activity_check = time.time() + const.CORE_THREAD_ACTIVITY_CHECK_TIME
                        
                        # switch thread context, via event htk_on_cobserver_ctx_switch
                        try:    
                            ev = event.Event('htk_on_cobserver_ctx_switch')     
                            self.fire_event(ev)
                        except:
                            ex_type, ex, tb = sys.exc_info()
                            print(ex_type)
                            print(ex)
                            traceback.print_tb(tb)
                        
                        # sleep process, status will be checked again after sleep time
                        self.dmsg('htk_on_debug_info', self._trn.msg('htk_observer_sleep'), self.fromhere(), 5)            
                        time.sleep(const.CORE_OBSERVER_SLEEP_TIME)
                        #res = current.msgq.send("SOME Message text")
                        #print("Observer sent message {0}".format(res))   
                        self.dmsg('htk_on_debug_info', self._trn.msg('htk_observer_awake'), self.fromhere(), 5)
                     
                    # final cleanup                                        
                    self.stop_services()        
                    self.destroy_core_threads()
                    self.dmsg('htk_on_debug_info', self._trn.msg('htk_observer_term'), self.fromhere(), 5)
                    self.dmsg('htk_on_debug_info', self._trn.msg('htk_pid_file_delete', self._pid_file), self.fromhere()) 
                    self._remove_pid_file(self._pid_file)
                                             
                except InputError as desc:
                    self.dmsg('htk_on_error', self._trn.msg('htk_reg_msg_service_failed', desc), self.fromhere())
                    self._stop_app()                                                         
            else: raise ValueError                                                                            
        except configparser.NoOptionError:
            self.dmsg('htk_on_error', self._trn.msg('htk_conf_opt_missing', 'Core', 'omsgq_transport_type'), self.fromhere())
            self._stop_app()
        except ValueError as desc:
            self.dmsg('htk_on_error', self._trn.msg('htk_conf_opt_val_err', 'Core', 'omsgq_transport_type', desc), self.fromhere())
            self._stop_app()    
        
    def _c_worker(self, i, status, action_status, pipe_conn, is_alive_check): 
        """Method watches worker process during its lifecycle
        
        Process polls messages from queue
        
        Args:            
           i (int): process id
           status (int): activity status
           action_status (int): action status
           pipe_conn (obj): pipe process connection
           is_alive_check
           
        Returns:
           void      
            
        Raises:
           event: htk_on_cworker_init
                
        """  
                
        ev = event.Event('htk_on_cworker_init')     
        self.fire_event(ev)
        if ev.will_run_default():
            setproctitle.setproctitle('hydratk/core:' + str(i)) # mark process to be identified in list of processes
            # updating signal hooks to work properly
            self._reg_self_signal_hooks() 
                                                
            current = multiprocessing.current_process()                        
            options = {
                    'socket_type' : zmq.PULL,
            }        
            current.pipe_conn = pipe_conn
            current.status = status     
            current.action_status = action_status
            current.is_alive_check = is_alive_check          
            #current.msgq = self._msg_router.get_queue(self._core_msg_service_id, messagerouter.MESSAGE_QUEUE_ACTION_CONNECT, options)
            
            # initialize process as message queue receiver
            context = zmq.Context()
            socket_pull = context.socket(zmq.PULL)
            socket_pull.connect("ipc:///tmp/hydratk/core.socket")
            
            # Initialize poll set
            poller = zmq.Poller()
            poller.register(socket_pull, zmq.POLLIN) #pull socket
            
            current.poller = poller      #assign poller to the current process
            current.msgq   = socket_pull #assign pull socket to the current process
                    
            self.dmsg('htk_on_debug_info', self._trn.msg('htk_core_msgq_connect_ok', self._msg_router.get_service_address(self._core_msg_service_id)), self.fromhere())
                        
            self.dmsg('htk_on_debug_info', self._trn.msg('htk_cworker_init'), self.fromhere()) 
            
            # continuous thread status check        
            while (current.status.value > const.CORE_THREAD_ALIVE):
                current.is_alive_check.value = time.time()             
                # check queue for messages if process is working, process them, sleep after          
                if (current.status.value == const.CORE_THREAD_WORK):                
                    socks = dict(poller.poll(100))                
                    if socket_pull in socks and socks[socket_pull] == zmq.POLLIN:                                
                        thr_intq_sleep = self._check_core_msg_queue()
                        if (thr_intq_sleep):                    
                            self.dmsg('htk_on_debug_info', self._trn.msg('htk_cthread_sleep'), self.fromhere(), 5)
                            time.sleep(1.0)
                            self.dmsg('htk_on_debug_info', self._trn.msg('htk_cthread_awake'), self.fromhere(), 5)
                    else:
                        self.dmsg('htk_on_debug_info', self._trn.msg('htk_cthread_sleep'), self.fromhere(), 5)
                        time.sleep(1.0)
                        self.dmsg('htk_on_debug_info', self._trn.msg('htk_cthread_awake'), self.fromhere(), 5)
                # check queue for messages if process is waiting, process them, sleep after
                elif (current.status.value == const.CORE_THREAD_WAIT):
                    self._check_cw_privmsg(current) 
                    self.dmsg('htk_on_debug_info', self._trn.msg('htk_cthread_sleep'), self.fromhere(), 5)
                    time.sleep(1)
                    self.dmsg('htk_on_debug_info', self._trn.msg('htk_cthread_awake'), self.fromhere(), 5)
               
            self.dmsg('htk_on_debug_info', self._trn.msg('htk_cworker_term'), self.fromhere())       
    
    def _check_co_privmsg(self):
        """Method checks queue for observer messages and processes them
        
        Args:      
           none      
           
        Returns:
           void      
                
        """  
                
        self.dmsg('htk_on_debug_info', 'checking privmsg', self.fromhere(), 1)
        try:
            for thr in self._thr:
                pipe_conn = thr.pipe_conn
                while (self._dopoll(pipe_conn)):
                    msg = pipe_conn.recv()
                    self._process_cw_msg(msg, thr)
                    
        except Exception as e:
            self.dmsg('htk_on_error', e, self.fromhere())
            tb = traceback.format_exc()
            pprint.pprint(tb) 
                    
    def _write_config_db(self, db_file):      
        """Method writes data from configuration file to database
        
        Args:
           db_file (str): database filename including path           
           
        Returns:
           void      
                
        """          
          
        db = dbconfig.DBConfig(db_file)
        db.connect()
        self.dmsg('htk_on_debug_info', self._trn.msg('htk_write_cfg_db'), self.fromhere())
        db.writedb(self._config)             
        
    def _dopoll(self, poller):
        """Method reads message from queue
        
        Args:         
           poller (obj): message queue receiver
           
        Returns:
           obj: message      
                
        """
                
        while True:
            try:
                return poller.poll()
            except Exception as e: #except IOError as e:
                if e.errno != errno.EINTR:
                    raise e                      
    
    def _check_core_msg_queue(self):
        """Method checks queue for message
        
        Message is sent via event if present (method doesn't wait if queue is empty)
        
        Args:    
           none     
           
        Returns:
           bool: True/False if queue is/isn't empty   
                
        """
                
        current = multiprocessing.current_process()
        mq = current.msgq
        q_empty = False
        try:
            current.action_status.value = const.CORE_THREAD_ACTION_PROCESS_MSG                     
            msg = mq.recv(zmq.NOBLOCK)           
            self._trigger_cmsg(msg)
        except zmq.error.Again:                    
            q_empty = True
                
        except zmq.ZMQError:
            ex_type, ex, tb = sys.exc_info()
            print(ex_type)
            print(ex)
            traceback.print_tb(tb) 
            
        current.action_status.value = const.CORE_THREAD_ACTION_NONE                                                                                                      
        return q_empty      
    
    def _check_cw_privmsg(self):
        """Method checks queue for worker messages and processes them
        
        Args:       
           none     
           
        Returns:
           void      
                
        """          
        
        self.dmsg('htk_on_debug_info', self._trn.msg('htk_cworker_check_priv_msg'), self.fromhere(), 1) 
        current = multiprocessing.current_process()
        try:
            while (self._dopoll(current.pipe_conn)):
                current.action_status.value = const.CORE_THREAD_ACTION_PROCESS_PRIVMSG
                msg = current.pipe_conn.recv()
                self._process_privmsg(msg)
                current.action_status.value = const.CORE_THREAD_ACTION_NONE
        except Exception as e:            
            self.dmsg('htk_on_error', e, self.fromhere())
            ex_type, ex, tb = sys.exc_info()
            print(ex_type)
            print(ex)
            traceback.print_tb(tb)    
    
    def _check_cw_activity(self):
        """Method checks worker activity
        
        Args:     
           none       
           
        Returns:
           void      
                
        """  
                
        for thr in self._thr:            
            # current.last_ping_response = 0
            # current.response_alert_level = 1
            '''Last ping check'''
            if (thr.response_alert_level == const.CORE_THREAD_NORESPONSE):
                '''Thread is not responding, trying to respawn'''
                pass
            else:
                if thr.next_check_time >= time.time():
                    activity_time = time.time() - thr.is_alive_check.value
                    #self.__send_ping(thr)
                    self.dmsg('htk_on_debug_info', self._trn.msg('htk_cworker_check_activity', str(thr.num), activity_time.__str__()), self.fromhere(), 1)
                else:
                    thr.response_alert_level += 1                    
            thr.next_check_time = time.time() + const.CORE_THREAD_PING_TIME
            
    def _do_command_action(self):  
        """Method processes command
        
        Command must have registered callback
        
        Args:  
           none          
           
        Returns:
           void      
                
        """  
                      
        if (self._command != None):                                
            if (self._command in self._cmd_hooks):                               
                self._run_command_hooks(self._command)
                       
        else:
            self._run_command_hooks(self._default_command)
    
    def _load_db_config(self):
        """Method loads configuration from database
        
        Database file is stored in configuration System/DBConfig/db_file
        
        Args:     
           none       
           
        Returns:
           void      
                
        """        
                
        db_file = self._config['System']['DBConfig']['db_file']
        db = dbconfig.DBConfig(db_file)        
        db.connect()
        cfg = db.db2cfg(active_only = True)
        for grp, obj, itmk, itmv, _ in cfg:
            grp = str(grp)
            obj = str(obj)
            itmk = str(itmk)
            itmv = str(itmv)
            itmv = int(itmv) if itmv.isdigit() else itmv
            if grp not in self._config:
                self._config[grp] = {}
            if obj not in self._config[grp]:
                self._config[grp][obj] = {}
                  
            self._config[grp][obj][itmk] = itmv # update in memory configuration
    
    
    def _process_extension_configs(self):
        """Method searches configuration directory for extension specific configuration files
        
        Each file is reported via event htk_before_append_extension_config_file
        
        Args:  
           none          
           
        Returns:
           void
           
        Raises:
           event: htk_before_append_extension_config_file      
                
        """            
        
        if (os.path.exists(self._ext_confd)):                    
            for dirname, _, filelist in os.walk(self._ext_confd): # subdir_list not used            
                for fname in filelist:
                    if fname.split('.')[1] == 'conf':
                        ext_config_file = dirname + '/' + fname
                        ev = event.Event('htk_before_append_extension_config_file', ext_config_file)        
                        if (self.fire_event(ev) > 0):
                            ext_config_file = ev.argv(0)
                        if ev.will_run_default():
                            self._append_extension_config_from_file(ext_config_file)
    
    
    def _append_extension_config_from_file(self, ext_config_file):
        """Method parses extension configuration file
        
        Args:  
           ext_config_file (str): config filename including path          
           
        Returns:
           void 
                
        """      
                
        if (os.path.exists(self._ext_confd)):
            try:
                self.dmsg('htk_on_debug_info', self._trn.msg('htk_loading_ext_cfg', ext_config_file), self.fromhere())
                with open(ext_config_file, 'r') as f:                    
                    ext_config = yaml.load(f)
                    self._merge_base_config(ext_config)                                                            
                self.dmsg('htk_on_debug_info', self._trn.msg('htk_ext_cfg_loaded', ext_config_file), self.fromhere())   
                
            except Exception as detail:
                self.errmsg(detail)
                ex_type, ex, tb = sys.exc_info()
                traceback.print_tb(tb)
                sys.exit(1)
     
    def _merge_base_config(self, config): 
        """Method merges configuration with in memory configuration
        
        Args:  
           config (dict): configuration with dictionary structure         
           
        Returns:
           void 
                
        """  
                               
        for gk, gv in config.items():
            for ok, ov in gv.items():
                for kk, kv in ov.items():                    
                    if gk != '' and ok != '' and kk != '':
                        if gk not in self._config: self._config[gk] = {}
                        if ok not in self._config[gk]: self._config[gk][ok] = {}
                        self._config[gk][ok][kk] = kv # update in memory configuration                                                                        
                                        
    def _load_base_config(self): 
        """Method loads base configuration from file
        
        Args:        
           none  
           
        Returns:
           void 
                
        """  
                                      
        if (os.path.exists(self._config_file)):            
            try:
                self.dmsg('htk_on_debug_info', self._trn.msg('htk_loading_base_cfg', self._config_file), self.fromhere())
                with open(self._config_file, 'r') as f:                    
                    self._config = yaml.load(f)                                                            
                self.dmsg('htk_on_debug_info', self._trn.msg('htk_base_cfg_loaded', self._config_file), self.fromhere())                
            except Exception as detail:
                print('except here')
                self.errmsg(detail)
                ex_type, ex, tb = sys.exc_info()
                traceback.print_tb(tb)
                sys.exit(1)
        else:
            self.dmsg('htk_on_error', self._trn.msg('htk_loading_base_cfg', self._config_file), self.fromhere())
            
    def _apply_config(self): 
        """Method initializes several configurable options
        
        Debug, language, message router, count of workers
                
        Configuration options:
        System/Debug/enabled
        System/Debug/level
        System/Language/id
        Core/Options/run_mode
        Core/MessageRoute/id
        Core/Workers/total
        
        Args:
           none         
           
        Returns:
           void 
                
        """  
                              
        from hydratk.translation.core import info
        
        # get debug from command option or configuration
        if (not self.check_debug()):
            try:                                             
                if (self._config['System']['Debug']['enabled'] == 1):
                    self._debug = True                        
                    self.dmsg('htk_on_debug_info', self._trn.msg('htk_debug_enabled'), self.fromhere())
                else:
                    self._debug = False 
              
               
            except Exception as exc:
                self.dmsg('htk_on_warning', self._trn.msg('htk_conf_opt_missing', 'Debug', 'enabled'), self.fromhere())
            try:                         
                debug_level = self._config['System']['Debug']['level']
                self._debug_level = int(debug_level) if debug_level > 0 else 1                                              
                self.dmsg('htk_on_debug_info', self._trn.msg('htk_debug_level_set', debug_level), self.fromhere())                
            except Exception as exc:
                pprint.pprint(exc)
                self.dmsg('htk_on_warning', self._trn.msg('htk_conf_opt_missing', 'Debug', 'level'), self.fromhere())   
        
        # import langtexts, get language from command option or configuration    
        try:
            if (not self.check_language()):                
                language = self._config['System']['Language']['id']
                self._language = language if language in info.languages else const.DEFAULT_LANGUAGE                                            
            self.dmsg('htk_on_debug_info', self._trn.msg('htk_lang_set', info.language_desc[self._language]), self.fromhere())
            self._trn.set_language(self._language)
            self._import_global_messages()                
        except Exception as exc:
            self.dmsg('htk_on_warning', self._trn.msg('htk_conf_opt_missing', 'General', 'language'), self.fromhere())
            
        
        try:
            # get run mode from command option or configuration
            if (not self.check_run_mode()):                
                run_mode = self._config['Core']['Options']['run_mode']
                self._run_mode = run_mode if run_mode in const.core_run_mode_enum_desc else const.DEFAULT_RUN_MODE                                        
            self.dmsg('htk_on_debug_info', self._trn.msg('htk_run_mode_set', self._run_mode, const.core_run_mode_enum_desc[self._run_mode]), self.fromhere())             
        except Exception as exc:
            self.dmsg('htk_on_warning', self._trn.msg('htk_conf_opt_missing', 'General', 'language'), self.fromhere())
            
        '''
        TODO: temporary disabled, will be redesigned            
        if 'extensions_dir' in self._config['System']['Extending'] and os.path.exists(self._config['System']['Extending']['extensions_dir']):
            sys.path.append(self._config['System']['Extending']['extensions_dir'])
        else: 
            self._use_extensions = False
                        
            self.dmsg('htk_on_warning', self._trn.msg('htk_ext_ext_dir_not_exists', self._config['System']['Extending']['extensions_dir']), self.fromhere())   
        ''' 
            
        # get message router id from configuration
        try:
            msg_router_id = self._config['Core']['MessageRouter']['id']            
            if (msg_router_id != ''):
                self._msg_router_id = msg_router_id
            else: raise ValueError                                                
            self.dmsg('htk_on_debug_info', self._trn.msg('htk_msg_router_id_set', msg_router_id), self.fromhere())                
        except Exception as exc:
            self.dmsg('htk_on_warning', self._trn.msg('htk_conf_opt_missing', 'Core', 'msg_router_id'), self.fromhere())
        except ValueError as desc:
            self.dmsg('htk_on_warning', self._trn.msg('htk_conf_opt_val_err', 'Core', 'msg_router_id', desc), self.fromhere())
            
        # get count of workers from configuration or from processor cores
        try:
            workers = self._config['Core']['Workers']['total']            
            if (workers != ''):
                workers = int(workers)
                self._num_threads = multiprocessing.cpu_count() if (workers < 1) else workers                
            else: raise ValueError                                                
            self.dmsg('htk_on_debug_info', self._trn.msg('htk_core_workers_num_set', self._num_threads), self.fromhere())                
        except Exception as exc:
            self.dmsg('htk_on_warning', self._trn.msg('htk_conf_opt_missing', 'Core', 'workers'), self.fromhere())
        except ValueError as desc:
            self.dmsg('htk_on_warning', self._trn.msg('htk_conf_opt_val_err', 'Core', 'workers', desc), self.fromhere())       

    def _load_extensions(self): 
        """Method loads extensions specified in configuration
        
        Internal extensions are imported as module
        
        External extensions are included to PYTHONPATH

        Args:         
           none
           
        Returns:
           void 
                
        """         
               
        if 'Extensions' in self._config:
            try:                       
                for ext_name, ext_cfg in self._config['Extensions'].items():                                                            
                                                                  
                    '''External extension package file'''
                    if 'file' in ext_cfg:
                        if os.path.exists(ext_cfg['file']) and os.path.isfile(ext_cfg['file']):
                            sys.path.append(ext_cfg['file'])
                            self.dmsg('htk_on_debug_info', self._trn.msg('htk_loading_extension', ext_name, ext_cfg['file']), self.fromhere())
                        else:
                            self.dmsg('htk_on_debug_info', self._trn.msg('htk_extension_wrong_cfg_file', ext_name, ext_cfg['file']), self.fromhere())
                            break 
                        '''Internal extension'''
                    if 'module' in ext_cfg and 'package' in ext_cfg:
                        self._load_extension(ext_name, ext_cfg)
                                
                    else:
                        self.dmsg('htk_on_debug_info', self._trn.msg('htk_extension_wrong_cfg', ext_name), self.fromhere())
                                        
        
            except Exception as detail:                        
                self.dmsg('htk_on_error', self._trn.msg('htk_fail_load_int_ext', ext_name, detail), self.fromhere())
                #tb = traceback.format_exc()
                #pprint.pprint(tb) 
                sys.exit(1)
        self.dmsg('htk_on_debug_info', self._trn.msg('htk_fin_load_int_ext'), self.fromhere()) 
      
    def _load_extension(self, ext_name, ext_cfg):
        """Method loads internal extension

        Args:  
           ext_name (str): extension name
           ext_cfg (dict): extension configuration      
           
        Returns:
           void 
           
        Raises:
           exception: Exception
                
        """  
                
        ext_module = ext_cfg['module']
        ext_base_path = ext_cfg['package']                
        ext_full_path = ext_base_path + '.' + ext_module 
        
        if ext_name not in self._ext: 
            # import extension (including langtexts) if enabled                    
            try:
                if 'enabled' not in ext_cfg:
                    self.dmsg('htk_on_error', self._trn.msg('htk_conf_opt_missing', 'Extension_' + ext_name, 'enabled'), self.fromhere())
                else:
                    if (ext_cfg['enabled'] == 1):
                        self.dmsg('htk_on_debug_info', self._trn.msg('htk_load_int_ext', ext_name), self.fromhere())                                                                                   
                        ext = self._extension_module_import(ext_full_path)
                        self._import_extension_messages(ext_base_path)                                         
                        self._ext[ext_name] = ext.Extension(self)
                        self.dmsg('htk_on_debug_info', self._trn.msg('htk_load_int_ext_success', self._ext[ext_name].get_ext_info()), self.fromhere())
                                   
            except Exception as e:
                import traceback, pprint
                self.dmsg('htk_on_extension_error', self._trn.msg('htk_fail_init_int_ext', ext_name, str(e)), self.fromhere())
                print(sys.exc_info())
                ex_type, ex, tb = sys.exc_info()
                traceback.print_tb(tb)
                #tb = traceback.format_exc(e)
                #pprint.pprint(tb) 
                #pprint.pprint(sys.path)
        else:
            raise Exception(self._trn.msg('htk_duplicate_extension', ext_name))         

    def _extension_module_import(self, ext_full_path):
        """Method imports extension

        Args:  
           ext_full_path (str): full module package name    
           
        Returns:
           obj: module 
                
        """  
                
        mod = __import__(ext_full_path)
        components = ext_full_path.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod
    
    def _load_module_from_file(self, filepath):
        """Method loads module from file
        
        Supported formats: py (source code), pyc (compiled code)

        Args:  
           filepath (str): filename including path  
           
        Returns:
           obj: module 
                
        """  
                
        import pprint

        module = None
        expected_class = 'Extension'               
        mod_name, file_ext = os.path.splitext(os.path.split(filepath)[-1])                        
        if file_ext.lower() == '.py':            
            py_mod = imp.load_source(mod_name, filepath)
            
        elif (file_ext.lower() == '.pyc'):
            py_mod = imp.load_compiled(mod_name, filepath)

        if expected_class in dir(py_mod):            
            module = py_mod             
        return module
                
    def _import_extension_messages(self, ext_path):
        """Method imports extension langtexts and commands help        

        Args:  
           ext_path (str): filename including path  
           
        Returns:
           void
                
        """  
                
        msg_package  = ext_path + '.translation.'+self._language+'.messages'
        help_package = ext_path + '.translation.'+self._language+'.help'
        
        # import langtexts
        try:
            self.dmsg('htk_on_debug_info', self._trn.msg('htk_load_ext_msg', self._language, str(msg_package)), self.fromhere())             
            lang = importlib.import_module(msg_package)
            self._trn.add_msg(lang.msg)            
            self.dmsg('htk_on_debug_info', self._trn.msg('htk_load_ext_msg_success', self._language), self.fromhere())            
        except ImportError as e:
            self.dmsg('htk_on_error', self._trn.msg('htk_load_ext_msg_failed', self._language, str(e)), self.fromhere())
            
        # import commands help                                    
        try:            
            self.dmsg('htk_on_debug_info', self._trn.msg('htk_load_ext_help', self._language, str(help_package)), self.fromhere())            
            help_msg = importlib.import_module(help_package)
            self._trn.add_help(help_msg)            
        except ImportError as e:
            self.dmsg('htk_on_error', self._trn.msg('htk_load_ext_help_failed', self._language, str(e)), self.fromhere())   
            
    def _import_package_messages(self, import_package, msg_package):
        """Method imports package langtexts      

        Args:  
           import_package (str): full package name
           msg_package (str): full package directory name
           
        Returns:
           void
                
        """  
                
        msg_package  = msg_package+'.'+self._language+'.messages'
        
        try:            
            self.dmsg('htk_on_debug_info', self._trn.msg('htk_load_package_msg', import_package, self._language), self.fromhere())                          
            lang = importlib.import_module(msg_package)
            self._trn.add_msg(lang.msg)
            self.dmsg('htk_on_debug_info', self._trn.msg('htk_load_package_msg_success', import_package, self._language), self.fromhere())                        
        except ImportError as e:
            self.dmsg('htk_on_error', self._trn.msg('htk_load_package_msg_failed', import_package, self._language, str(e)), self.fromhere())  
        
        
    def _import_global_messages(self):
        """Method imports global langtexts and command help  

        Args:  
           none
           
        Returns:
           void
                
        """  
                
        msg_package  = 'hydratk.translation.core.'+self._language+'.messages'
        help_package = 'hydratk.translation.core.'+self._language+'.help'
        
        # import langtexts
        try:            
            self.dmsg('htk_on_debug_info', self._trn.msg('htk_load_global_msg', self._language, msg_package), self.fromhere())                          
            self._trn.msg_mod = importlib.import_module(msg_package)
            self._trn.register_messages(self._trn.msg_mod.msg)
            self.dmsg('htk_on_debug_info', self._trn.msg('htk_load_global_msg_success', self._language), self.fromhere())                        
        except ImportError as e:
            self.dmsg('htk_on_error', self._trn.msg('htk_load_global_msg_failed', self._language, str(e)), self.fromhere()) 
            
        # import command help            
        try:
            self.dmsg('htk_on_debug_info', self._trn.msg('htk_load_global_help', self._language, str(help_package)), self.fromhere())                        
            self._trn.set_help_mod(importlib.import_module(help_package))                                   
            self.dmsg('htk_on_debug_info', self._trn.msg('htk_load_global_help_success', self._language), self.fromhere())            
        except ImportError as e:
            self.dmsg('htk_on_error', self._trn.msg('htk_load_global_help_failed', self._language, str(e)), self.fromhere())    
       
                
    def _reg_self_command_hooks(self):  
        """Method registers global commands hooks

        Args: 
           none 
           
        Returns:
           void
                
        """          
                      
        hooks = [
                {'command' : 'start', 'callback' : self._start_app },
                {'command' : 'stop', 'callback' : self._stop_app_command },
                {'command' : 'short-help', 'callback' : CommandlineTool.print_short_help },
                {'command' : 'help', 'callback' : CommandlineTool.print_help },
                {'command' : 'list-extensions', 'callback' : self._list_extensions },
                {'command' : 'create-config-db', 'callback' : self._create_config_db },
                {'command' : 'create-ext-skel', 'callback' : self.create_ext_skel },
                {'command' : 'create-lib-skel', 'callback' : self.create_lib_skel },
            ]
        self.register_command_hook(hooks)  
    
    def _runlevel_baseinit(self):     
        """Method executes specific processing for runlevel baseinit
        
        Initialize translator, import global langtexts, register hooks

        Args:  
           none
           
        Returns:
           bool: True
                
        """   
                        
        self._runlevel = const.RUNLEVEL_BASEINIT
        
        '''Setting up dynamic translation messages import hook'''
        sys.meta_path.append(self)
                              
        current   = threading.currentThread()
        current.status = const.CORE_THREAD_ALIVE    
                                                      
        self._trn = translator.Translator()
        self._trn.set_debug_level(const.DEBUG_LEVEL)                
        
        """Checking for the --lang param presence"""
        if self.check_language() == False:          
            self._trn.set_language(self._language)
        
        self._import_global_messages()
                
        
        self._reg_self_command_hooks()
        self._reg_self_event_hooks()
        
        if (len(sys.argv) > 1 and sys.argv[1] != 'help'):
            self.check_config()
            
            '''Checking run mode'''        
            self.check_run_mode() 
                                         
        return True
                                    
    def _runlevel_config(self):
        """Method executes specific processing for runlevel config
        
        Load configuration from several sources - base, extensions, database

        Args:  
           none
           
        Returns:
           bool: True
                
        """   
                
        self._runlevel = const.RUNLEVEL_CONFIG        
        self._load_base_config()
        self._process_extension_configs()
        if self._config['System']['DBConfig']['enabled'] == 1:
            if os.path.isfile(self._config['System']['DBConfig']['db_file']) and os.path.getsize(self._config['System']['DBConfig']['db_file']) > 256:
                self._load_db_config()        
        self._apply_config()
        return True #required by fn_hook
        
    
    def _runlevel_extensions(self):
        """Method executes specific processing for runlevel extensions
        
        Load extensions

        Args:  
           none
           
        Returns:
           bool: True
           
        Raises:
           event: htk_before_load_extensions
           event: htk_after_load_extensions
                
        """ 
                
        self._runlevel = const.RUNLEVEL_EXTENSIONS
        ev = event.Event('htk_before_load_extensions')     
        self.fire_event(ev)
        self._load_extensions()         
        ev = event.Event('htk_after_load_extensions')     
        self.fire_event(ev)
        return True #required by fn_hook
    
    def _runlevel_cli(self):
        """Method executes specific processing for runlevel cli
        
        Parse command options

        Args:  
           none
           
        Returns:
           bool: True
                
        """ 
                
        self._runlevel = const.RUNLEVEL_CLI
        self._set_default_cli_params()
        self._parse_cli_args()
        return True #required by fn_hook
    
    def _runlevel_core(self):
        """Method executes specific processing for runlevel core
        
        Subscribe managers if running in parallel processing mode

        Args:  
           none
           
        Returns:
           bool: True
                
        """ 
                
        self._runlevel = const.RUNLEVEL_CORE
        #subscribe managers
        if self._run_mode >= const.CORE_RUN_MODE_PP_APP:                    
            '''Initializing pp support'''
            from multiprocessing import Manager
            from hydratk.lib.dynamic import callback
                        
            self._fn_cb_shared     = Manager().dict()
            self._async_fn_tickets = Manager().dict()
            self._cbm              = callback.CallBackManager(self._fn_cb, self._fn_cb_shared)
            self._cbm.set_async_handler(AsyncCallBackHandler(self)) 
             
            self._init_message_router()
            self._c_observer()
            
        return True #required by fn_hook
    
    def _runlevel_appl(self):
        """Method executes specific processing for runlevel appl
        
        Process command

        Args:  
           none
           
        Returns:
           bool: True
                
        """ 
                
        self._runlevel = const.RUNLEVEL_APPL        
        if (self.have_command_action()):
            self._do_command_action()
        return True #required by fn_hook
    
    def _run_command_option_hooks(self, command_opt, command_opt_value):
        """Method is processing specified command option callbacks.
           
        This method runs automatically in runlevel cli, if there're specified options. 
        
        Args:
           command_opt (str): command option
           command_opt_value (str): option value
        
        Returns:            
           int: number of processed callbacks
                              
        """
        
        processed_callbacks = 0
        if command_opt in self._cmd_option_hooks:                        
            for record in self._cmd_option_hooks[command_opt]:                                                               
                cb = record['callback']                
                cb(command_opt_value)
                processed_callbacks += 1
        
        else:
            pass        
            #possibly notify about unregistered command option
        return processed_callbacks   
    
    def _run_command_hooks(self, command):
        """Method is processing specified command callbacks.
           
        By default this method is called in runlevel appl if there's command specified 
        
        Args:
           command (str): command
        
        Returns:            
           int: number of processed callbacks                  
           
        """
        
        processed_callbacks = 0
        if command in self._cmd_hooks:                        
            for record in self._cmd_hooks[command]:                                                               
                cb = record['callback']                
                cb()
                processed_callbacks += 1
        
        else:
            pass        
            #possibly notify about unregistered command
        return processed_callbacks
    
    
    def _set_default_cli_params(self):
        """Method initializes command line according to configuration
        
        Args:
           none
        
        Returns:            
           void                
           
        """
                
        CommandlineTool.set_translator(self._trn)
        
        '''Define commands'''
        if self._opt_profile in commandopt.cmd:                                    
            CommandlineTool.set_possible_commands(commandopt.cmd[self._opt_profile])  
                      
        '''Define options'''             
        short_opt = commandopt.short_opt[self._opt_profile] if self._opt_profile in commandopt.short_opt else [] 
        long_opt  = commandopt.long_opt[self._opt_profile] if self._opt_profile in commandopt.long_opt else []                                                     
        CommandlineTool.set_possible_options(short_opt, long_opt)        
        
        '''Set help text'''      
        cmd_text = {}
        for cmd in commandopt.cmd[self._opt_profile]: 
            if cmd in self._trn.help_mod.help_cmd:
                cmd_text[cmd] = self._trn.help_mod.help_cmd[cmd]
            else: self.dmsg('htk_on_warning', self._trn.msg('htk_help_cmd_def_missing', cmd, self._language), self.fromhere())                            
        opt_text = {}
        for opt in commandopt.long_opt[self._opt_profile]:
            if opt in self._trn.help_mod.help_opt:
                opt_text.update(self._trn.help_mod.help_opt[opt])
            else: self.dmsg('htk_on_warning', self._trn.msg('htk_option_def_missing', opt, self._language), self.fromhere())   
                                                    
        CommandlineTool.set_help(self._help_title, self._cp_string, cmd_text, opt_text)                   
    
    def _set_pid_file(self, pid_file):
        """Method creates PID file
        
        Args:
           pid_file (str): PID filename including path
        
        Returns:            
           int: PID                
           
        """
                
        pid = os.getpid()
        if (pid_file != ''):                                    
            file_path = os.path.dirname(pid_file)
            if (not os.path.exists(file_path)):                                                
                            os.makedirs(file_path)
            f = open(pid_file, 'w')
            f.write(str(pid))
            f.close()
        return pid          
    
    def _notify_thread(self, pid):
        """Method notifies thread via signal SIGPIPE
        
        Args:
           pid (int): PID to be notified
        
        Returns:            
           void               
           
        """
                
        os.kill(pid, signal.SIGPIPE)
        
    def _send_ping(self, thr):
        """Method sends PING message to thread
        
        Args:
           thr (obj): thread to be pinged 
        
        Returns:            
           void               
           
        """
                
        timestamp = time.time()
        thr.last_ping = timestamp
        msg = {
               'type' : message.REQUEST,
               'command' : message.PING,
               'from' : 'MasterHead:0',
               'to'   : 'MasterHead:' + str(thr.num),
               'time' : timestamp,
               'zone' : 'Core'
               }
        thr.pipe_conn.send(msg)
        self._notify_thread(thr.pid)
        
    def _service_starter(self, cb, service_status, parent_conn):
        """Method starts service process
        
        Args:
           cb (method): callback method
           service_status (int): service status
           parent_conn (obj): pipe connection
        
        Returns:            
           void               
           
        """
                
        current = multiprocessing.current_process() 
        setproctitle.setproctitle('hydra/srv:' + current.service_name) # mark process to be identified in list of processes
        self._reg_service_signal_hooks()
        cb(service_status, parent_conn)
        
    def _sig_retriever(self, signum, frame):
        """Method handles received signal
        
        If signal is supported (see hydratk.core.hsignal), new event is fired
        Not supported signals are ignored
        
        Args:
           signum (int): signal number
           frame: NOT USED
        
        Returns:            
           void   
           
        Raises:
           event: htk_on_signal 
           event: htk_on_sigterm|htk_on_sigint|htk_on_sigpipe|htk_on_sigalamr         
           
        """
                
        self.fire_event(event.Event('htk_on_signal', signum))
        if signum in hsignal.sig2event:
            self.fire_event(event.Event(hsignal.sig2event[signum]))
    
    def _reg_service_signal_hooks(self):
        """Method registers signal hooks supported for services
        
        Args:
           none
        
        Returns:            
           void         
           
        """
                        
        signal.signal(signal.SIGTERM, self._sig_retriever)
        signal.signal(signal.SIGINT, self._sig_retriever)
        signal.signal(signal.SIGPIPE, self._sig_retriever)        
        hook = [{'event' : 'htk_on_signal', 'callback' : self._ec_sig_handler, 'unpack_args' : True}]        
        self.register_event_hook(hook)
    
    
    def _reg_self_fn_hooks(self):
        """Method registers functionality hooks
        
        Bootstrap, runlevels
        
        Args:
           none
        
        Returns:            
           void         
           
        """
                
        hook = [
                {'fn_id' : 'h_bootstrap', 'callback' : self._bootstrap },
                {'fn_id' : 'h_runlevel_baseinit', 'callback' : self._runlevel_baseinit },
                {'fn_id' : 'h_runlevel_config', 'callback' : self._runlevel_config },
                {'fn_id' : 'h_runlevel_extensions', 'callback' : self._runlevel_extensions },
                {'fn_id' : 'h_runlevel_cli', 'callback' : self._runlevel_cli },
                {'fn_id' : 'h_runlevel_core', 'callback' : self._runlevel_core },
                {'fn_id' : 'h_runlevel_appl', 'callback' : self._runlevel_appl }               
            ]                    
        self.register_fn_hook(hook)
        
        #queue messages handling
        self._reg_msg_handlers()
    
    def _reg_self_event_hooks(self):
        """Method registers event hooks
        
        Args:
           none
        
        Returns:            
           void         
           
        """        
        
        hook = [
                {'event' : 'htk_on_error', 'callback' : self._eh_htk_on_error, 'unpack_args' : True},        
                {'event' : 'htk_on_warning', 'callback' : self._eh_htk_on_warning, 'unpack_args' : True}, 
                {'event' : 'htk_on_debug_info', 'callback' : self._eh_htk_on_debug_info, 'unpack_args' : True},
                {'event' : 'htk_on_cprint', 'callback' : self._eh_htk_on_cprint, 'unpack_args' : True},
                {'event' : 'htk_on_got_cmd_options', 'callback' : self._eh_htk_on_got_cmd_options },
                {'event' : 'htk_on_extension_error', 'callback' : self._eh_htk_on_extension_error, 'unpack_args' : True},
                {'event' : 'htk_on_extension_warning', 'callback' : self._eh_htk_on_extension_warning, 'unpack_args' : True},
                {'event' : 'htk_on_uncaught_exception', 'callback' : self._eh_htk_on_exception, 'unpack_args' : True},
                {'event' : 'htk_on_cmsg_recv', 'callback' : self._process_cmsg, 'unpack_args' : True}
                
            ]
                      
        self.register_event_hook(hook)
                            
    def _parse_cli_args(self): 
        """Method parses command and options
        
        Recognized commands are handled, unrecognized are ignored
        
        Args:
           none
        
        Returns:            
           void  
           
        Raises:
           event: htk_on_cmd_options       
           
        """  
                
        command = CommandlineTool.get_input_command()
        try:                
            options = CommandlineTool.get_input_options(commandopt.opt[self._opt_profile])
        except cmdoptparser.CmdOptParserError as err:
            options = False
            self.dmsg('htk_on_error', self._trn.msg('htk_unrecognized_opt', str(err)), self.fromhere())       
        if (len(sys.argv) > 1):
            if command == False:
                self.dmsg('htk_on_warning', self._trn.msg('htk_undetected_cmd'), self.fromhere())
                self._command = self._default_command                
            else:                                
                self._command = command
                        
            if options != False:                   
                for opt_name, opt_value in options['options'].items():
                    self._run_command_option_hooks(opt_name, opt_value)                    
                                        
                    if opt_name == '-h' or opt_name == '--help':
                        CommandlineTool.print_help()
                        break
                                        
                        
        else:
            self._command = self._default_command              
        self.fire_event(event.Event('htk_on_cmd_options'))  
     
    def _process_cw_msg(self, msg, thr):
        """Method processes PONG message from worker
        
        Args:
           msg (dict): message
           thr (obj): thread
        
        Returns:            
           void   
           
        """  
                
        if msg['zone'] == 'Core':
            if msg['command'] == message.PONG:
                thr.response_alert_level = 0
                thr.next_ping_time = time.time() + const.CORE_THREAD_PING_TIME
                try:
                    r_speed = 0                                      
                    r_speed = float(msg['time']) - float(thr.last_ping)
                except Exception as e:
                    print(e)
                self.dmsg('htk_on_debug_info', self._trn.msg('htp_cworker_prcess_msg', str(thr.num), str(r_speed)), self.fromhere()) 
    
    def _trigger_cmsg(self, msg): 
        """Method sends message in event
        
        Args:
           msg (dict): message
        
        Returns:            
           void 
           
        Raises:
           event: htk_on_cmsg_recv  
           
        """  
                              
        self.fire_event(event.Event('htk_on_cmsg_recv', msg))       
    
    def _response_ping(self, msg):
        """Method sends PONG message
        
        Args:
           msg (dict): message
        
        Returns:            
           void 
           
        """ 
                
        current = multiprocessing.current_process()
        if msg['zone'] == 'Core':
            msg = {
               'type'    : message.RESPONSE,
               'command' : message.PONG,
               'from'    : 'MasterHead:' + str(current.num),
               'to'      : 'MasterHead:0',
               'time'    : time.time(),
               'zone'    : 'Core'
               }
        current.pipe_conn.send(msg)
        self._notify_thread(os.getppid())
        pass
        
    def _process_privmsg(self, msg):
        """Method processes private message
        
        If PING message is received, PONG message is sent as response
        
        Args:
           msg (dict): message
        
        Returns:            
           void 
           
        Raises:
           event: h_privmsg_recv
           
        """ 
                
        # pprint.pprint(msg)        
        self.fire_event(event.Event('h_privmsg_recv', msg))
        if msg['type'] == message.REQUEST:
            if msg['command'] == message.PING:
                self._response_ping(msg)
    
                    
    def _remove_pid_file(self, pid_file):
        """Method deletes PID file
        
        Args:
           pid_file (str): PID filename including path
        
        Returns:            
           bool: result
           
        """ 
                
        result = False
        if os.path.exists(pid_file) and os.path.isfile(pid_file):
            os.unlink(pid_file)
            result = True
        return result
    
    def _reg_self_signal_hooks(self):  
        """Method registers signal hooks
        
        Args:
           none
        
        Returns:            
           void
           
        """ 
                      
        signal.signal(signal.SIGTERM, self._sig_retriever)
        signal.signal(signal.SIGINT, self._sig_retriever)
        signal.signal(signal.SIGPIPE, self._sig_retriever)
        
        hook = [{'event' : 'htk_on_signal', 'callback' : self._ec_sig_handler, 'unpack_args' : True}]
        if (multiprocessing.current_process().name == 'MainProcess'):                                    
            hook.extend(
                        [{'event' : 'htk_on_sigint', 'callback' : self._ec_stop_app },
                        {'event' : 'htk_on_sigterm', 'callback' : self._ec_stop_app },
                        {'event' : 'htk_on_sigpipe', 'callback' : self._ec_check_co_privmsg, 'unpack_args' : True}]
                    )
                        
        else:
            hook.extend(
                        [{'event' : 'htk_on_sigint', 'callback' : self._ec_parent_tell_signal },
                        {'event' : 'htk_on_sigterm', 'callback' : self._ec_parent_tell_signal },
                        {'event' : 'htk_on_sigpipe', 'callback' : self._ec_check_cw_privmsg }]
                    )
            
        self.register_event_hook(hook)
        
    def _start_app(self):
        """Method starts application
        
        Initialize observer process
        
        Args:
           none
        
        Returns:            
           void
           
        Raises:
           event: htk_on_start
           
        """ 
                
        self.dmsg('htk_on_debug_info', self._trn.msg('htk_app_start'), self.fromhere())
        cevent = event.Event('htk_on_start')
        self.fire_event(cevent)
        if cevent.will_run_default():
            self._init_message_router()                
            self._c_observer()
    
            
    def _stop_app(self, force_exit=False):
        """Method stops application
        
        Args:
           force_exit (bool): force application stopping
        
        Returns:            
           void
           
        Raises:
           event: htk_on_stop
           
        """ 
                
        self.dmsg('htk_on_debug_info', self._trn.msg('htk_app_stop'), self.fromhere())
        cevent = event.Event('htk_on_stop')        
        self.fire_event(cevent)
        if cevent.will_run_default():
            self._app_status = const.APP_STATUS_STOP
            self._observer_status = const.CORE_THREAD_EXIT
            current = multiprocessing.current_process()
            current.status = const.CORE_THREAD_EXIT
            if (force_exit):
                self.dmsg('htk_on_debug_info', self._trn.msg('htk_pid_file_delete'), self.fromhere()) 
                self._remove_pid_file(self._pid_file)
                sys.exit(1)
    
    def _stop_app_command(self):
        """Method stops application in controlled way
        
        Process is terminated using signal SIGTERM
        
        Configuration options - Core/Service/pid_file
        
        Args:
           none
        
        Returns:            
           void
           
        """ 
                
        pid_file = self._config['Core']['Service']['pid_file']
        if (os.path.exists(pid_file)):
            pid = open(pid_file).read()
            try:                
                os.kill(int(pid), 0)
                self.dmsg('htk_on_debug_info', self._trn.msg('htk_app_running_with_pid', pid), self.fromhere())
                self.dmsg('htk_on_debug_info', self._trn.msg('htk_app_stop_request_soft'), self.fromhere())
                try:                                    
                    os.kill(int(pid), signal.SIGTERM)
                    try:                        
                        while(True):
                            os.kill(int(pid), 0)
                            sys.stdout.write('.')
                            sys.stdout.flush()
                            time.sleep(0.5)
                    except:
                        print('.')
                        self.dmsg('htk_on_debug_info', self._trn.msg('htk_app_stopped'), self.fromhere())
                except:                    
                    self.dmsg('htk_on_debug_info', self._trn.msg('htk_app_not_running_except'), self.fromhere())
            except:
                self.dmsg('htk_on_debug_info', self._trn.msg('htk_app_not_running_with_pid', pid), self.fromhere())
        else:
            self.dmsg('htk_on_debug_info', self._trn.msg('htk_app_not_running'), self.fromhere())
    
    def _init_message_router(self):
        """Method initializes message router

        Args:
           none
        
        Returns:            
           void
           
        """ 
                
        self._msg_router = messagerouter.MessageRouter(self._msg_router_id)        
        self.dmsg('htk_on_debug_info', self._trn.msg('htk_msg_router_init_ok', self._msg_router_id), self.fromhere())
        
    def _list_extensions(self):  
        """Method prints extension list

        Args:
           none
        
        Returns:            
           void
           
        """ 
                      
        for ext_name in self._ext:                        
            print("%s: %s" % (ext_name, self._ext[ext_name].get_ext_info())) 
            

 