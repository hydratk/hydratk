# -*- coding: utf-8 -*-

"""This code is a part of HydraTk (Hydra Toolkit)

.. module:: hydratk.translation.cs.help
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
   'create-config-db' : 'vytvoří konfigurační databázi',
   'create-ext-skel'  : 'vytvoří projektovou kostru pro vývoj HydraTK rozšíření',
   'create-lib-skel'  : 'vytvoří projektovou kostru pro vývoj HydraTK knihovny',          
}

help_cmd_args = {
   'help' : '<příkaz>'
}

''' Hydra Native Options '''
help_opt = {
   'debug'             : { '{h}-d, --debug <level>{e}' : 'zapnutí režimu ladění s úrovní > 0' },
   'debug-channel'     : { '{h}-e, --debug-channel <číslo kanálu, ..>{e}' : 'zapnutí filtru pro režim ladění' },
   'config'            : { '{h}-c, --config <soubor>{e}' : 'načte alternativní konfigurační soubor' },
   'force'             : { '{h}-f, --force{e}' : 'zvyšuje důraz na provedení příkazu' },
   'interactive'       : { '{h}-i, --interactive{e}' : 'zapne interaktivní režim' },
   'language'          : { '{h}-l, --language <jazyk>{e}' : 'nastaví standardní jazyk, seznam dostupných jazyků je uveden v dokumentaci' }, 
   'run-mode'          : { '{h}-m, --run-mode <mode>{e}' : 'nastaví režim spuštění, seznam dostupných režimů je uveden v dokumentaci' },
   'profile'           : { '{h}-p, --profile <soubor>{e}' : 'zapne cProfiler a výstup měření uloži do zvoleného souboru' },
   'config-db-file'    : { '{h}--config-db-file <soubor>{e}' : { 'description' : 'volitelné, cesta k souboru databáze', 'commands' : ('create-config-db')}},
   'ext-skel-path'     : { '{h}--ext-skel-path <cesta>{e}' : { 'description' : 'volitelné, cesta k adresáři kde bude vytvořena kostra rozšíření HydraTK', 'commands' : ('create-ext-skel')}},
   'lib-skel-path'     : { '{h}--lib-skel-path <cesta>{e}' : { 'description' : 'volitelné, cesta k adresáři kde bude vytvořena kostra knihovny HydraTK', 'commands' : ('create-lib-skel')}}
      
}            
