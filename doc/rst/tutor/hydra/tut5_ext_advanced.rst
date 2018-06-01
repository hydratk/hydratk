.. _tutor_hydra_tut5_ext_advanced:

Tutorial 5: Advanced extension
==============================

This tutorial will show you how to create advanced extension.

Topic
^^^^^

Our extension will solve simple tasks from Physics - motion in mechanics, electromagnetic field.
Numeric schema is used to solve appropriate differential equations. The extension has command line
interface, user provides initial conditions and extension returns motion data including graphs.
The extension provides single mode (to solve one task) and parallel mode (to solve multiple tasks).

Skeleton
^^^^^^^^

First we create extension skeleton using htk command in interactive mode.

  .. code-block:: bash
  
     $ htk -i create-ext-skel
     
     ****************************************
     *   Extension skeleton create wizard   *
     ****************************************
     This wizard will create HydraTK extension development skeleton in following 6 steps
     Hit ENTER for default value, CTRL + C to exit
     1. Enter the directory, where the extension structure will be created
     [/root/hydratk]:.
     extension skeleton directory set to: .
     2. Enter the extension module name, must be one word short unique string
     [hobbit]:physolver
     extension module name set to: physolver
     3. Enter the extension description
     [This extension provides example functionality, how to develop HydraTK extensions]:Physics problems solver
     extension description set to: Physics problems solver
     4. Enter the extension author name
     [Bilbo Baggins]:Charlie Bowman
     extension author name set to: Charlie Bowman
     5. Enter the extension author email
     [bilbo@shire.com]:charlie.bowman@gmail.com
     extension author email set to: charlie.bowman@gmail.com
     6. Select extension usage and distribution license, currently supported are: BSD
     [BSD]:
     extension usage and distribution license set to: BSD
     Completed. 
     
Skeleton is created in directory ~/hydratk/hydratk-ext-physolver with following structure.
The files content is created from template, see tutorial 4 for more details.

  .. code-block:: bash
  
     /doc - documentation
       /physolver.1 - manual page
     /etc - configuration file
       /hydratk     
         /conf.d
           /hydratk-ext-physolver.conf
     /src - source code
       /hydratk
         /extensions
           /physolver - extension title
             bootstrapper.py - bootstrapper code
             physolver.py - extension code
             __init__.py             
             /translation - langtexts for Czech and English language
               /cs
                 help.py - command line help
                 __init__.py
                 messages.py - messages used in code
               /en
                 help.py
                 __init__.py
                 messages.py
               __init__.py
           __init__.py
         __init__.py
     LICENSE.txt - license file with template text
     MANIFEST.in - manifest file with template text
     README.rst - readme file with template text
     requirements.txt - requirements file with template text
     setup.cfg - setup configuration
     setup.py - setup script with template text
     
Installation
^^^^^^^^^^^^

First we will prepare installation script. 

The extension requires hydratk (dependency included automatically) and modules numpy, matplotlib to 
create graphs. Include the modules to requirements file (matplotlib is not supported for PyPy interpreter).

* requirements.txt

  .. code-block:: cfg
  
     hydratk>=0.4.0
     numpy>=1.12.1
     matplotlib>=2.0.0 ; platform_python_implementation != 'PyPy'
     
Now update setup.py, the changes are commented.

* setup.py

  .. code-block:: python
 
     # -*- coding: utf-8 -*-
     from setuptools import setup as st_setup
     from setuptools import find_packages as st_find_packages
     from sys import argv, version_info
     from platform import python_implementation
     import hydratk.lib.install.task as task
     import hydratk.lib.system.config as syscfg

     try:
        os_info = syscfg.get_supported_os()
     except Exception as exc:
        print(str(exc))
        exit(1)

     with open("README.rst", "r") as f:
        readme = f.read()
    
     classifiers = [
         "Development Status :: 3 - Alpha",
         "Environment :: Console",
         "Environment :: Other Environment",
         "Intended Audience :: Developers",
         "License :: Freely Distributable",
         "Operating System :: OS Independent",   
         "License :: OSI Approved :: BSD License",
         "Programming Language :: Python",    
         "Programming Language :: Python :: 2.6",
         "Programming Language :: Python :: 2.7",
         "Programming Language :: Python :: 3.3",
         "Programming Language :: Python :: 3.4",
         "Programming Language :: Python :: 3.5",
         "Programming Language :: Python :: 3.6",
         "Programming Language :: Python :: Implementation",
         "Programming Language :: Python :: Implementation :: CPython",   
         "Programming Language :: Python :: Implementation :: PyPy",
         "Topic :: Software Development :: Libraries :: Application Frameworks",
         "Topic :: Utilities"
    ]

    # matplotlib is not supported for PyPy, will be installed for CPython
    def version_update(cfg, *args):

        major = version_info[0]
        if (python_implementation() != 'PyPy'):
            cfg['modules'].append({'module': 'matplotlib', 'version': '>=2.0.0', 'profile': 'math'})

    config = {
        'pre_tasks' : [
            version_update,
            task.install_modules
        ],

        'post_tasks' : [
            task.set_config,
            task.set_manpage
        ],
         
        # numpy is required  
        'modules' : [   
            {'module': 'hydratk', 'version': '>=0.4.0'},
            {'module': 'numpy', 'version': '>=1.12.1'}
        ],
          
        'files' : {
            'config' : {
                'etc/hydratk/conf.d/hydratk-ext-physolver.conf' : '{0}/hydratk/conf.d'.format(syscfg.HTK_ETC_DIR)
            },
            'manpage' : 'doc/physolver.1'
        }

    } 

     task.run_pre_install(argv, config)                         
         
     entry_points = {
                'console_scripts': [
                    'physolver = hydratk.extensions.physolver.bootstrapper:run_app'                               
                ]
     }          
                        
     st_setup(
         name='physolver',
         version='0.1.0a-dev1',
         description='Physics problems solver',
         long_description=readme,
         author='Charlie Bowman',
         author_email='charlie.bowman@gmail.com',
         url='http://extensions.hydratk.org/Physolver',
         license='BSD',
         packages=st_find_packages('src'),
         package_dir={'' : 'src'},
         classifiers=classifiers,
         zip_safe=False,
         entry_points=entry_points,
         keywords='hydratk',
         requires_python='>=2.6,!=3.0.*,!=3.1.*,!=3.2.*',
         platforms='Linux,FreeBSD'
     )        
        
     task.run_post_install(argv, config)        

Main extension file is modified, dependency check and uninstallation procedure.

