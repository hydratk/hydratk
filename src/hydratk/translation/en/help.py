# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.en.messages
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
   'create-config-db' : 'creates configuration database'
}

help_cmd_args = {
   'help' : '<command>'
}

''' Hydra Native Options '''
help_opt = {
   'debug'             : { '{h}-d, --debug <level>{e}' : 'debug turned on with specified level > 0' },
   'config'            : { '{h}-c, --config <file>{e}' : 'reads the alternate configuration file' },
   'force'             : { '{h}-f, --force{e}' : 'enforces command' },
   'language'          : { '{h}-l, --language <language>{e}' : 'sets the text output language, for the list of available languages check the docs' },
   'cluster'           : { '{h}-x, --cluster{e}' :  { 'description' : 'activates cluster mode', 'commands' : ('start')}},
   'cluster-node-type' : { '{h}-t, --cluster-node-type <type>{e}' : { 'description' : 'sets the application node type in cluster mode, available types are: hub, leaf', 'commands' : ('start')}},
   'config-db-file'    : { '{h}--config-db-file <file>{e}' :  { 'description' : 'optional, database file path', 'commands' : ('create-config-db')}}
}