from hydratk.core.masterhead import MasterHead
from hydratk.lib.console.commandlinetool import CommandlineTool 
import hydratk.core.const as const
import yodalib.hydratk.core.commandopt as commandopt

class TestHead(MasterHead):
    
    cli_cmdopt_profile = 'htk'
    options = {}
    
    def __init__(self):
        
        self._instance = super(TestHead, self).__new__(MasterHead)        
        self.reset()
        
        self._reg_self_fn_hooks()        
        self.run_fn_hook('h_bootstrap')
        
    def reset(self):
        
        self._runlevel         = const.RUNLEVEL_SHUTDOWN
        self._config           = None   
        self._language         = const.DEFAULT_LANGUAGE 
        self._config_file      = const.CONFIG_FILE
        self._ext_confd        = const.EXT_CONFIG_DIR
        self._use_extensions   = True
        '''Extensions'''
        self._ext              = {} 
        self._default_command  = 'short-help'
        self._help_title       = '{h}' + const.APP_NAME + ' v' + const.APP_VERSION + '{e}'
        self._cp_string        = '{u}' + const.CP_STRING + '{e}'   
        self._command          = None
        self._opt_profile      = 'htk'     
        self._cmd_option_hooks = {}
        self._event_hooks      = {}
        self._cmd_hooks        = {}
        self._fn_hooks         = {} 
        self._msg_router_id    = 'raptor01'    
        self._msg_router       = None  
        self._app_status       = None
        self._observer_status  = None
        '''Core thread pool'''
        self._thr              = [] 
        '''Translator instance'''
        self._trn              = None 
        self._pid_file         = None
        self._option           = {}
        self._option_param     = {}

        '''Application services pool'''    
        self._app_service      = []
        self._run_mode         = const.CORE_RUN_MODE_SINGLE_APP
    
        '''Function callbacks'''
        self._fn_cb            = {}
    
        '''Parallel processing'''
        self._fn_cb            = {}
        self._fn_cb_shared     = {}
        self._async_fn_tickets = {}
        self._cbm              = None  #Callback manager   
        self._async_fn         = {}
        self._async_fn_ex      = None  
        
    def clear_cmd(self):
        
        self._cmd_hooks = {}
        commandopt.cmd = {}  
        commandopt.long_opt = {}
        commandopt.short_opt = {}
        commandopt.opt = {}
        
    @staticmethod
    def get_input_option(opt):
        
        return TestHead.options[opt] if (opt in TestHead.options) else False  
    
    def pre_replace(self):
        
        self._old = CommandlineTool.get_input_option
        CommandlineTool.get_input_option = staticmethod(TestHead.get_input_option) 
        
    def post_replace(self): 
        
        CommandlineTool.get_input_option = staticmethod(self._old)               
        
    def match_cli_command(self, cmd, opt_group='htk'):
        
        if opt_group not in commandopt.cmd:
            commandopt.cmd[opt_group] = []
            
        if cmd != '': 
            if cmd not in commandopt.cmd[opt_group]:                
                commandopt.cmd[opt_group].append(cmd)                
                
            else:                
                raise ValueError(self._trn.msg('htk_cmd_registered', cmd))
        else:
            raise ValueError(self._trn.msg('htk_cmd_invalid', cmd))    
        
    def match_long_option(self, opt, value_expected=False, d_opt=None, allow_multiple=False, opt_group='htk'):
        
        if type(opt_group).__name__ == 'list':
            for optg in opt_group:
                if optg not in commandopt.long_opt:
                    commandopt.long_opt[optg] = []
                if opt not in commandopt.long_opt[optg]:
                    commandopt.long_opt[optg].append(opt)
                    optl = "--{0}".format(opt)
                    if optg not in commandopt.opt:
                        commandopt.opt[optg] = {}
                    commandopt.opt[optg][optl] = {
                                                    'd_opt'          : d_opt,
                                                    'has_value'      : value_expected,
                                                    'allow_multiple' : allow_multiple                           
                                                }
        elif type(opt_group).__name__ == 'str':
            if opt_group not in commandopt.long_opt:
                commandopt.long_opt[opt_group] = []
            if opt not in commandopt.long_opt[opt_group]:
                commandopt.long_opt[opt_group].append(opt)
                optl = "--{0}".format(opt)
                if opt_group not in commandopt.opt:
                    commandopt.opt[opt_group] = {}
                commandopt.opt[opt_group][optl] = {
                                                'd_opt'          : d_opt,
                                                'has_value'      : value_expected,
                                                'allow_multiple' : allow_multiple                           
                                            }
        
        else:
            raise TypeError('opt_group can be only of type list or str, got {0}'.format(type(opt_group).__name__))  
        
    def match_short_option(self, opt, value_expected=False, d_opt=None, allow_multiple=False, opt_group='htk'):
        
        if type(opt_group).__name__ == 'list':
            for optg in opt_group:
                if optg not in commandopt.short_opt:
                    commandopt.short_opt[optg] = ''
                if opt not in commandopt.short_opt[optg]:
                    commandopt.short_opt[optg] += opt
                    opts = "-{0}".format(opt)
                    if optg not in commandopt.opt:
                        commandopt.opt[optg] = {}
                    commandopt.opt[optg][opts] = {
                                                    'd_opt'          : d_opt,
                                                    'has_value'      : value_expected,
                                                    'allow_multiple' : allow_multiple                           
                                                }
        elif type(opt_group).__name__ == 'str':
            if opt_group not in commandopt.short_opt:
                commandopt.short_opt[opt_group] = ''
            if opt not in commandopt.short_opt[opt_group]:
                commandopt.short_opt[opt_group] += opt
                opts = "-{0}".format(opt)
                if opt_group not in commandopt.opt:
                    commandopt.opt[opt_group] = {}
                commandopt.opt[opt_group][opts] = {
                                                'd_opt'          : d_opt,
                                                'has_value'      : value_expected,
                                                'allow_multiple' : allow_multiple                           
                                            }
        
        else:
            raise TypeError('opt_group can be only of type list or str, got {0}'.format(type(opt_group).__name__))                       