* physolver.py

  .. code-block:: python
  
     # -*- coding: utf-8 -*-
     """This code is a part of PhySolver extension

     .. module:: extensions.physolver.physolver
        :platform: Unix
        :synopsis: This HydraTK generated extension is providing physics problems solver
     .. moduleauthor:: Charlie Bowman <charlie.bowman@gmail.com>

     """

     from hydratk.core import extension, bootstrapper, event, const
     from hydratk.lib.console.commandlinetool import CommandlineTool
     from hydratk.lib.debugging.simpledebug import dmsg
     import hydratk.lib.system.config as syscfg

     import os
     import math

     # required modules for dependency check
     dep_modules = {
         'hydratk': {
             'min-version': '0.4.0',
             'package': 'hydratk'
         },
         'numpy': {
             'min-version': '1.12.1',
             'package': 'numpy'
         },
         'matplotlib': {
             'min-version': '2.0.0',
             'package': 'matplotlib'
         }
     }

     class Extension(extension.Extension):

         # from template and skeleton wizard
         def _init_extension(self):

             self._ext_id      = 'physolver'
             self._ext_name    = 'PhySolver'
             self._ext_version = '0.1.0a-dev1'
             self._ext_author  = 'Charlie Bowman <charlie.bowman@gmail.com>'
             self._ext_year    = '2018'
             self._ext_desc    = 'Physics problems solver'

             if (not self._check_dependencies()):
                 exit(0)

         # dependency check, required modules must be installed
         def _check_dependencies(self):
        
             return bootstrapper._check_dependencies(dep_modules, 'hydratk-ext-physolver')

         # uninstallation procedure, manual page and configuration are removed
         def _uninstall(self):
        
             files = [
                 '/usr/share/man/man1/physolver.1',
                 '{0}/hydratk/conf.d/hydratk-ext-physolver.conf'.format(syscfg.HTK_ETC_DIR)
             ]

             return files, dep_modules
             
Interface
^^^^^^^^^

The extension provides command line interface, both in htk and standalone mode.
First we will modify help file (only english version is shown, czech version is similar).
The interface provides 1 command run and 6 long options.

* help.py

  .. code-block:: python
  
     # -*- coding: utf-8 -*-
     """This code is a part of Physolver extension

     .. module:: extensions.physolver.translation.en.help
        :platform: Unix
        :synopsis: English language translation for Physolver extension help generator
     .. moduleauthor:: Charlie Bowman <charlie.bowman@gmail.com>

     """

     language = {
       'name' : 'English',
       'ISO-639-1' : 'en'
     } 

     ''' Physolver Commands '''
     help_cmd = {
        'phy-run' : 'run physolver',

        # standalone with option profile physolver
        'run': 'run physolver'
     }

     ''' Physolver Options '''
     help_opt = {
        'phy-init-cond' : { '{h}[--phy-init-cond <list>]{e}' : { 'description' : 'initial conditions, specific for each task, mandatory for single mode', 'commands' : ('phy-run')}},
        'phy-input' : { '{h}[--phy-input <path>]{e}' : { 'description' : 'input file path, see required format in doc, mandatory for parallel mode', 'commands' : ('phy-run')}},
        'phy-interval' : { '{h}[--phy-interval <number>]{e}' : { 'description' : 'time interval, default 10', 'commands' : ('phy-run')}},
        'phy-output' : { '{h}[--phy-output <path>]{e}' : { 'description' : 'output directory path, default .', 'commands' : ('phy-run')}},
        'phy-step' : { '{h}[--phy-step <number>]{e}' : { 'description' : 'time step, default 0.01', 'commands' : ('phy-run')}},
        'phy-task' : { '{h}[--phy-task <title>]{e}' : { 'description' : 'task, see available tasks in doc, mandatory for single mode', 'commands' : ('phy-run')}},

        # standalone with option profile physolver
        'init-cond' : { '{h}[--init-cond <list>]{e}' : { 'description' : 'initial conditions, specific for each task, mandatory for single mode', 'commands' : ('run')}},
        'input' : { '{h}[--input <path>]{e}' : { 'description' : 'input file path, see required format in doc, mandatory for parallel mode', 'commands' : ('run')}},
        'interval' : { '{h}[--interval <number>]{e}' : { 'description' : 'time interval, default 10', 'commands' : ('run')}},
        'output' : { '{h}[--output <path>]{e}' : { 'description' : 'output directory path, default .', 'commands' : ('run')}},
        'step' : { '{h}[--step <number>]{e}' : { 'description' : 'time step, default 0.01', 'commands' : ('run')}},
        'task' : { '{h}[--task <title>]{e}' : { 'description' : 'task, see available tasks in doc, mandatory for single mode', 'commands' : ('run')}}
     }

Manual page is prepared for standalone mode.
     
* physolver.1

  .. code-block:: cfg
  
     .TH physolver 1
     .SH NAME
     physolver \- runs Physolver HydraTK extension
     .SH SYNOPSIS
     .B physolver
     [\fBoptions\fR]
     .B command
     .SH DESCRIPTION
     \fBPhysolver\fR extension provides physics problems solver. 
     .SH COMMANDS
     \fBrun\fR - run physolver
       \fIOptions:\fR    
         \fB[--init-cond <list>]\fR - initial conditions, specific for each task, mandatory for single mode
         \fB[--input <path>]\fR - element title from specification, mandatory for parallel mode
         \fB[--interval <number>]\fR - time interval, default 10
         \fB[--output <path>]\fR - output directory path, default .
         \fB[--step <number>]\fR - time step, default 0.01
         \fB[--task <title>]\fR - task, see available tasks in doc, mandatory for single mode    

     \fBhelp\fR - prints help       
     .SH GLOBAL OPTIONS
     \fB-c, --config <file>\fR - reads the alternate configuration file

     \fB-d, --debug <level>\fR - debug turned on with specified level > 0

     \fB-e, --debug-channel <channel number, ..>\fR - debug channel filter turned on

     \fB-f, --force\fR - enforces command

     \fB-h, --home\fR - sets htk_root_dir to the current user home directory

     \fB-i, --interactive\fR - turns on interactive mode

     \fB-l, --language <language>\fR - sets the text output language, the list of available languages is specified in the docs

     \fB-m, --run-mode <mode>\fR - sets the running mode (1 - single, default, 2 - parallel), the list of available modes is specified in the docs
     .SH FILES AND DIRECTORIES
     Configuration file: /etc/hydratk/conf.d/physolver.conf
     .SH AUTHOR
     Charlie Bowman (charlie.bowman@gmail.com)
     .SH INTERNET RESOURCES
     .SH LICENSING
     hydratk-ext-physolver is distributed under BSD license. See the file "LICENSE.txt" in the source distribution for information.

Command actions are registered in main file. bootstrapper.py is not modified.
     
