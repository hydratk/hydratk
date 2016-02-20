# -*- coding: utf-8 -*-
"""This code is a part of Hydra toolkit

.. module:: install.pre_install
   :platform: Unix
   :synopsis: Module for pre-install tasks
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from config import config as cfg
import command as cmd
from os import path

def run_pre_install():
    
    print('**************************************')
    print('*    HydraTK installation wizard     *')
    print('**************************************')    
    
    prompt = ''
    modes = cfg['modes']
    for i in xrange(0, len(modes)):
        prompt += '{0} - {1}\n'.format(i+1, modes[i])
    
    print('Choose mode to install')
    try:
        mode = int(raw_input('{0}'.format(prompt)))        
    except ValueError:
        mode = 1
    mode = modes[mode-1] if (mode <= len(modes)) else 'basic'
    print('Mode {0} will be installed'.format(mode)) 
    
    modules = cfg['modules']
    files = cfg['files']
    if (mode == 'basic'):
        requires = modules[mode]
        data_files = files[mode]
    elif (mode == 'full'):
        requires = modules['basic'] + modules[mode]
        data_files = files['basic'] + files[mode]
    elif (mode == 'custom'):
        requires, data_files = set_custom_modules()
     
    print('**************************************') 
    print('*     Running pre-install tasks      *')    
    print('**************************************')
    
    for task in cfg['pre_tasks']:
        print('\n*** Running task: {0} ***\n'.format(task))
        
        if (task == 'install_java'):
            requires, data_files = globals()[task](requires, data_files)
        elif ('install' in task):
            requires = globals()[task](requires) 
        else:
            globals()[task]()          
    
    return (requires, data_files)  

def set_custom_modules():
    
    print('Non-basic modules will be offered to install')
    requires = cfg['modules']['basic']
    data_files = cfg['files']['basic']
    
    for module in cfg['modules']['full']:
        if (cmd.ask_module(module)):
            requires.append(module)
            
            if (module == 'JPype1'):
                for data in cfg['files']['full']:
                    if ('java' in data[0]):
                        data_files.append(data)
    
    return (requires, data_files) 

def install_libs_from_repo(requires):
    
    pckm = cmd.get_pck_manager()[0]
    
    libs = cfg['libs']
    for key in libs.keys():
        if (key in requires):
            lib_inst = []
            if (libs[key].has_key('repo')):
                lib_inst += libs[key]['repo']
            if (libs[key].has_key(pckm)):
                lib_inst += libs[key][pckm]
            for lib in lib_inst:
                cmd.install_pck(pckm, lib)  
                
    return requires
                
def install_java(requires, data_files):
    
    module = 'JPype1'
    alias = 'java'
    if (module in requires): 
        if (not cmd.is_installed(alias)):
            if (cmd.ask_install(alias)):
                conf = cfg['libs'][module]
                app = conf['file']
                url = '{0}/{1}'.format(conf['url'], app)
                options = '--header \"Cookie: oraclelicense=accept-securebackup-cookie\"'
                cmd.download_pck(url, options, app)
        
                cmd.decompress(app)
                dir = cmd.set_inst_dir()
                cmd.move(conf['dir'], alias, dir)
                cmd.setenv('JAVA_HOME', '{0}/{1}/bin'.format(cfg['os']['inst_dir'], alias))
                cmd.setenv('PATH', '$JAVA_HOME')
                cmd.delete(app)
            else:
                requires.remove(module)
                
                data_new = []
                for data in data_files:
                    if (not alias in data[0]):
                        data_new.append(data)
                data_files = data_new 
                        
        else:
            print('{0} already installed'.format(alias))          

    return (requires, data_files)

def install_oracle(requires):
    
    module = 'cx_Oracle'
    alias = 'instantclient'
    if (module in requires):
        if (not cmd.is_installed('sqlplus')):
            if (cmd.ask_install(alias)):
                cookies = 'cookies.txt'
                while (not path.exists(cookies)):
                    raw_input('Please login to Oracle website with your account.\nExport cookies and store them into {0}'.format(cookies))
                
                conf = cfg['libs'][module]
                dir = cmd.set_inst_dir()
                for i in xrange(0, len(conf['file'])):
                    app = conf['file'][i]
                    url = '{0}/{1}'.format(conf['url'], app)
                    options = '--load-cookies {0}'.format(cookies)        
                    cmd.download_pck(url, options, app)  
                    cmd.decompress(app, 'zip')                                    
                    cmd.delete(app)
                
                cmd.move(conf['dir'], alias, dir)
                dir = '{0}/{1}'.format(dir, alias)
                for src, link in conf['symlink'].items():
                    cmd.create_symlink(dir, src, link)
                
                cmd.setenv('ORACLE_HOME', '{0}/{1}'.format(cfg['os']['inst_dir'], alias))
                cmd.setenv('PATH', '$ORACLE_HOME')
                cmd.ldconfig(alias, dir)                
                cmd.delete(cookies)
            else:
                requires.remove(module)  
        else:
            print('{0} already installed'.format(alias))             
     
    return requires 
        
def install_phantomjs(requires):
    
    module = 'selenium'
    alias = 'phantomjs'
    if (module in requires):
        if (not cmd.is_installed(alias)):
            if (cmd.ask_install(alias)):
                conf = cfg['libs'][module]
                app = conf['file']
                url = '{0}/{1}'.format(conf['url'], app)
                cmd.download_pck(url, outfile=app)  
        
                cmd.decompress(app) 
                dir = cmd.set_inst_dir()           
                cmd.move(conf['dir'], alias, dir)
                cmd.setenv('PATH', '{0}/{1}/bin'.format(cfg['os']['inst_dir'], alias))
                cmd.delete(app)
            else:
                requires.remove(module)
        else:
            print('{0} already installed'.format(alias))   
      
    return requires                     