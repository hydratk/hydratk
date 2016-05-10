# -*- coding: utf-8 -*-
"""This code is a part of Hydra toolkit

.. module:: install.command
   :platform: Unix
   :synopsis: Module for common commands used in installation tasks
.. moduleauthor:: Petr Rašek <bowman@hydratk.org>

"""

from config import config as cfg
from subprocess import call, Popen, PIPE
from os import remove, environ, path
from shutil import move as mv
import cmd

def get_pck_manager():
    """Method detects package managers

    Args:

    Returns:
       list: managers
    
    """    
    
    pck_managers = ['apt-get', 'yum']
    
    pckm = []
    for pck in pck_managers:     
        if (is_installed(pck)):
            pckm.append(pck) 
    
    return pckm

def is_installed(app):
    """Method checks if application is installed

    Args:
       app (str): application

    Returns:
       bool: result
    
    """      
    
    cmd = ['which', app]
    proc = Popen(cmd, stdout=PIPE)
    out = proc.communicate() 
    
    result = True if (len(out[0]) > 0) else False
    return result    

def install_pck(pckm, pck):
    """Method installs package

    Args:
       pckm (str): package manager, apt-get|yum
       pck (str): package name

    Returns:
       void
    
    """     
    
    print('Installing package: {0}'.format(pck))
    
    if (pckm == 'apt-get'):
        cmd = 'apt-get -y install {0}'.format(pck)
    elif (pckm == 'yum'):
        cmd = 'yum install {0}'.format(pck)
        
    if (call(cmd, shell=True) != 0):
        print('Failed to install package {0}'.format(pck)) 
        
def ask_module(module):
    """Method asks if user wants to install module

    Args:
       module (str): python module

    Returns:
       bool: result
    
    """     
    
    print('Do you want to install module: {0}'.format(module))
    choice = raw_input('[Y]:')
    result = True if (len(choice) == 0 or choice == 'Y') else False
    return result                
        
def ask_install(app):
    """Method asks if user wants to install application

    Args:
       app (str): application

    Returns:
       bool: result
    
    """     
    return True

    print('{0} not installed, do you want to install it ?'.format(app))
    choice = raw_input('[Y]:')
    result = True if (len(choice) == 0 or choice == 'Y') else False
    return result        
        
def set_inst_dir(): 
    """Method sets installation directory

    Args:

    Returns:
       str: directory
    
    """ 
         
    return cfg['os']['inst_dir'] #workaround to make pip installer working

    print('Choose install directory')
    dir = raw_input('[{0}]:'.format(cfg['os']['inst_dir']))  
    dir = dir if (len(dir) > 0) else cfg['os']['inst_dir']
    return dir   

def download_pck(url, options=None, outfile=None):
    """Method downloads package

    Args:
       url (str): download url
       options (str): download options for wget command
       outfile (str): output filename

    Returns:
       void
    
    """     
    
    print('Downloading package: {0}'.format(url))
    
    outfile = url if (outfile == None) else outfile
    if (options != None):
        cmd = 'wget {0} {1} -O {2}'.format(options, url, outfile)
    else:
        cmd = 'wget {0} -O {1}'.format(url, outfile) 
        
    if (call(cmd, shell=True) != 0):
        print('Failed to download package {0}'.format(url))                         

def move(src, dst=None, dir=cfg['os']['inst_dir']): 
    """Method moves directory

    Args:
       src (str): source directory name
       dst (str): destination directory name including path
       dir (str): destination directory

    Returns:
       void
    
    """     
    
    path = '{0}/{1}'.format(dir, dst) if (dst != None) else '{0}/{1}'.format(dir, src)
    print('Moving {0} to {1}'.format(src, path))  
    mv(src, path)  
        
def delete(path): 
    """Method deletes directory

    Args:
       path (str): directory path

    Returns:
       void
    
    """       
    
    print('Deleting {0}'.format(path)) 
    remove(path)   
        
def decompress(path, method='tar'):
    """Method decompresses archive

    Args:
       path (str): archive path
       method (str): decompressing method, tar|zip|gzip|bzip

    Returns:
       void
    
    """         
    
    print('Decompressing file: {0}').format(path)  
    
    if (method == 'tar'):
        cmd = 'tar -xf {0}'.format(path)
    elif (method == 'zip'):
        cmd = 'unzip {0}'.format(path)
    elif (method == 'gzip'):
        cmd = 'gunzip {0}'.format(path)
    elif (method == 'bzip'):
        cmd = 'bunzip2 {0}'.format(path)
    
    if (call(cmd, shell=True) != 0):
        print('Failed to decompress file {0}'.format(file))                                                       
           
def set_rights(path, rights, recursive=True):
    """Method sets acces rights

    Args:
       path (str): directory or file path
       rights (str): access rights in Unix style
       recursive (bool): set recursive rights

    Returns:
       void
    
    """     
    
    print('Setting rights for {0}'.format(path))
    
    if (recursive):
        cmd = 'chmod -R {0} {1}'.format(rights, path)
    else:
        cmd = 'chmod {0} {1}'.format(rights, path)
        
    if (call(cmd, shell=True) != 0):
        print('Failed to set rights for {0}'.format(path))
        
def setenv(var, value, cfg=cfg['os']['profile']):  
    """Method sets environment variable

    Args:
       var (str): variable name
       value (str): variable value
       cfg (str): configuation file

    Returns:
       void
    
    """     
    
    print('Setting environment variable: {0}={1}'.format(var, value))

    with open(cfg) as f:
        cont = f.read()
        if (var in environ):
            env = '{0}=${1}:{2}'.format(var, var, value)
        else:
            env = '{0}={1}'.format(var, value)

    if (not env in cont):
        with open(cfg, 'a') as f:
            f.write(env+'\n')       

    if (var in environ):
        environ[var] += ':{0}'.format(value)
    else:
        environ[var] = value
        
def create_symlink(dir, src, link):
    """Method creates symbolic link

    Args:
       dir (str): source directory
       src (str): source name
       link (str): link name

    Returns:
       void
    
    """     
    
    print('Creating symlink {0} for {1}'.format(link, src))
    cmd = 'ln -s {0} {1}'.format(src, link)
    
    if (call(cmd, cwd=dir, shell=True) != 0):
        print('Failed to create symlink {0}'.format(link))   
        
def ldconfig(app, dir, cfg=cfg['os']['ldconfig']):
    """Methods adds application to ldconfig

    Args:
       app (str): application library
       dir (str): source directory
       cfg (str): ldconfig configuration file

    Returns:
       void
    
    """     
    
    cmd = 'ldconfig'
    print('Adding {0} to {1}'.format(dir, cmd))
    
    cfg_file = '{0}/{1}.conf'.format(cfg, app)
    if (not path.exists(cfg_file)):
        with open(cfg_file, 'w') as f:
            f.write(dir+'\n')
        
    if (call(cmd, shell=True) != 0):
        print('Failed to call {0}'.format(cmd))             
        
def compile_java_class(dir, file, classpath=None):   
    """Method compiles Java class

    Args:
       dir (str): source directory
       file (str): Java filename
       classpath (str): classpath used in compilation

    Returns:
       void
    
    """      
    
    print('Compiling {0}'.format(file))
    
    if (classpath != None):
        cmd = 'javac -cp {0} {1}'.format(classpath, file)
    else:
        cmd = 'javac {0}'.format(file)
        
    if (call(cmd, cwd=dir, shell=True) != 0):
        print('Failed to compile {0}'.format(file))         