* physolver.py

  .. code-block:: python
  
     # register command actions for htk and standalone mode
     def _register_actions(self):

         if (self._mh.cli_cmdopt_profile == 'physolver'):
             self._register_standalone_actions()
         else:
             self._register_htk_actions()

     # command actions in htk mode
     def _register_htk_actions(self):
    
         # command
         self._mh.match_cli_command('phy-run')

         # command hook
         hook = [
             {'command': 'phy_run', 'callback': self.run}
         ]
         self._mh.register_command_hook(hook)

         # long options with value
         self._mh.match_long_option('init-cond', True, 'phy-init-cond')
         self._mh.match_long_option('input', True, 'phy-input')
         self._mh.match_long_option('interval', True, 'phy-interval')
         self._mh.match_long_option('output', True, 'phy-output')
         self._mh.match_long_option('step', True, 'phy-step')
         self._mh.match_long_option('task', True, 'phy-task')

     # command actions in standalone mode
     def _register_standalone_actions(self):

         # help command text
         option_profile = 'physolver'
         help_title = '{h}' + self._ext_name + ' v' + self._ext_version + '{e}'
         cp_string = '{u}' + "(c) " + self._ext_year + " " + self._ext_author + '{e}'
         self._mh.set_cli_appl_title(help_title, cp_string)

         # command
         self._mh.match_cli_command('run', option_profile)

         # command hook
         hook = [
              {'command': 'run', 'callback': self.run}
         ]
         self._mh.register_command_hook(hook)

         # help command
         self._mh.match_cli_command('help', option_profile)

         # long options with value, standalone titles are mapped to htk titles
         self._mh.match_long_option('init-cond', True, 'phy-init-cond', False, option_profile)
         self._mh.match_long_option('input', True, 'phy-input', False, option_profile)
         self._mh.match_long_option('interval', True, 'phy-interval', False, option_profile)
         self._mh.match_long_option('output', True, 'phy-output', False, option_profile)
         self._mh.match_long_option('step', True, 'phy-step', False, option_profile)
         self._mh.match_long_option('task', True, 'phy-task', False, option_profile)

         # global htk options
         self._mh.match_cli_option(('c', 'config'), True, 'config', False, option_profile)
         self._mh.match_cli_option(('d', 'debug'), True, 'debug', False, option_profile)
         self._mh.match_cli_option(('e', 'debug-channel'), True, 'debug-channel', False, option_profile)
         self._mh.match_cli_option(('l', 'language'), True, 'language', False, option_profile)
         self._mh.match_cli_option(('m', 'run-mode'), True, 'run-mode', False, option_profile)
         self._mh.match_cli_option(('f', 'force'), False, 'force', False, option_profile)
         self._mh.match_cli_option(('i', 'interactive'), False, 'interactive', False, option_profile)
         self._mh.match_cli_option(('h', 'home'), False, 'home', False, option_profile)
                  
Single mode
^^^^^^^^^^^

Now we will code command handle in single mode. The code will also contain documentation blocks compatible with Sphinx format. 
Whole htk code contains such blocks to generate documentation automatically.

Extension runs single task provided in option --task. The initial conditions are provided in option --init-cond in list form (cond1,cond2,...).
Options --step, --interval, --output are optional. If not provided the values are read from configuration (see below) or set by default. 

* physolver.py

  .. code-block:: python
  
     class Extension(extension.Extension):
         """Class Extension
         """

         # class attributes
         _tasks = [
                   'vertical_throw',
                   'horizontal_throw',
                   'oblique_throw',
                   'vibration',
                   'electric_field',
                   'magnetic_field',
                   'electromagnetic_field'
                  ]

        _init_cond = None
        _step = None
        _time = None
        
        def run(self):
            """Method runs physolver

            Args:
               none

            Returns:
               void

            """

            # debug message, the file content is displayed later
            self._mh.demsg('htk_on_debug_info', self._mh._trn.msg('physolver_received_cmd', 'phy-run'), self._mh.fromhere())

            # get options
            input = CommandlineTool.get_input_option('phy-input')
            task = CommandlineTool.get_input_option('phy-task')
            init_cond = CommandlineTool.get_input_option('phy-init-cond')
            step = CommandlineTool.get_input_option('phy-step')
            interval = CommandlineTool.get_input_option('phy-interval')
            output = CommandlineTool.get_input_option('phy-output')

            # get extension configuration
            cfg = self._mh.cfg['Extensions']['PhySolver']

            # single mode
            if (self._mh.run_mode == const.CORE_RUN_MODE_SINGLE_APP):

                # option validation
                dmsg(self._mh._trn.msg('physolver_running_mode', 'single'))
                if (not task):
                    print(self._mh._trn.msg('physolver_missing_option', 'task'))
                elif (task not in self._tasks):
                    print(self._mh._trn.msg('physolver_invalid_option_value', 'task', '|'.join(self._tasks)))
                elif (not init_cond):
                    print(self._mh._trn.msg('physolver_missing_option', 'init-cond'))
                else:

                    init_cond = init_cond.split(',')

                    # set parameters from option, config or default
                    if (step):
                        step = float(step)
                    elif ('step' in cfg):
                        step = float(cfg['step'])
                    else:
                        step = 0.01
                
                    if (interval):
                        interval = float(interval)
                    elif ('interval' in cfg):
                        interval = float(cfg['interval'])
                    else:
                        interval = 10.0
                    
                    if (output):
                        output = output
                    elif ('output' in cfg):
                        output = cfg['output']
                    else:
                        output = '.'
            
                    # run required task
                    self._run_task(task, init_cond, step, interval, output)
                    
        def _run_task(self, task, init_cond, step, interval, output, id=None):
            """Method handles context switch event in parallel mode

            Args:
               task (str): task title
               init_cond (list): initial conditions
               step (float): time step
               interval (float): time interval
               output (str): output directory path
               id (int): task id, used in parallel mode for output filename

            Returns:
               void

            """

            self._mh.demsg('htk_on_debug_info', self._mh._trn.msg('physolver_task_start', task, init_cond), self._mh.fromhere())
            
            # set class attributes
            self._init_cond = init_cond
            self._step = step
            self._interval = interval

            # run required task method
            data = getattr(self, '_task_' + task)()

            # task output
            if (data != None):
                self._prepare_output(task if(id == None) else task + str(id), data, output)
                self._mh.demsg('htk_on_debug_info', self._mh._trn.msg('physolver_task_finish', task, init_cond), self._mh.fromhere())
                
* hydratk-ext-physolver.conf

  .. code-block: cfg
  
     Extensions:
       PhySolver:
       package: hydratk.extensions.physolver
       module: physolver       
       enabled: 1    
       interval: 10
       step: 0.01
       output: .
       
* Parallel mode

Now we will code command handle in parallel mode.

Mode is enabled by global option -m 2. Extension requires option --input and parses the file. Each row uses format task;init-cond;step;interval;output.
Extension runs each task in separate process and is stopped when all tasks are processed.
The code also shows event firing (start, finish) and processing (context switch, start, finish).

 .. code-block:: python
 
    class Extension(extension.Extension):
        """Class Extension
        """

        # class attributes
        _tickets = []
        
        def _register_actions(self):

            # event hooks
            hook = [
                    {'event': 'htk_on_cobserver_ctx_switch', 'callback': self._pp_app_check},
                    {'event': 'physolver_pp_run_started', 'callback': self._pp_started},
                    {'event': 'physolver_pp_run_finished', 'callback': self._pp_finished}
                   ]

            self._mh.register_event_hook(hook)
            
        def run(self):
        
            # parallel mode
            elif (self._mh.run_mode == const.CORE_RUN_MODE_PP_APP):

                # option validation
                dmsg(self._mh._trn.msg('physolver_running_mode', 'parallel'))
                if (not input):
                    print(self._mh._trn.msg('physolver_missing_option', 'input'))
                elif (not os.path.exists(input)):
                    print(self._mh._trn.msg('physolver_invalid_option_value', 'input', 'existing file'))
                else:

                    # start event
                    ev = event.Event('physolver_pp_run_started', input)
                    self._mh.fire_event(ev)

                    with open(input, 'r') as f:
                        content = f.readlines()

                    # parse input file
                    id = 1
                    for l in content:

                        task, init_cond, step, interval, output = l.split(';')
                        if (task not in self._tasks):
                            print(self._mh._trn.msg('physolver_invalid_option_value', 'task', '|'.join(self._tasks)))
                        else:

                            init_cond = init_cond.split(',')

                            # set parameters from option, config or default
                            if (step):
                                step = float(step)
                            elif ('step' in cfg):
                                step = float(cfg['step'])
                            else:
                                step = 0.01

                            if (interval):
                                interval = float(interval)
                            elif ('interval' in cfg):
                                interval = float(cfg['interval'])
                            else:
                                interval = 10.0
                    
                            if (output):
                                output = output[:-1]
                            elif ('output' in cfg):
                                output = cfg['output']
                            else:
                                output = '.'

                            # create ticket to run required task asynchronously
                            ticket_id = self._mh.async_ext_fn((self, '_run_task'), None, task, init_cond, step, interval, output, id)
                            self._tickets.append(ticket_id)
                            id += 1
                            
        def _pp_started(self, ev):
            """Method handles start event in parallel mode

            Args:
               ev (obj): event

            Returns:
               void

            """

            print(self._mh._trn.msg('physolver_pp_run_started', ev._args[0]))

        def _pp_finished(self, ev):
            """Method handles finish event in parallel mode

            Args:
               ev (obj): event

            Returns:
               void

            """

            print(self._mh._trn.msg('physolver_pp_run_finished'))
        
        def _pp_app_check(self, ev):
            """Method handles context switch event in parallel mode

            Args:
               ev (obj): event

            Returns:
               void

            """

            dmsg(self._mh._trn.msg('physolver_context_switch', len(self._tickets)))
            # tickets not processed yet
            if len(self._tickets) > 0:
                for index, ticket_id in enumerate(self._tickets):
                    dmsg(self._mh._trn.msg('physolver_checking_ticket', ticket_id))
                    if self._mh.async_ticket_completed(ticket_id):
                        self._mh.delete_async_ticket(ticket_id)
                        del self._tickets[index]
                    else:
                        dmsg(self._mh._trn.msg('physolver_waiting_tickets', len(self._tickets)))

            # tickets processed, stop application
            else:
                ev = event.Event('physolver_pp_run_finished')
                self._mh.fire_event(ev)
                self._mh.stop_pp_app()
                
