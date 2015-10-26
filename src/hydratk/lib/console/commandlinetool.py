"""This code is a part of Hydra Toolkit library

.. module:: commandlinetool
   :platform: Unix
   :synopsis: A useful module for commandline input parameters handling.
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
import sys, getopt
import pprint
from hydratk.lib.array import multidict
from hydratk.lib.number import conversion
from hydratk.lib.number.conversion import int2bool
from hydratk.lib.translation.translator import Translator
from locale import str

HS = chr(27)+chr(91)+"1m"
US = chr(27)+chr(91)+"4m"
EOS  = chr(27)+chr(91)+"0m"

def rprint(data):
        sys.stdout.write(data)
        sys.stdout.flush()
        
class CommandlineTool():
    __title      = ''
    __cp_string  = ''
    __commands   = []
    __long_opt   = {}
    __short_opt  = ''
    __cmd_text   = {}
    __opt_text   = {}
    __trn = None        
         
    @staticmethod
    def set_translator(translator):                     
        if isinstance(translator, Translator):            
            CommandlineTool.__trn = translator
        else:
            raise ValueError('translator must be a valid instance of hydratk.lib.translation.translator.Translator class')
        
    @staticmethod
    def set_possible_commands(commands):
        """Commands setter method
        
          :param commands: Possible commands to use
          :type commands: list
          :returns: void
        .. sectionauthor:: Petr Czaderna <pc@headz.cz>
        """        
        CommandlineTool.__commands = commands
        
    @staticmethod    
    def set_possible_options(short_opt, long_opt):
        """Options setter method
        
          :param short_opt: Possible short options to use (getopt format)
          :type short_opt: str
          :param long_opt: Possible long options to use (getopt format)
          :type long_opt: list
          :returns: void
        .. sectionauthor:: Petr Czaderna <pc@headz.cz>
        """         
        CommandlineTool.__short_opt = short_opt
        CommandlineTool.__long_opt = long_opt
    
    @staticmethod
    def set_help(title, cp_string, cmd_text, opt_text):        
        """Method creates and returns a formated help text
           :param title: Title text
           :type title: str
           :param cp_string: Copyright string
           :type cp_string: str
           :param cmd_text: Text description for specified commands, format is ['command' : 'description']
           :type cmd_text: dict
           :param opt_text: Text description for specified options, format is ['short_opt', 'long_opt' : 'description']
           :type opt_text: dict
           :returns: void
        .. sectionauthor:: Petr Czaderna <pc@headz.cz>
        """
        CommandlineTool.__title = title
        CommandlineTool.__cp_string = cp_string
        CommandlineTool.__cmd_text = cmd_text
        CommandlineTool.__opt_text = opt_text    
    
        
    @staticmethod    
    def print_help():        
        print(CommandlineTool.create_help())
    
    @staticmethod  
    def get_command_options_desc(command):
        """Method creates and returns a formated help text
   
           :returns string help text
        .. sectionauthor Petr Czaderna <pc@headz.cz>
        """                                     
        result = []
        command.replace(' ','')
        command.replace('{h}','')
        command.replace('{u}','')
        command.replace('{e}','')
       
        optlist = list(CommandlineTool.__opt_text.keys())
        optlist.sort()
        for opt in optlist:
            desc = CommandlineTool.__opt_text[opt]
                                       
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
   
           :return string command or false if no valid command was used
        .. sectionauthor Petr Czaderna <pc@headz.cz>
        """
        result = False
        for cmd in sys.argv:
            if cmd in CommandlineTool.__commands:
                result = cmd  
            
        return result
      
    @staticmethod
    def get_input_options():
        """Method returns passed action command parameter
   
           :returns result dictionary with short and long input options
        .. sectionauthor Petr Czaderna <pc@headz.cz>
        """
        result = {}
        try:            
            result['options'], result['remaining'] = getopt.getopt(sys.argv[1:], CommandlineTool.__short_opt, CommandlineTool.__long_opt)                
        except getopt.GetoptError as err:            
            raise err          
        return result
    
    @staticmethod
    def get_input_option(opt):
        options = CommandlineTool.get_input_options()
        result = False
        if options != False:
            for opt_name, opt_value in options['options']:
                if opt_name == opt:
                    result = opt_value if opt_value != '' else True
                    break
        return result
                
    @staticmethod
    def create_help():
        import pprint
        """Method creates and returns a formated help text
   
           :returns result help text
        .. sectionauthor Petr Czaderna <pc@headz.cz>
        """

        result = ''
        result += CommandlineTool.__title + "\n"
        result +=  CommandlineTool.__cp_string + "\n"
        have_options = ' [options..]' if len(CommandlineTool.__short_opt) > 0 or len(CommandlineTool.__long_opt) > 1 else ''
        have_commands = ' <command>' if len(CommandlineTool.__commands) > 0 else ''
        result += "Syntax: "+sys.argv[0]+have_options+have_commands+"\n\n" if CommandlineTool.__trn == None else CommandlineTool.__trn.msg('htk_help_syntax',sys.argv[0]) + "\n\n"
        if (have_commands):
            result += "Commands:\n" if CommandlineTool.__trn == None else CommandlineTool.__trn.msg('htk_help_commands') + "\n" 
            if (len(CommandlineTool.__cmd_text) > 0):
                cmdlist = list(CommandlineTool.__cmd_text.keys())
                cmdlist.sort()                              
                for cmd in cmdlist:                    
                    desc = CommandlineTool.__cmd_text[cmd] 
                    desc = desc if type(desc).__name__ == 'str' else 'undefined'                                                                                          
                    result += "   {h}"+cmd+"{e} - "+desc+"\n"                                            
                    cmd_options = CommandlineTool.get_command_options_desc(cmd)
                                                     
                    if len(cmd_options) > 0:
                        #pprint.pprint(cmd_options) 
                        result += "      Options:\n" if CommandlineTool.__trn == None else "      " + CommandlineTool.__trn.msg('htk_help_options') + "\n"                        
                        for cmd_opt in cmd_options:                            
                            result += "         "+cmd_opt+"\n"
            
                        result += "\n"                        
            else: #no text description
                for cmd in CommandlineTool.__commands:
                    result += "   "+cmd+"\n"
                    cmd_options = CommandlineTool.get_command_options_desc(cmd)
                    if len(cmd_options) > 0:
                        result = "      Options:\n" if CommandlineTool.__trn == None else "      " + CommandlineTool.__trn.msg('htk_help_options') + "\n"
                        for cmd_opt in cmd_options:
                            result += "         "+cmd_opt+"\n"            
                        result += "\n"

        if (have_options):
            result += "\nGlobal Options:\n" if CommandlineTool.__trn == None else "\n" + CommandlineTool.__trn.msg('htk_help_glob_options') + "\n"            
            if len(CommandlineTool.__opt_text) > 0:
                optlist = list(CommandlineTool.__opt_text.keys())
                optlist.sort()
                for opt in optlist:
                    desc = CommandlineTool.__opt_text[opt]                                                                                      
                    if (type(desc) is not dict):
                        if desc != '':                            
                            result += "   "+opt+" - "+desc+"\n"
          
                        else: #no text description
                            for opt in CommandlineTool.__short_opt:
                                have_param = int2bool(opt.find(':'))
                                opt = opt.replace(':','')
                                opt_param = '' if have_param == False else ' <param>'
                                result = result + "   "+opt+"\n"
        
      
    
        #apply decorations    
        result = CommandlineTool.parse_shell_text(result)
        return result

    @staticmethod 
    def parse_shell_text(result):
        result = result.replace('{h}', HS)
        result = result.replace('{u}', US)
        result = result.replace('{e}', EOS)
        return result