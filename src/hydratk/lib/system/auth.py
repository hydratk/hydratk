# -*- coding: utf-8 -*-
"""Module for user authentication

.. module:: lib.system.auth
   :platform: Unix
   :synopsis: Module for user authentication
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

from os import path
import crypt
from re import compile as compile_regex

def check_auth(user, password):
    """Perform authentication against the local systme.

    This function will perform authentication against the local system's
    /etc/shadow or /etc/passwd database for a given user and password.

    Args:
       user (str): The username to perform authentication with
       password (str): The password (plain text) for the given user

    Returns:
       bool: result
    
    """

    salt_pattern = compile_regex(r"\$.*\$.*\$")
    passwd = "/etc/shadow" if path.exists("/etc/shadow") else "/etc/passwd"
    result = False
    
    with open(passwd, "r") as f:
        rows = (line.strip().split(":") for line in f)
        records = [row for row in rows if row[0] == user]
    '''check if user exists'''    
    if (isinstance(records, list) and len(records) > 0 and records[0][0] == user): 
        hashv = records and records[0][1]
        salt = salt_pattern.match(hashv).group()
        result = crypt.crypt(password, salt) == hashv
    return result