* messages.py

Now we will configure message langtexts (english version is displayed only).

  .. code-block:: python
  
     # -*- coding: utf-8 -*-
     """This code is a part of Physolver extension

     .. module:: extensions.physolver.translation.en
        :platform: Unix
        :synopsis: English language translation for Physolver extension
     .. moduleauthor:: Charlie Bowman <charlie.bowman@gmail.com>

     """

     language = {
       'name' : 'English',
       'ISO-639-1' : 'en'
     }

     msg = {
         'physolver_received_cmd': ["Received command: '{0}'"],
         'physolver_missing_option': ["Missing option: {0}"],
         'physolver_invalid_option_value': ["Invalid option {0} value, supported values: {1}"],
         'physolver_running_mode' : ["Running in {0} mode"],
         'physolver_context_switch': ["Got context switch, active tickets: {0}"],
         'physolver_checking_ticket': ["Checking ticket_id {0}"],
         'physolver_waiting_tickets': ["There are still {0} waiting tickets"],
         'physolver_task_start' : ['Task {0} with initial conditions {1} was started'],
         'physolver_task_finish' : ['Task {0} with initial conditions {1} was finished'],
         'physolver_pp_run_started' : ['Run in parallel mode started, input file {0}'],
         'physolver_pp_run_finished': ['Run in parallel mode finished']
     }
     
Solver
^^^^^^

Finally we can code methods to solve appropriate tasks including output preparation.
It requires basic knowledge of physics, numerical scheme for differential equations and matplotlib graphs.

