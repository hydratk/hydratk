# -*- coding: utf-8 -*-

"""This code is a part of Hydra Toolkit

.. module:: hydratk.translation.cs.messages
   :platform: Unix
   :synopsis: Czech language translation for help generator
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
language = {
  'name' : 'Čeština',
  'ISO-639-1' : 'cs'
} 

''' HydraTK Native Commands '''
help_cmd = {
   'start'            : 'spustí aplikaci',          
   'stop'             : 'zastaví aplikaci',         
   'help'             : 'zobrazí nápovědu',         
   'list-extensions'  : 'zobrazí seznam aktivních rozšíření',   
   'create-config-db' :'vytvoří konfigurační databázi'         
}

help_cmd_args = {
   'help' : '<příkaz>'
}

''' Hydra Native Options '''
help_opt = {
   'debug'             : { '{h}-d, --debug <level>{e}' : 'zapnutí režimu ladění s úrovní > 0' },
   'config'            : { '{h}-c, --config <soubor>{e}' : 'načte alternativní konfigurační soubor' },
   'force'             : { '{h}-f, --force{e}' : 'zvyšuje důraz na provedení příkazu' },
   'language'          : { '{h}-l, --language <jazyk>{e}' : 'nastaví standardní jazyk, seznam dostupných jazyků najdete v dokumentaci' },
   'cluster'           : { '{h}-x, --cluster{e}' : { 'description' : 'aktivuje režim cluster', 'commands' : ('start')}},
   'cluster-node-type' : { '{h}-t, --cluster-node-type <typ>{e}' : { 'description' : 'nastaví typ nodu aplikace v režimu cluster, dostupné typy jsou: hub, leaf', 'commands' : ('start')}},
   'config-db-file'    : { '{h}--config-db-file <soubor>{e}' : { 'description' : 'volitelné, cesta k souboru databáze', 'commands' : ('create-config-db')}}
}            
