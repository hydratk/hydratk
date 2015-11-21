# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit

.. module:: core.corehead
   :platform: Unix
   :synopsis: HydraTK core module
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import os
import sys
import signal
import yaml
import getopt
import multiprocessing
import importlib
import imp
import traceback
import pprint
import setproctitle
import time
import zmq

PYTHON_MAJOR_VERSION = sys.version_info[0]

if PYTHON_MAJOR_VERSION == 2:
    import ConfigParser as configparser    
    
if PYTHON_MAJOR_VERSION == 3:    
    import configparser     

import re    
from hydratk.core import const
from hydratk.core import hsignal
from hydratk.core import commands
from hydratk.core import message
from hydratk.core.eventhandler import EventHandler
from hydratk.core import event
from hydratk.core.debugger import Debugger
from hydratk.core import messagerouter
from hydratk.lib.profiling.profiler import Profiler
from hydratk.lib.console.commandlinetool import CommandlineTool
from hydratk.lib.array import multidict
from hydratk.lib.exceptions.inputerror import InputError
import hydratk.core.dbconfig as dbconfig

class CoreHead(EventHandler, Debugger, Profiler):
    """Class CoreHead extends from EventHandler, Debugger and Profiler           
    """
    _runlevel         = const.RUNLEVEL_SHUTDOWN
    _config           = None   
    _language         = const.DEFAULT_LANGUAGE 
    _config_file      = const.CONFIG_FILE
    _ext_confd        = const.EXT_CONFIG_DIR
    _use_extensions   = True
    '''Extensions'''
    _ext              = {} 
    _default_command  = 'help'    
    _command          = None     
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
    

    def _bootstrap(self):                
        if self._runlevel == const.RUNLEVEL_BASEINIT:
            self.run_fn_hook('h_runlevel_config')            
            if self._runlevel == const.RUNLEVEL_CONFIG:
                self.run_fn_hook('h_runlevel_extensions')
                if self._runlevel == const.RUNLEVEL_EXTENSIONS:
                    self.run_fn_hook('h_runlevel_cli')
                    if self._runlevel == const.RUNLEVEL_CLI:
                        self.run_fn_hook('h_runlevel_appl')            
        else:
            pass #already running
        
        return True #required by fn_hook
        
    def _create_config_db(self):
        result = False
        force_cmd = True if CommandlineTool.get_input_option('-f') or  CommandlineTool.get_input_option('--force') == True else False
        db_file_param = CommandlineTool.get_input_option('--config-db-file')
        cfg_db_file = self._config['System']['DBConfig']['db_file']
        if db_file_param not in (True,False) or cfg_db_file != '':
            create_db_file = db_file_param if db_file_param not in (True,False) else cfg_db_file
            dir_name = os.path.dirname(create_db_file)   
            if os.access(dir_name, os.W_OK):
                if os.path.isfile(create_db_file) == False: 
                    self.dmsg('htk_on_debug_info', self._trn.msg('htk_create_cfg_db', create_db_file), self.fromhere())
                    self._write_config_db(create_db_file)
                else:
                    if force_cmd == True:
                        self.dmsg('htk_on_debug_info', self._trn.msg('htk_remove_cfg_db'), self.fromhere())
                        os.remove(create_db_file)
                        self._write_config_db(create_db_file)
                    else:
                        self.dmsg('htk_on_debug_info', self._trn.msg('htk_cfg_db_exists'), self.fromhere())   
            else:
                self.dmsg('htk_on_error', self._trn.msg('htk_create_cfg_db_error', create_db_file), self.fromhere())
                print(os.access(create_db_file, os.W_OK))
        
        else:
            self.dmsg('htk_on_error', self._trn.msg('htk_cfg_db_not_spec'), self.fromhere())
        
        return result    
    
    def _c_observer(self):
        setproctitle.setproctitle('hydra/c_observer')
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
            cmsgq_transport_type = int(self._config['Core']['MessageService']['transport_type'])            
            if (cmsgq_transport_type != ''):
                options = {}
                if cmsgq_transport_type in(messagerouter.SERVICE_TRANSPORT_TYPE_ZMQ_IPC, messagerouter.SERVICE_TRANSPORT_TYPE_ZMQ_TCP):
                    cmsgq_address = self._config['Core']['MessageService']['address'] 
                    options = {                                                      
                           'address' : cmsgq_address                  
                    }
                try:
                    self._msg_router.register_service(self._core_msg_service_id, cmsgq_transport_type, options)
                    self.dmsg('htk_on_debug_info', self._trn.msg('htk_core_msg_service_add_ok', core_msg_service_id), self.fromhere())
                    self._observer_status = const.CORE_THREAD_WORK
                    current = multiprocessing.current_process()
                    current.status = const.CORE_THREAD_WORK
                    options = {                                                                                     
                           'socket_type' : zmq.PULL                                              
                    }
                    try:
                        current.msgq = self._msg_router.get_queue(self._core_msg_service_id, messagerouter.MESSAGE_QUEUE_ACTION_BIND, options)                    
                        self.dmsg('htk_on_debug_info', self._trn.msg('htk_core_msgq_init_ok', self._msg_router.get_service_address(self._core_msg_service_id)), self.fromhere())
                    except zmq.ZMQBindError as desc:
                        pass 
                    ''' TODO process exceptions '''
                    
                    self.dmsg('htk_on_debug_info', self._trn.msg('htk_observer_init'), self.fromhere())
                    
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
                    self.init_core_threads()
                    self._reg_self_signal_hooks()
                    next_cw_activity_check = time.time() + const.CORE_THREAD_ACTIVITY_CHECK_TIME                            
                    while (current.status > const.CORE_THREAD_ALIVE and self._observer_status >= const.CORE_THREAD_ALIVE):
                        if (time.time() >= next_cw_activity_check):
                            self._check_cw_activity()
                            next_cw_activity_check = time.time() + const.CORE_THREAD_ACTIVITY_CHECK_TIME 
                        
                        self.dmsg('htk_on_debug_info', self._trn.msg('htk_observer_sleep'), self.fromhere(), 5)            
                        time.sleep(const.CORE_OBSERVER_SLEEP_TIME)
                        self.dmsg('htk_on_debug_info', self._trn.msg('htk_observer_awake'), self.fromhere(), 5)                                    
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
        
    def c_worker(self, i, status, action_status, pipe_conn, is_alive_check): 
        setproctitle.setproctitle('hydra/core:' + str(i))
        '''updating signal hooks to work properly'''        
        self._reg_self_signal_hooks() 
                                            
        current = multiprocessing.current_process()                        
        options = {
                'socket_type' : zmq.PULL,
        }        
        current.pipe_conn = pipe_conn
        current.status = status     
        current.action_status = action_status
        current.is_alive_check = is_alive_check          
        current.msgq = self._msg_router.get_queue(self._core_msg_service_id, messagerouter.MESSAGE_QUEUE_ACTION_CONNECT, options)        
        self.dmsg('htk_on_debug_info', self._trn.msg('htk_core_msgq_connect_ok', self._msg_router.get_service_address(self._core_msg_service_id)), self.fromhere())
                    
        self.dmsg('htk_on_debug_info', self._trn.msg('htk_cworker_init'), self.fromhere())        
        while (current.status.value > const.CORE_THREAD_ALIVE):
            current.is_alive_check.value = time.time()                       
            if (current.status.value == const.CORE_THREAD_WORK):                                
                thr_intq_sleep = self._check_core_msg_queue()
                if (thr_intq_sleep):                    
                    self.dmsg('htk_on_debug_info', self._trn.msg('htk_cthread_sleep'), self.fromhere(), 5)
                    time.sleep(1.0)
                    self.dmsg('htk_on_debug_info', self._trn.msg('htk_cthread_awake'), self.fromhere(), 5)
            elif (current.status.value == const.CORE_THREAD_WAIT):
                self._check_cw_priv_msg(current)
                self.dmsg('htk_on_debug_info', self._trn.msg('htk_cthread_sleep'), self.fromhere(), 5)
                time.sleep(1)
                self.dmsg('htk_on_debug_info', self._trn.msg('htk_cthread_awake'), self.fromhere(), 5)
           
        self.dmsg('htk_on_debug_info', self._trn.msg('htk_cworker_term'), self.fromhere())       
    
    def _check_co_privmsg(self):
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
        db = dbconfig.DBConfig(db_file)
        db.connect()
        self.dmsg('htk_on_debug_info', self._trn.msg('htk_write_cfg_db'), self.fromhere())
        db.writedb(self._config)             
        
    def _dopoll(self, poller):
        while True:
            try:
                return poller.poll()
            except Exception as e: #except IOError as e:
                if e.errno != errno.EINTR:
                    raise e
                
      
    
    def _check_core_msg_queue(self):
        current = multiprocessing.current_process()
        mq = current.msgq
        q_empty = False
        try:
            current.action_status.value = const.CORE_THREAD_ACTION_PROCESS_MSG
            msg = mq.recv(zmq.NOBLOCK)
            self._process_msg(msg)
        except zmq.ZMQError:
            q_empty = True
        current.action_status.value = const.CORE_THREAD_ACTION_NONE                                                                                                      
        return q_empty      
    
    def _check_cw_privmsg(self):
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
            tb = traceback.format_exc()
            pprint.pprint(tb)        
    
    def _check_cw_activity(self):
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
        if (self._command != None):                                
            if (self._command in self._cmd_hooks):                               
                self._run_command_hooks(self._command)
                       
        else:
            self._run_command_hooks(self._default_command)
    
    def _load_db_config(self):        
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
                  
            self._config[grp][obj][itmk] = itmv
    
    
    def _process_extension_configs(self):
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
        for gk, gv in config.items():
            for ok, ov in gv.items():
                for kk, kv in ov.items():                    
                    if gk != '' and ok != '' and kk != '':
                        if gk not in self._config: self._config[gk] = {}
                        if ok not in self._config[gk]: self._config[gk][ok] = {}
                        self._config[gk][ok][kk] = kv                                                                         
                                        
    def _load_base_config(self):                       
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
        from hydratk.translation.core import info
        
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
                self._debug_level = debug_level if debug_level > 0 else 1                                              
                self.dmsg('htk_on_debug_info', self._trn.msg('htk_debug_level_set', debug_level), self.fromhere())                
            except Exception as exc:
                pprint.pprint(exc)
                self.dmsg('htk_on_warning', self._trn.msg('htk_conf_opt_missing', 'Debug', 'level'), self.fromhere())   
            
        try:
            if (not self.check_language()):                
                language = self._config['System']['Language']['id']
                self._language = language if language in info.languages else const.DEFAULT_LANGUAGE                                            
            self.dmsg('htk_on_debug_info', self._trn.msg('htk_lang_set', info.language_desc[self._language]), self.fromhere())
            self._trn.set_language(self._language)
            self._import_global_messages()                
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
        ext_module = ext_cfg['module']
        ext_base_path = ext_cfg['package']                
        ext_full_path = ext_base_path + '.' + ext_module 
        
        if ext_name not in self._ext:                     
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
                tb = traceback.format_exc(e)
                pprint.pprint(tb) 
                pprint.pprint(sys.path)
        else:
            raise Exception(self._trn.msg('htk_duplicate_extension', ext_name))         

    def _extension_module_import(self, ext_full_path):
        mod = __import__(ext_full_path)
        components = ext_full_path.split('.')
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod
    
    def _load_module_from_file(self, filepath):
        import pprint
        pprint.pprint(sys.path)
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
        msg_package  = ext_path + '.translation.'+self._language+'.messages'
        help_package = ext_path + '.translation.'+self._language+'.help'
        try:
            self.dmsg('htk_on_debug_info', self._trn.msg('htk_load_ext_msg', self._language, str(msg_package)), self.fromhere())             
            lang = importlib.import_module(msg_package)
            self._trn.add_msg(lang.msg)            
            self.dmsg('htk_on_debug_info', self._trn.msg('htk_load_ext_msg_success', self._language), self.fromhere())            
        except ImportError as e:
            self.dmsg('htk_on_error', self._trn.msg('htk_load_ext_msg_failed', self._language, str(e)), self.fromhere())                                    
        try:            
            self.dmsg('htk_on_debug_info', self._trn.msg('htk_load_ext_help', self._language, str(help_package)), self.fromhere())            
            help_msg = importlib.import_module(help_package)
            self._trn.add_help(help_msg)            
        except ImportError as e:
            self.dmsg('htk_on_error', self._trn.msg('htk_load_ext_help_failed', self._language, str(e)), self.fromhere())   
            
    def _import_package_messages(self, import_package, msg_package):
        msg_package  = msg_package+'.'+self._language+'.messages'
        
        try:            
            self.dmsg('htk_on_debug_info', self._trn.msg('htk_load_package_msg', import_package, self._language), self.fromhere())                          
            lang = importlib.import_module(msg_package)
            self._trn.add_msg(lang.msg)
            self.dmsg('htk_on_debug_info', self._trn.msg('htk_load_package_msg_success', import_package, self._language), self.fromhere())                        
        except ImportError as e:
            self.dmsg('htk_on_error', self._trn.msg('htk_load_package_msg_failed', import_package, self._language, str(e)), self.fromhere())  
        
        
    def _import_global_messages(self):
        msg_package  = 'hydratk.translation.core.'+self._language+'.messages'
        help_package = 'hydratk.translation.core.'+self._language+'.help'
        try:            
            self.dmsg('htk_on_debug_info', self._trn.msg('htk_load_global_msg', self._language, msg_package), self.fromhere())                          
            self._trn.msg_mod = importlib.import_module(msg_package)
            self._trn.register_messages(self._trn.msg_mod.msg)
            self.dmsg('htk_on_debug_info', self._trn.msg('htk_load_global_msg_success', self._language), self.fromhere())                        
        except ImportError as e:
            self.dmsg('htk_on_error', self._trn.msg('htk_load_global_msg_failed', self._language, str(e)), self.fromhere())             
        try:
            self.dmsg('htk_on_debug_info', self._trn.msg('htk_load_global_help', self._language, str(help_package)), self.fromhere())                        
            self._trn.set_help_mod(importlib.import_module(help_package))                                   
            self.dmsg('htk_on_debug_info', self._trn.msg('htk_load_global_help_success', self._language), self.fromhere())            
        except ImportError as e:
            self.dmsg('htk_on_error', self._trn.msg('htk_load_global_help_failed', self._language, str(e)), self.fromhere())    
            
    def _reg_self_command_hooks(self):        
        hooks = [
                {'command' : 'start', 'callback' : self._start_app },
                {'command' : 'stop', 'callback' : self._stop_app_command },
                {'command' : 'help', 'callback' : CommandlineTool.print_help },
                {'command' : 'list-extensions', 'callback' : self._list_extensions },
                {'command' : 'create-config-db', 'callback' : self._create_config_db },
                {'command' : 'create-ext-skel', 'callback' : self.create_ext_skel },
                {'command' : 'create-lib-skel', 'callback' : self.create_lib_skel },
            ]
        self.register_command_hook(hooks)  
                                    
    def _runlevel_config(self):
        self._runlevel = const.RUNLEVEL_CONFIG        
        self._load_base_config()
        self._process_extension_configs()
        if self._config['System']['DBConfig']['enabled'] == 1:
            if os.path.isfile(self._config['System']['DBConfig']['db_file']) and os.path.getsize(self._config['System']['DBConfig']['db_file']) > 256:
                self._load_db_config()        
        self._apply_config()
        return True #required by fn_hook
        
    
    def _runlevel_extensions(self):
        self._runlevel = const.RUNLEVEL_EXTENSIONS
        self._load_extensions()
        return True #required by fn_hook
    
    def _runlevel_cli(self):
        self._runlevel = const.RUNLEVEL_CLI
        self._set_default_cli_params()
        self._parse_cli_args()
        return True #required by fn_hook
    
    def _runlevel_appl(self):
        self._runlevel = const.RUNLEVEL_APPL
        if (self.have_command_action()):
            self._do_command_action()
        return True #required by fn_hook
    
    def _run_command_option_hooks(self, command_opt, command_opt_value):
        """Method is processing specified command option callbacks.
           
           This method runs automatically in runlevel cli, if there're specified options. 
        
        Args:
           command_opt (str): command option
        
        Returns:            
           int  - number of processed callbacks
                   
           
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
           int  - number of processed callbacks                  
           
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
        CommandlineTool.set_translator(self._trn)
        
        '''Define commands'''                            
        CommandlineTool.set_possible_commands(commands.commands)  
                      
        '''Define options'''                                               
        CommandlineTool.set_possible_options(commands.getopt_short_opts, commands.getopt_long_opts)        

        '''Set help text'''
        help_title = '{h}' + const.APP_NAME + ' v' + const.APP_VERSION + '{e}'
        cp_string = '{u}' + const.CP_STRING + '{e}'
        cmd_text = {}
        for cmd in commands.commands: 
            if cmd in self._trn.help_mod.help_cmd:
                cmd_text[cmd] = self._trn.help_mod.help_cmd[cmd]
            else: self.dmsg('htk_on_warning', self._trn.msg('htk_help_cmd_def_missing', cmd, self._language), self.fromhere())                            
        opt_text = {}
        for opt in commands.long_opts:
            if opt in self._trn.help_mod.help_opt:
                opt_text.update(self._trn.help_mod.help_opt[opt])
            else: self.dmsg('htk_on_warning', self._trn.msg('htk_option_def_missing', opt, self._language), self.fromhere())   
                                               
        CommandlineTool.set_help(help_title, cp_string, cmd_text, opt_text)            
    
    def _set_pid_file(self, pid_file):
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
        os.kill(pid, signal.SIGPIPE)
        
    def _send_ping(self, thr):
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
        current = multiprocessing.current_process() 
        setproctitle.setproctitle('hydra/srv:' + current.service_name)
        self._reg_service_signal_hooks()
        cb(service_status, parent_conn)
        
    def _sig_retriever(self, signum, frame):
        self.fire_event(event.Event('htk_on_signal', signum))
        if signum in hsignal.sig2event:
            self.fire_event(event.Event(hsignal.sig2event[signum]))
    
    def _reg_service_signal_hooks(self):        
        signal.signal(signal.SIGTERM, self._sig_retriever)
        signal.signal(signal.SIGINT, self._sig_retriever)
        signal.signal(signal.SIGPIPE, self._sig_retriever)        
        hook = [{'event' : 'htk_on_signal', 'callback' : self._ec_sig_handler, 'unpack_args' : True}]        
        self.register_event_hook(hook)
    
    
    def _reg_self_fn_hooks(self):
        hook = [
                {'fn_id' : 'h_bootstrap', 'callback' : self._bootstrap },
                {'fn_id' : 'h_runlevel_config', 'callback' : self._runlevel_config },
                {'fn_id' : 'h_runlevel_extensions', 'callback' : self._runlevel_extensions },
                {'fn_id' : 'h_runlevel_cli', 'callback' : self._runlevel_cli },
                {'fn_id' : 'h_runlevel_appl', 'callback' : self._runlevel_appl }
            ]
        self.register_fn_hook(hook)
    
    
    def _reg_self_event_hooks(self):
        
        hook = [
                {'event' : 'htk_on_error', 'callback' : self._eh_htk_on_error, 'unpack_args' : True},        
                {'event' : 'htk_on_warning', 'callback' : self._eh_htk_on_warning, 'unpack_args' : True}, 
                {'event' : 'htk_on_debug_info', 'callback' : self._eh_htk_on_debug_info, 'unpack_args' : True},
                {'event' : 'htk_on_got_cmd_options', 'callback' : self._eh_htk_on_got_cmd_options },
                {'event' : 'htk_on_extension_error', 'callback' : self._eh_htk_on_extension_error, 'unpack_args' : True},
                {'event' : 'htk_on_extension_warning', 'callback' : self._eh_htk_on_extension_warning, 'unpack_args' : True},
                {'event' : 'htk_on_uncaught_exception', 'callback' : self._eh_htk_on_exception, 'unpack_args' : True}
            ]
                      
        self.register_event_hook(hook)
                            
    def _parse_cli_args(self):        
        if (len(sys.argv) > 1):
            command = CommandlineTool.get_input_command()
            try:                
                options = CommandlineTool.get_input_options()
            except getopt.GetoptError as err:
                options = False
                self.dmsg('htk_on_error', self._trn.msg('htk_unrecognized_opt', err.opt), self.fromhere())
                
            
            if command == False:
                self.dmsg('htk_on_warning', self._trn.msg('htk_undetected_cmd'), self.fromhere())
                self._command = self._default_command                
            else:                                
                self._command = command
                        
            if options != False:
                            
                for opt_name, opt_value in options['options']:
                    self._run_command_option_hooks(opt_name, opt_value)                    
                                        
                    if opt_name == '-h' or opt_name == '--help':
                        CommandlineTool.print_help()
                        break
                                        
                        
        else:
            self._command = self._default_command              
        self.fire_event(event.Event('htk_on_cmd_options'))  
     
    def _process_cw_msg(self, msg, thr):
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
    
    def _process_msg(self, msg):        
        self.fire_event(event.Event('h_msg_recv', msg))        
    
    def _response_ping(self, msg):
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
        # pprint.pprint(msg)        
        self.fire_event(event.Event('h_privmsg_recv', msg))
        if msg['type'] == message.REQUEST:
            if msg['command'] == message.PING:
                self._response_ping(msg)
    
                    
    def _remove_pid_file(self, pid_file):
        result = False
        if os.path.exists(pid_file) and os.path.isfile(pid_file):
            result = os.unlink(pid_file)
        return result
    
    def _reg_self_signal_hooks(self):        
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
        self.dmsg('htk_on_debug_info', self._trn.msg('htk_app_start'), self.fromhere())
        cevent = event.Event('htk_on_start')
        self.fire_event(cevent)
        if cevent.will_run_default():
            self._init_message_router()                
            self._c_observer()
    
            
    def _stop_app(self, force_exit=False):
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
        self._msg_router = messagerouter.MessageRouter(self._msg_router_id)        
        self.dmsg('htk_on_debug_info', self._trn.msg('htk_msg_router_init_ok', self._msg_router_id), self.fromhere())
        
    def _list_extensions(self):        
        for ext_name in self._ext:                        
            print("%s: %s" % (ext_name, self._ext[ext_name].get_ext_info())) 