* physolver.py

  .. code-block:: python

     def _prepare_output(self, task, data, output):
         """Method prepares task output, CSV file and graphs

         Args:
            task (str): task filename
            data (dict): calculated data
            output (str): output directory path

         Returns:
            void

         """
        
         # CSV file
         data['t'] = [str(i) for i in data['t']]
         out = 't;' + ';'.join(data['t'])

         if ('x' in data):
             data['x'] = [str(i) for i in data['x']]
             out += '\nx;' + ';'.join(data['x'])
         if ('vx' in data):
             data['vx'] = [str(i) for i in data['vx']]
             out += '\nvx;' + ';'.join(data['vx'])
         if ('y' in data):
             data['y'] = [str(i) for i in data['y']]
             out += '\ny;' + ';'.join(data['y'])
         if ('vy' in data):
             data['vy'] = [str(i) for i in data['vy']]
             out += '\nvy;' + ';'.join(data['vy'])

         path = os.path.join(output, task+'.csv')
         with open(path, 'w') as f:
             f.write(out)

         # graphs
         import matplotlib.pyplot as plt

         if ('x' in data):
             plt.figure()
             plt.xlabel('--> t [s]')
             plt.ylabel('--> x [m]')
             plt.title(task)
             plt.grid('on')
             plt.plot(data['t'], data['x'])
             plt.savefig(task + '_x_t.png')
         if ('vx' in data):
             plt.figure()
             plt.xlabel('--> t [s]')
             plt.ylabel('--> vx [m/s]')
             plt.title(task)
             plt.grid('on')
             plt.plot(data['t'], data['vx'])
             plt.savefig(task + '_vx_t.png')
         if ('y' in data):
             plt.figure()
             plt.xlabel('--> t [s]')
             plt.ylabel('--> y [m]')
             plt.title(task)
             plt.grid('on')
             plt.plot(data['t'], data['y'])
             plt.savefig(task + '_y_t.png')
         if ('vy' in data):
             plt.figure()
             plt.xlabel('--> t [s]')
             plt.ylabel('--> vy [m/s]')
             plt.title(task)
             plt.grid('on')
             plt.plot(data['t'], data['vy'])
             plt.savefig(task + '_vy_t.png')
         if ('x' in data and 'y' in data):
             plt.figure()
             plt.xlabel('--> x [m]')
             plt.ylabel('--> y [m]')
             plt.title(task)
             plt.grid('on')
             plt.plot(data['x'], data['y'])
             plt.savefig(task + '_x_y.png')
            
         # phase portrait
         r, v = [], [] 
         if ('x' in data and 'vx' in data and ('y' not in data and 'vy' not in data)):
             r, v = data['x'], data['vx']
         elif ('y' in data and 'vy' in data and ('x' not in data and 'vx' not in data)):
             r, v = data['y'], data['vy']
         elif ('x' in data and 'vx' in data and 'y' in data and 'vy' in data):
             for i in range(len(data['t'])):
                 x, y, vx, vy = float(data['x'][i]), float(data['y'][i]), float(data['vx'][i]), float(data['vy'][i])
                 r.append(math.sqrt(x * x + y * y))
                 v.append(math.sqrt(vx * vx + vy * vy))
                
         if (r != [] and v != []):
             plt.figure()
             plt.xlabel('--> r [m]')
             plt.ylabel('--> v [m/s]')
             plt.title(task)
             plt.grid('on')
             plt.plot(r, v)
             plt.savefig(task + '_r_v.png')
 
     def _task_vertical_throw(self):
         """Method solves vertical throw

         Initial conditions: y0, vy0
         Output: t, y, vy

         Args:
            none

         Returns:
            dict

         """
        
         if (len(self._init_cond) != 2):
             print(self._mh._trn.msg('physolver_invalid_option_value', 'init-cond', 'y0, vy0'))
             return None

         y0, vy0 = float(self._init_cond[0]), float(self._init_cond[1])
         t, y, vy, g = self._step, y0, vy0, 10.0

         data = {
                 't' : [0.0],
                 'y' : [y],
                 'vy' : [vy]
                }

         while (t <= self._interval):

             y = y + vy * self._step
             vy = vy - g * self._step
 
             data['t'].append(t)
             data['y'].append(y)
             data['vy'].append(vy)
 
             t += self._step

         return data

     def _task_horizontal_throw(self):
         """Method solves horizontal throw

         Initial conditions: y0, vx0
         Output: t, x, vx, y, vy

         Args:
            none

         Returns:
            dict

         """

         if (len(self._init_cond) != 2):
             print(self._mh._trn.msg('physolver_invalid_option_value', 'init-cond', 'y0, vx0'))
             return None

         y0, vx0 = float(self._init_cond[0]), float(self._init_cond[1])
         t, x, vx, y, vy, g = self._step, 0.0, vx0, y0, 0.0, 10.0

         data = {
                 't' : [0.0],
                 'x' : [x],
                 'vx' : [vx],
                 'y' : [y],
                 'vy' : [vy]
                }

         while (t <= self._interval):

             x = x + vx * self._step
             vx = vx
             y = y + vy * self._step
             vy = vy - g * self._step

             data['t'].append(t)
             data['x'].append(x)
             data['vx'].append(vx)
             data['y'].append(y)
             data['vy'].append(vy)

             t += self._step

         return data

     def _task_oblique_throw(self):
         """Method solves oblique throw

         Initial conditions: alpha, v0
         Output: t, x, vx, y, vy

         Args:
            none

         Returns:
            dict

         """

         if (len(self._init_cond) != 2):
             print(self._mh._trn.msg('physolver_invalid_option_value', 'init-cond', 'alpha, v0'))
             return None

         alpha, v0 = float(self._init_cond[0]) * math.pi / 180, float(self._init_cond[1])
         vx0, vy0 = v0 * math.cos(alpha), v0 * math.sin(alpha)
         t, x, vx, y, vy, g = self._step, 0.0, vx0, 0.0, vy0, 10.0

         data = {
                 't' : [0.0],
                 'x' : [x],
                 'vx' : [vx],
                 'y' : [y],
                 'vy' : [vy]
                }

         while (t <= self._interval):

             x = x + vx * self._step
             vx = vx
             y = y + vy * self._step
             vy = vy - g * self._step

             data['t'].append(t)
             data['x'].append(x)
             data['vx'].append(vx)
             data['y'].append(y)
             data['vy'].append(vy)

             t += self._step

         return data

     def _task_vibration(self):
         """Method solves vibration motion

         Initial conditions: y0, vy0
         Output: t, y, vy

         Args:
            none

         Returns:
            dict

         """

         if (len(self._init_cond) != 2):
             print(self._mh._trn.msg('physolver_invalid_option_value', 'init-cond', 'y0, vy0'))
             return None

         y0, vy0 = float(self._init_cond[0]), float(self._init_cond[1])
         t, y, vy, k = self._step, y0, vy0, 5.0

         data = {
                 't' : [0.0],
                 'y' : [y],
                 'vy' : [vy]
                }

         while (t <= self._interval):

             y = y + vy * self._step
             vy = vy - k * y * self._step

             data['t'].append(t)
             data['y'].append(y)
             data['vy'].append(vy)

             t += self._step

         return data

     def _task_electric_field(self):
         """Method solves motion in electric field

         Initial conditions: Ex, m, q
         Output: t, x, vx

         Args:
            none

         Returns:
            dict

         """

         if (len(self._init_cond) != 3):
             print(self._mh._trn.msg('physolver_invalid_option_value', 'init-cond', 'Ex, m, q'))
             return None

         E, m, q = float(self._init_cond[0]), float(self._init_cond[1]), float(self._init_cond[2])
         t, x, vx = self._step, 0.0, 0.0

         data = {
                 't' : [0.0],
                 'x' : [x],
                 'vx' : [vx]
                }

         while (t <= self._interval):

             x = x + vx * self._step
             vx = vx + q / m * E * self._step

             data['t'].append(t)
             data['x'].append(x)
             data['vx'].append(vx)
 
             t += self._step

         return data

     def _task_magnetic_field(self):
         """Method solves motion in magnetic field

         Initial conditions: Bz, vy0, m, q
         Output: t, x, vx, y, vy

         Args:
            none

         Returns:
            dict

         """

         if (len(self._init_cond) != 4):
             print(self._mh._trn.msg('physolver_invalid_option_value', 'init-cond', 'Bz, vy0, m, q'))
             return None

         B, vy0, m, q = float(self._init_cond[0]), float(self._init_cond[1]), float(self._init_cond[2]), float(self._init_cond[3])
         t, x, vx, y, vy = self._step, 0.0, 0.0, 0.0, vy0

         data = {
                 't' : [0.0],
                 'x' : [x],
                 'vx' : [vx],
                 'y' : [y],
                 'vy' : [vy]
                }

         while (t <= self._interval):

             x = x + vx * self._step
             vx_n = vx + q / m * B * vy * self._step

             y = y + vy * self._step
             vy = vy - q / m * B * vx * self._step
             vx = vx_n

             data['t'].append(t)
             data['x'].append(x)
             data['vx'].append(vx)
             data['y'].append(y)
             data['vy'].append(vy)

             t += self._step

         return data

     def _task_electromagnetic_field(self):
         """Method solves motion in electromagnetic field

         Initial conditions: Ex, Bz, m, q
         Output: t, x, vx, y, vy

         Args:
            none

         Returns:
            dict

         """

         if (len(self._init_cond) != 4):
             print(self._mh._trn.msg('physolver_invalid_option_value', 'init-cond', 'Ex, Bz, m, q'))
             return None

         E, B, m, q = float(self._init_cond[0]), float(self._init_cond[1]), float(self._init_cond[2]), float(self._init_cond[3])
         t, x, vx, y, vy = self._step, 0.0, 0.0, 0.0, 0.0

         data = {
                 't' : [0.0],
                 'x' : [x],
                 'vx' : [vx],
                 'y' : [y],
                 'vy' : [vy]
                }

         while (t <= self._interval):

             x = x + vx * self._step
             vx_n = vx + q / m * E * self._step + q / m * B * vy * self._step

             y = y + vy * self._step
             vy = vy - q / m * B * vx * self._step
             vx = vx_n

             data['t'].append(t)
             data['x'].append(x)
             data['vx'].append(vx)
             data['y'].append(y)
             data['vy'].append(vy)
 
             t += self._step

         return data
         
Usage
^^^^^

* Interface

  .. code-block:: bash
  
     $ physolver
  
     PhySolver v0.1.0a-dev1
     (c) 2018 Charlie Bowman <charlie.bowman@gmail.com>
     Usage: physolver [options] command
     For list of the all available commands and options type physolver help
              
     $ physolver help
     
     PhySolver v0.1.0a-dev1
     (c) 2018 Charlie Bowman <charlie.bowman@gmail.com>
     Usage: physolver [options] command

     Commands:
        help - prints help
        run - run physolver
           Options:
              [--init-cond <list>] - initial conditions, specific for each task, mandatory for single mode
              [--input <path>] - input file path, see required format in doc, mandatory for parallel mode
              [--interval <number>] - time interval, default 10
              [--output <path>] - output directory path, default .
              [--step <number>] - time step, default 0.01
              [--task <title>] - task, see available tasks in doc, mandatory for single mode


     Global Options:
        -c, --config <file> - reads the alternate configuration file
        -d, --debug <level> - debug turned on with specified level > 0
        -e, --debug-channel <channel number, ..> - debug channel filter turned on
        -f, --force - enforces command
        -h, --home - sets htk_root_dir to the current user home directory
        -i, --interactive - turns on interactive mode
        -l, --language <language> - sets the text output language, the list of available languages is specified in the docs
        -m, --run-mode <mode> - sets the running mode, the list of available modes is specified in the docs
              
