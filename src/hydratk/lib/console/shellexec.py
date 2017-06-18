"""This code is a part of Hydra Toolkit library

.. module:: lib.console.shellexec
   :platform: Unix
   :synopsis: Module for several solutions of shell command execution
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

def shell_exec(command, get_output = False):
    """Method executes shell command and returns output

    Args:   
       command (str): command
       get_output (bool): get output         

    Returns:
       int command return code or tuple (return_code, stout, stderr)

    """    
    from subprocess import Popen, PIPE
    p = Popen(command , shell=True, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()    
    return (p.returncode, out, err) if get_output == True else p.returncode 
    