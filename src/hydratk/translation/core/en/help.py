# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.en.help
   :platform: Unix
   :synopsis: English language translation for help generator
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

language = {
  'name' : 'English',
  'ISO-639-1' : 'en'
}

''' Hydra Native Commands '''

help_cmd = { 
   'start'            : 'starts the application',
   'stop'             : 'stops the application',
   'help'             : 'prints help',
   'list-extensions'  : 'displays list of loaded extensions',
   'create-config-db' : 'creates configuration database',
   'create-ext-skel'  : 'creates project skeleton for HydraTK extension development',
   'create-lib-skel'  : 'creates project skeleton for HydraTK library development'   
}

help_cmd_args = {
   'help' : '<command>'
}

''' Hydra Native Options '''
help_opt = {
   'debug'             : { '{h}-d, --debug <level>{e}' : 'debug turned on with specified level > 0' },
   'config'            : { '{h}-c, --config <file>{e}' : 'reads the alternate configuration file' },
   'force'             : { '{h}-f, --force{e}' : 'enforces command' },
   'interactive'       : { '{h}-i, --interactive{e}' : 'turns on interactive mode' },
   'language'          : { '{h}-l, --language <language>{e}' : 'sets the text output language, for the list of available languages check the docs' },   
   'config-db-file'    : { '{h}--config-db-file <file>{e}' :  { 'description' : 'optional, database file path', 'commands' : ('create-config-db')}},
   'ext-skel-path'     : { '{h}--ext-skel-path <path>{e}' : { 'description' : 'volitelné, cesta k adresáři kde bude vytvořena kostra rozšíření HydraTK', 'commands' : ('create-ext-skel')}},
   'lib-skel-path'     : { '{h}--lib-skel-path <path>{e}' : { 'description' : 'volitelné, cesta k adresáři kde bude vytvořena kostra knihovny HydraTK', 'commands' : ('create-lib-skel')}}
}