* Single mode

  .. code-block:: bash
  
     # minimal option variant
     $ physolver --task vertical_throw --init-cond "100,0" run
     
     $ ls
     vertical_throw.csv  vertical_throw_vy_t.png  vertical_throw_r_v.png  vertical_throw_y_t.png
     
     # full option variant
     $ physolver --task vibration --init-cond "0,10" --step 0.01 --interval 10 --output . run
          
     $ ls
     vibration.csv  vibration_vy_t.png  vibration_r_v.png  vibration_y_t.png
     
     # debug detail
     $ physolver --task vibration --init-cond "0,10" --step 0.01 --interval 10 --output . run
     
     01/06/2018 10:24:35,419 DEBUG(1): hydratk.core.corehead.CoreHead._append_extension_config_from_file:[0]: Trying to load extension config /root/.pyenv/versions/p27/etc/hydratk/conf.d/hydratk-ext-physolver.conf
     01/06/2018 10:24:35,451 DEBUG(1): hydratk.core.corehead.CoreHead._append_extension_config_from_file:[0]: Loaded extension config /root/.pyenv/versions/p27/etc/hydratk/conf.d/hydratk-ext-physolver.conf
     01/06/2018 10:24:35,501 DEBUG(1): hydratk.core.corehead.CoreHead._apply_config:[0]: Run mode set to '1 (CORE_RUN_MODE_SINGLE_APP)'
     01/06/2018 10:24:37,787 DEBUG(1): hydratk.core.corehead.CoreHead._load_extension:[0]: Loading internal extension: 'PhySolver'
     01/06/2018 10:24:37,807 DEBUG(1): hydratk.core.corehead.CoreHead._import_extension_messages:[0]: Trying to to load extension messages for language en, package 'hydratk.extensions.physolver.translation.en.messages'
     01/06/2018 10:24:37,809 DEBUG(1): hydratk.core.corehead.CoreHead._import_extension_messages:[0]: Extensions messages for language en, loaded successfully
     01/06/2018 10:24:37,823 DEBUG(1): hydratk.core.corehead.CoreHead._import_extension_messages:[0]: Trying to to load extension help for language en, package 'hydratk.extensions.physolver.translation.en.help'
     01/06/2018 10:24:38,733 DEBUG(1): hydratk.extensions.physolver.physolver.Extension.run:[0]: Received command: 'phy-run'
     01/06/2018 10:24:38,734 DEBUG(1): hydratk.extensions.physolver.physolver.Extension.run:[0]: Running in single mode
     01/06/2018 10:24:38,755 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._run_task:[0]: Task vibration with initial conditions ['0', '10'] was started
     01/06/2018 10:24:41,195 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._run_task:[0]: Task vibration with initial conditions ['0', '10'] was finished
     01/06/2018 10:24:41,197 DEBUG(1): hydratk.extensions.physolver.bootstrapper.run_app:[0]: Application exit
     
