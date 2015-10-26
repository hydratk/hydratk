# -*- coding: utf-8 -*-
'''
Created on 9.3.2014

@author: Petr
'''
from os import path
import crypt
from re import compile as compile_regex

def check_auth(user, password):
    """Perform authentication against the local systme.

    This function will perform authentication against the local system's
    /etc/shadow or /etc/passwd database for a given user and password.

    :param user: The username to perform authentication with
    :type user: str

    :param password: The password (plain text) for the given user
    :type password: str

    :returns: True if successful, None otherwise.
    :rtype: True or None
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