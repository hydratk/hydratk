# -*- coding: utf-8 -*-
"""Useful module for commandline input parameters handling

.. module:: lib.console.commandlinetool
   :platform: Unix
   :synopsis: Useful module for commandline input parameters handling
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import sys
from hydratk.lib.number.conversion import int2bool
from hydratk.lib.translation.translator import Translator
from hydratk.lib.console import cmdoptparser

HS = chr(27)+chr(91)+"1m"
US = chr(27)+chr(91)+"4m"
EOS  = chr(27)+chr(91)+"0m"

def rprint(data):
        sys.stdout.write(data)
        sys.stdout.flush()
        
class CommandlineTool():
    """Class CommandLineTool
    """
    
    _title      = ''
    _cp_string  = ''
    _commands   = []
    _long_opt   = {}
    _short_opt  = []
    _cmd_text   = {}
    _opt_text   = {}
    _trn        = None
    _parser     = None        
         
    @staticmethod
    def set_translator(translator):      
        """Method sets translator
        
        Args:   
           translator (obj): Translator object
           
        Returns:
           void
           
        Raises:
           error: ValueError  
                
        """  
                               
        if isinstance(translator, Translator):            
            CommandlineTool._trn = translator
        else:
            raise ValueError('translator must be a valid instance of hydratk.lib.translation.translator.Translator class')
        
    @staticmethod
    def set_possible_commands(commands):
        """Commands setter method
        
        Args:
           commands (list): Possible commands to use
           
        Returns:
           void
                              
        """        
        
        CommandlineTool._commands = commands
        
    @staticmethod    
    def set_possible_options(short_opt, long_opt):
        """Options setter method
        
        Args:
           short_opt (list): Possible short options to use (getopt format)
           long_opt (list): Possible long options to use (getopt format)
           
        Returns:
           void
                            
        """    
            
        CommandlineTool._short_opt = short_opt
        CommandlineTool._long_opt = long_opt
    
    @staticmethod
    def set_help(title, cp_string, cmd_text, opt_text):        
        """Method creates and returns a formated help text
        
        Args:
           title (str): Title text
           cp_string (str): Copyright string
           cmd_text (dict): Text description for specified commands, format is ['command' : 'description']
           opt_text (dict): Text description for specified options, format is ['short_opt', 'long_opt' : 'description']
           
        Returns:
           void
               
        """
        CommandlineTool._title = title
        CommandlineTool._cp_string = cp_string
        CommandlineTool._cmd_text = cmd_text
        CommandlineTool._opt_text = opt_text    
    
    
    @staticmethod
    def print_short_help():
        """Method prints short help
        
        Args:   
           none
           
        Returns:
           void   
                
        """  
                
        print(CommandlineTool.create_short_help())
        
    @staticmethod    
    def print_help():  
        """Method prints long help
        
        Args:
           none   
           
        Returns:
           void   
                
        """ 
                      
        print(CommandlineTool.create_help())
    
    @staticmethod  
    def get_command_options_desc(command):
        """Method creates and returns a formated help text
        
        Args:
           command (str): command text
   
        Returns:
           str: help text
        
        """   
                                          
        result = []
        command.replace(' ','')
        command.replace('{h}','')
        command.replace('{u}','')
        command.replace('{e}','')
       
        optlist = list(CommandlineTool._opt_text.keys())       
        optlist.sort()
        for opt in optlist:
            desc = CommandlineTool._opt_text[opt]
                                       
            if type(desc) is dict:          
                if type(desc['commands']) is tuple:                                    
                    for cmd in desc['commands']:                                          
                        if (command == cmd):
                            result.append(opt + ' - ' + desc['description'])
                else:                    
                    if (command == desc['commands']):
                            result.append(opt + ' - ' + desc['description'])
                                                                                                 
        return result
    
    @staticmethod
    def get_input_command():
        """Method returns passed action command parameter
        
        Args:
           none
   
        Returns:
           str: string command 
           bool: false if no valid command was used
        
        """
        
        result = False
        for cmd in sys.argv:
            if cmd in CommandlineTool._commands:
                result = cmd  
            
        return result
      
    @staticmethod
    def get_input_options(opt_dict):
        """Method returns passed action command parameter
        
        Args:
           opt_dict (dict): options
   
        Returns:
           dict: result dictionary with short and long input options
           
        Raises:
           error: CmdOptParserError
        
        """
        
        result = {}
        try:            
            CommandlineTool._parser = cmdoptparser.CmdOptParser()
            for option, opt_set in opt_dict.items():
                d_option = opt_set['d_opt'] if opt_set['d_opt'] is not None else option                
                CommandlineTool._parser.add_opt(option, d_option, opt_set['has_value'], opt_set['allow_multiple'])            
            result['options'], result['remaining'] = CommandlineTool._parser.parse()               
        except cmdoptparser.CmdOptParserError as err:            
            raise err          
        return result
    
    @staticmethod
    def get_input_option(opt):
        """Method gets option value
        
        Args:   
           opt (str): option
           
        Returns:
           bool: result   
           
        Raises:
           error: CmdOptParserError
                
        """ 
                
        if CommandlineTool._parser == None:
            raise cmdoptparser.CmdOptParserError('Commandline needs to be parsed first')       
        opt_value = CommandlineTool._parser.get_opt(opt)
        if opt_value is None:
            opt_value = False
        result = opt_value if opt_value != '' else True        
        return result
    
    @staticmethod
    def create_short_help():
        """Method creates short help text
        
        Args:   
           none
           
        Returns:
           str: help text
                
        """ 
                
        result = ''
        result += CommandlineTool._title + "\n"
        result +=  CommandlineTool._cp_string + "\n"
        have_options = ' [options..]' if len(CommandlineTool._short_opt) > 0 or len(CommandlineTool._long_opt) > 1 else ''
        have_commands = ' <command>' if len(CommandlineTool._commands) > 0 else ''
        cmd = (sys.argv[0]).split('/')[-1]
        result += "Syntax: "+sys.argv[0]+have_options+have_commands+"\n" if CommandlineTool._trn == None else CommandlineTool._trn.msg('htk_help_syntax',cmd) + "\n"        
        result += "For list of all available commands and options type {h}"+cmd+" help{e}" if CommandlineTool._trn == None else CommandlineTool._trn.msg('htk_help_on_help',cmd)
        
        #apply decorations    
        result = CommandlineTool.parse_shell_text(result)
        return result
                    
    @staticmethod
    def create_help():        
        """Method creates and returns a formated help text
        
        Args:
           none
   
        Returns:
           str: result help text
           
        """
        
        import pprint
        result = ''
        result += CommandlineTool._title + "\n"
        result +=  CommandlineTool._cp_string + "\n"
        have_options = ' [options..]' if len(CommandlineTool._short_opt) > 0 or len(CommandlineTool._long_opt) > 1 else ''
        have_commands = ' <command>' if len(CommandlineTool._commands) > 0 else ''
        cmd = (sys.argv[0]).split('/')[-1]
        result += "Syntax: "+cmd+have_options+have_commands+"\n\n" if CommandlineTool._trn == None else CommandlineTool._trn.msg('htk_help_syntax',cmd) + "\n\n"
        if (have_commands):
            result += "Commands:\n" if CommandlineTool._trn == None else CommandlineTool._trn.msg('htk_help_commands') + "\n" 
            if (len(CommandlineTool._cmd_text) > 0):
                cmdlist = list(CommandlineTool._cmd_text.keys())
                cmdlist.sort()                              
                for cmd in cmdlist:                    
                    desc = CommandlineTool._cmd_text[cmd] 
                    desc = desc if type(desc).__name__ == 'str' else 'undefined'                                                                                          
                    result += "   {h}"+cmd+"{e} - "+desc+"\n"                                            
                    cmd_options = CommandlineTool.get_command_options_desc(cmd)
                                                     
                    if len(cmd_options) > 0:
                        #pprint.pprint(cmd_options) 
                        result += "      Options:\n" if CommandlineTool._trn == None else "      " + CommandlineTool._trn.msg('htk_help_options') + "\n"                        
                        for cmd_opt in cmd_options:                            
                            result += "         "+cmd_opt+"\n"
            
                        result += "\n"                        
            else: #no text description
                for cmd in CommandlineTool._commands:
                    result += "   "+cmd+"\n"
                    cmd_options = CommandlineTool.get_command_options_desc(cmd)
                    if len(cmd_options) > 0:
                        result = "      Options:\n" if CommandlineTool._trn == None else "      " + CommandlineTool._trn.msg('htk_help_options') + "\n"
                        for cmd_opt in cmd_options:
                            result += "         "+cmd_opt+"\n"            
                        result += "\n"

        if (have_options):                        
            if len(CommandlineTool._opt_text) > 0:                
                optlist = list(CommandlineTool._opt_text.keys())
                optlist.sort()
                glob_opt_result = ''
                for opt in optlist:
                    desc = CommandlineTool._opt_text[opt]                                                                                      
                    if (type(desc) is not dict):
                        if desc != '':                            
                            glob_opt_result += "   "+opt+" - "+desc+"\n"
          
                        else: #no text description
                            for opt in CommandlineTool._short_opt:
                                have_param = int2bool(opt.find(':'))
                                opt = opt.replace(':','')
                                opt_param = '' if have_param == False else ' <param>'
                                glob_opt_result += "   "+opt+"\n"
                if glob_opt_result != '':
                    result += "\nGlobal Options:\n" if CommandlineTool._trn == None else "\n" + CommandlineTool._trn.msg('htk_help_glob_options') + "\n"                    
                    result += glob_opt_result
      
    
        #apply decorations    
        result = CommandlineTool.parse_shell_text(result)
        return result

    @staticmethod 
    def parse_shell_text(result):
        """Method adds special characters for shell print
        
        Args:  
           result (str): text  
           
        Returns:
           str: shell text   
                
        """ 
                
        result = result.replace('{h}', HS)
        result = result.replace('{u}', US)
        result = result.replace('{e}', EOS)
        return result