* Parallel mode

  .. code-block:: bash
   
     # all tasks
     $ cat input.csv
     
     vertical_throw;100,0;0.01;10;.
     horizontal_throw;10,20;;;
     oblique_throw;45,20;;;
     vibration;0,10;;;
     electric_field;100,0.001,0.001;;;
     magnetic_field;1,10,0.001,0.001;;;
     electromagnetic_field;100,10,0.001,0.001;;;
            
     $ physolver -m 2 --input input.csv run
     
     Run in parallel mode started, input file input.csv
     Run in parallel mode finished
     
     $ ls
     electromagnetic_field7_vx_t.png  horizontal_throw2_vy_t.png       magnetic_field6_vy_t.png    oblique_throw3_x_t.png  vertical_throw1_r_v.png
     electromagnetic_field7_vy_t.png  horizontal_throw2_x_t.png        magnetic_field6_x_t.png     oblique_throw3_x_y.png  vertical_throw1_vy_t.png
     electromagnetic_field7_x_t.png   horizontal_throw2_x_y.png        magnetic_field6_x_y.png     oblique_throw3_y_t.png  vertical_throw1_y_t.png
     electric_field5.csv              electromagnetic_field7_x_y.png   horizontal_throw2_y_t.png   magnetic_field6_y_t.png vibration4.csv
     electric_field5_r_v.png          electromagnetic_field7_y_t.png   input.csv                   vibration4_r_v.png
     electric_field5_vx_t.png         oblique_throw3.csv               vibration4_vy_t.png
     electric_field5_x_t.png          horizontal_throw2.csv            magnetic_field6.csv         oblique_throw3_r_v.png   vibration4_y_t.png
     electromagnetic_field7.csv       horizontal_throw2_r_v.png        magnetic_field6_r_v.png     oblique_throw3_vx_t.png   
     electromagnetic_field7_r_v.png   horizontal_throw2_vx_t.png       magnetic_field6_vx_t.png    oblique_throw3_vy_t.png  vertical_throw1.csv
     
     # debug detail
     $ physolver -d 1 m 2 --input input.csv run
     
     01/06/2018 10:37:31,417 DEBUG(1): hydratk.core.corehead.CoreHead._append_extension_config_from_file:[0]: Trying to load extension config /root/.pyenv/versions/p27/etc/hydratk/conf.d/hydratk-ext-physolver.conf
     01/06/2018 10:37:31,424 DEBUG(1): hydratk.core.corehead.CoreHead._append_extension_config_from_file:[0]: Loaded extension config /root/.pyenv/versions/p27/etc/hydratk/conf.d/hydratk-ext-physolver.conf
     01/06/2018 10:37:31,445 DEBUG(1): hydratk.core.corehead.CoreHead._apply_config:[0]: Run mode set to '2 (CORE_RUN_MODE_PP_APP)'
     01/06/2018 10:37:31,445 DEBUG(1): hydratk.core.corehead.CoreHead._apply_config:[0]: Main message router id set to 'raptor01'
     01/06/2018 10:37:31,446 DEBUG(1): hydratk.core.corehead.CoreHead._apply_config:[0]: Number of core workers set to: 4
     01/06/2018 10:37:33,313 DEBUG(1): hydratk.core.corehead.CoreHead._load_extension:[0]: Loading internal extension: 'PhySolver'
     01/06/2018 10:37:33,319 DEBUG(1): hydratk.core.corehead.CoreHead._import_extension_messages:[0]: Trying to to load extension messages for language en, package 'hydratk.extensions.physolver.translation.en.messages'
     01/06/2018 10:37:33,321 DEBUG(1): hydratk.core.corehead.CoreHead._import_extension_messages:[0]: Extensions messages for language en, loaded successfully
     01/06/2018 10:37:33,322 DEBUG(1): hydratk.core.corehead.CoreHead._import_extension_messages:[0]: Trying to to load extension help for language en, package 'hydratk.extensions.physolver.translation.en.help'
     01/06/2018 10:37:33,592 DEBUG(1): hydratk.core.corehead.CoreHead._load_extension:[0]: Internal extension: 'PhySolver v0.1.0a-dev1 (c) [2018 Charlie Bowman <charlie.bowman@gmail.com>]' loaded successfully
     01/06/2018 10:37:34,113 DEBUG(1): hydratk.core.corehead.CoreHead._init_message_router:[0]: Message Router 'raptor01' initialized successfully
     01/06/2018 10:37:34,116 DEBUG(1): hydratk.core.corehead.CoreHead._c_observer:[0]: Core message service 'c01' registered successfully
     01/06/2018 10:37:34,117 DEBUG(1): hydratk.core.corehead.CoreHead._c_observer:[0]: Starting to observe
     01/06/2018 10:37:34,118 DEBUG(1): hydratk.core.corehead.CoreHead._c_observer:[0]: Saving PID 5379 to file: /tmp/hydratk/hydratk.pid
     01/06/2018 10:37:34,131 DEBUG(1): hydratk.core.masterhead.MasterHead.add_core_thread:[0]: Initializing core thread id: 1
     01/06/2018 10:37:34,141 DEBUG(1): hydratk.core.masterhead.MasterHead.add_core_thread:[0]: Initializing core thread id: 2
     01/06/2018 10:37:34,173 DEBUG(1): hydratk.core.corehead.CoreHead._c_worker:[1]: Core message queue '/tmp/hydratk/core.socket' connected successfully
     01/06/2018 10:37:34,175 DEBUG(1): hydratk.core.masterhead.MasterHead.add_core_thread:[0]: Initializing core thread id: 3
     01/06/2018 10:37:34,175 DEBUG(1): hydratk.core.corehead.CoreHead._c_worker:[1]: Starting to work
     01/06/2018 10:37:34,194 DEBUG(1): hydratk.core.masterhead.MasterHead.add_core_thread:[0]: Initializing core thread id: 4
     01/06/2018 10:37:34,227 DEBUG(1): hydratk.extensions.physolver.physolver.Extension.run:[0]: Received command: 'phy-run'
     01/06/2018 10:37:34,228 DEBUG(1): hydratk.extensions.physolver.physolver.Extension.run:[0]: Running in parallel mode
     01/06/2018 10:37:34,233 DEBUG(1): hydratk.core.messagehead.CoreHead._process_cmsg:[1]: Processing message: {'type': 'async_ext_fn', 'from': 'htk_obsrv@core.raptor', 'to': 'any@core.raptor', 'data': {'callback': {'method': '_run_task', 'args': ('vertical_throw', ['100', '0'], 0.01, 10.0, '.', 1), 'ext_name': 'PhySolver', 'kwargs': {}}, 'ticket_id': '1527842254.23-0-1'}}
     Run in parallel mode started, input file input.csv
     01/06/2018 10:37:34,237 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: Got context switch, active tickets: 7
     01/06/2018 10:37:34,237 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: Checking ticket_id 1527842254.23-0-1
     01/06/2018 10:37:34,240 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._run_task:[1]: Task vertical_throw with initial conditions ['100', '0'] was started
     01/06/2018 10:37:34,245 DEBUG(1): hydratk.core.corehead.CoreHead._c_worker:[2]: Core message queue '/tmp/hydratk/core.socket' connected successfully
     01/06/2018 10:37:34,253 DEBUG(1): hydratk.core.corehead.CoreHead._c_worker:[3]: Core message queue '/tmp/hydratk/core.socket' connected successfully
     01/06/2018 10:37:34,259 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: There are still 7 waiting tickets
     01/06/2018 10:37:34,259 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: Checking ticket_id 1527842254.23-0-2
     01/06/2018 10:37:34,246 DEBUG(1): hydratk.core.corehead.CoreHead._c_worker:[2]: Starting to work
     01/06/2018 10:37:34,265 DEBUG(1): hydratk.core.messagehead.CoreHead._process_cmsg:[2]: Processing message: {'type': 'async_ext_fn', 'from': 'htk_obsrv@core.raptor', 'to': 'any@core.raptor', 'data': {'callback': {'method': '_run_task', 'args': ('oblique_throw', ['45', '20'], 0.01, 10.0, '', 3), 'ext_name': 'PhySolver', 'kwargs': {}}, 'ticket_id': '1527842254.23-0-3'}}
     01/06/2018 10:37:34,276 DEBUG(1): hydratk.core.corehead.CoreHead._c_worker:[3]: Starting to work
     01/06/2018 10:37:34,290 DEBUG(1): hydratk.core.messagehead.CoreHead._process_cmsg:[3]: Processing message: {'type': 'async_ext_fn', 'from': 'htk_obsrv@core.raptor', 'to': 'any@core.raptor', 'data': {'callback': {'method': '_run_task', 'args': ('horizontal_throw', ['10', '20'], 0.01, 10.0, '', 2), 'ext_name': 'PhySolver', 'kwargs': {}}, 'ticket_id': '1527842254.23-0-2'}}
     01/06/2018 10:37:34,293 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._run_task:[2]: Task oblique_throw with initial conditions ['45', '20'] was started
     01/06/2018 10:37:34,296 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._run_task:[3]: Task horizontal_throw with initial conditions ['10', '20'] was started
     01/06/2018 10:37:34,359 DEBUG(1): hydratk.core.corehead.CoreHead._c_worker:[4]: Core message queue '/tmp/hydratk/core.socket' connected successfully
     01/06/2018 10:37:34,359 DEBUG(1): hydratk.core.corehead.CoreHead._c_worker:[4]: Starting to work
     01/06/2018 10:37:35,342 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: Got context switch, active tickets: 7
     01/06/2018 10:37:38,613 DEBUG(1): hydratk.extensions.yoda.yoda.Extension.pp_app_check:[0]: Got context switch, active tickets: 0
     01/06/2018 10:37:39,567 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._run_task:[1]: Task vertical_throw with initial conditions ['100', '0'] was finished
     01/06/2018 10:37:39,569 DEBUG(1): hydratk.core.messagehead.CoreHead._process_cmsg:[1]: Processing message: {'type': 'async_ext_fn', 'from': 'htk_obsrv@core.raptor', 'to': 'any@core.raptor', 'data': {'callback': {'method': '_run_task', 'args': ('vibration', ['0', '10'], 0.01, 10.0, '', 4), 'ext_name': 'PhySolver', 'kwargs': {}}, 'ticket_id': '1527842254.23-0-4'}}
     01/06/2018 10:37:39,587 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._run_task:[1]: Task vibration with initial conditions ['0', '10'] was started
     01/06/2018 10:37:39,617 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: Got context switch, active tickets: 7
     01/06/2018 10:37:39,631 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: Checking ticket_id 1527842254.23-0-1
     01/06/2018 10:37:39,633 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: Checking ticket_id 1527842254.23-0-3
     01/06/2018 10:37:39,633 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: There are still 6 waiting tickets
     01/06/2018 10:37:42,723 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._run_task:[1]: Task vibration with initial conditions ['0', '10'] was finished
     01/06/2018 10:37:42,724 DEBUG(1): hydratk.core.messagehead.CoreHead._process_cmsg:[1]: Processing message: {'type': 'async_ext_fn', 'from': 'htk_obsrv@core.raptor', 'to': 'any@core.raptor', 'data': {'callback': {'method': '_run_task', 'args': ('electromagnetic_field', ['100', '10', '0.001', '0.001'], 0.01, 10.0, '', 7), 'ext_name': 'PhySolver', 'kwargs': {}}, 'ticket_id': '1527842254.24-0-7'}}
     01/06/2018 10:37:42,726 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._run_task:[1]: Task electromagnetic_field with initial conditions ['100', '10', '0.001', '0.001'] was started
     01/06/2018 10:37:42,784 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: Got context switch, active tickets: 6
     01/06/2018 10:37:42,811 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: Checking ticket_id 1527842254.24-0-6
     01/06/2018 10:37:42,829 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: There are still 5 waiting tickets
     01/06/2018 10:37:42,850 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._run_task:[3]: Task horizontal_throw with initial conditions ['10', '20'] was finished
     01/06/2018 10:37:42,877 DEBUG(1): hydratk.core.messagehead.CoreHead._process_cmsg:[3]: Processing message: {'type': 'async_ext_fn', 'from': 'htk_obsrv@core.raptor', 'to': 'any@core.raptor', 'data': {'callback': {'method': '_run_task', 'args': ('electric_field', ['100', '0.001', '0.001'], 0.01, 10.0, '', 5), 'ext_name': 'PhySolver', 'kwargs': {}}, 'ticket_id': '1527842254.24-0-5'}}
     01/06/2018 10:37:42,878 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._run_task:[3]: Task electric_field with initial conditions ['100', '0.001', '0.001'] was started
     01/06/2018 10:37:43,109 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._run_task:[2]: Task oblique_throw with initial conditions ['45', '20'] was finished
     01/06/2018 10:37:43,131 DEBUG(1): hydratk.core.messagehead.CoreHead._process_cmsg:[2]: Processing message: {'type': 'async_ext_fn', 'from': 'htk_obsrv@core.raptor', 'to': 'any@core.raptor', 'data': {'callback': {'method': '_run_task', 'args': ('magnetic_field', ['1', '10', '0.001', '0.001'], 0.01, 10.0, '', 6), 'ext_name': 'PhySolver', 'kwargs': {}}, 'ticket_id': '1527842254.24-0-6'}}
     01/06/2018 10:37:43,132 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._run_task:[2]: Task magnetic_field with initial conditions ['1', '10', '0.001', '0.001'] was started
     01/06/2018 10:37:43,854 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: Got context switch, active tickets: 5
     01/06/2018 10:37:43,855 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: Checking ticket_id 1527842254.23-0-2
     01/06/2018 10:37:43,856 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: Checking ticket_id 1527842254.24-0-5
     01/06/2018 10:37:43,857 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: There are still 4 waiting tickets
     01/06/2018 10:37:43,857 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: Checking ticket_id 1527842254.24-0-6
     01/06/2018 10:37:44,881 DEBUG(1): hydratk.core.corehead.CoreHead._check_cw_activity:[0]: Checking live status on thread: 1, last activity before: 2.15677785873
     01/06/2018 10:37:44,882 DEBUG(1): hydratk.core.corehead.CoreHead._check_cw_activity:[0]: Checking live status on thread: 2, last activity before: 1.77164101601
     01/06/2018 10:37:44,888 DEBUG(1): hydratk.core.corehead.CoreHead._check_cw_activity:[0]: Checking live status on thread: 3, last activity before: 2.01188111305
     01/06/2018 10:37:44,889 DEBUG(1): hydratk.core.corehead.CoreHead._check_cw_activity:[0]: Checking live status on thread: 4, last activity before: 0.602080106735
     01/06/2018 10:37:44,890 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: Got context switch, active tickets: 4
     01/06/2018 10:37:44,903 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: Checking ticket_id 1527842254.23-0-3
     01/06/2018 10:37:44,904 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: Checking ticket_id 1527842254.24-0-6
     01/06/2018 10:37:44,905 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: There are still 3 waiting tickets
     01/06/2018 10:37:44,905 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: Checking ticket_id 1527842254.24-0-7
     01/06/2018 10:37:46,980 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: Checking ticket_id 1527842254.24-0-7
     01/06/2018 10:37:46,981 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: There are still 2 waiting tickets
     01/06/2018 10:37:48,035 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: Got context switch, active tickets: 2
     01/06/2018 10:37:48,035 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: Checking ticket_id 1527842254.24-0-6
     01/06/2018 10:37:48,036 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: There are still 2 waiting tickets
     01/06/2018 10:37:48,824 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._run_task:[1]: Task electromagnetic_field with initial conditions ['100', '10', '0.001', '0.001'] was finished
     01/06/2018 10:37:48,944 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._run_task:[2]: Task magnetic_field with initial conditions ['1', '10', '0.001', '0.001'] was finished
     01/06/2018 10:37:49,061 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: Got context switch, active tickets: 2
     01/06/2018 10:37:49,062 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: Checking ticket_id 1527842254.24-0-6
     01/06/2018 10:37:50,073 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: Got context switch, active tickets: 1
     01/06/2018 10:37:50,075 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: Checking ticket_id 1527842254.24-0-7
     01/06/2018 10:37:51,085 DEBUG(1): hydratk.extensions.physolver.physolver.Extension._pp_app_check:[0]: Got context switch, active tickets: 0
     Run in parallel mode finished
     01/06/2018 10:37:51,089 DEBUG(1): hydratk.core.corehead.CoreHead._stop_app:[0]: Stopping application
     01/06/2018 10:37:52,101 DEBUG(1): hydratk.core.masterhead.MasterHead.destroy_core_threads:[0]: Destroying core thread id: 1
     01/06/2018 10:37:52,141 DEBUG(1): hydratk.core.corehead.CoreHead._c_worker:[1]: Terminating work
     01/06/2018 10:37:52,170 DEBUG(1): hydratk.core.masterhead.MasterHead.destroy_core_threads:[0]: Destroying core thread id: 2
     01/06/2018 10:37:52,261 DEBUG(1): hydratk.core.corehead.CoreHead._c_worker:[2]: Terminating work
     01/06/2018 10:37:52,282 DEBUG(1): hydratk.core.masterhead.MasterHead.destroy_core_threads:[0]: Destroying core thread id: 3
     01/06/2018 10:37:52,702 DEBUG(1): hydratk.core.corehead.CoreHead._c_worker:[3]: Terminating work
     01/06/2018 10:37:52,771 DEBUG(1): hydratk.core.masterhead.MasterHead.destroy_core_threads:[0]: Destroying core thread id: 4
     01/06/2018 10:37:53,119 DEBUG(1): hydratk.core.corehead.CoreHead._c_worker:[4]: Terminating work
     01/06/2018 10:37:53,129 DEBUG(1): hydratk.core.corehead.CoreHead._c_observer:[0]: PID file deleted: /tmp/hydratk/hydratk.pid
     01/06/2018 10:37:53,131 DEBUG(1): hydratk.extensions.physolver.bootstrapper.run_app:[0]: Application exit
     
Unit tests
^^^^^^^^^^

htk supports unit testing using Yoda extension. 
See example hydratk/tests/hydratk/extensions/benchmark/benchmark/01_methods_ut.jedi                                                                                                                                                                                                            