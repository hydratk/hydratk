# -*- coding: utf-8 -*-
"""Module for string operations

.. module:: lib.string.operation
   :platform: Unix
   :synopsis: Module for string operations
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

import unicodedata
import re

def mreplace(text, dic): 
    """ Replace in 'text' all occurences of any key in the given
    dictionary by its corresponding value.  Returns the new string.
    
    Args:
       text (str): text
       dic (dict): key - search, value - replace
       
    Returns:
       str: text
    
    """
         
    import re
    regex = re.compile("(%s)" % "|".join(map(re.escape, dic.keys())))    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: str(dic[mo.string[mo.start():mo.end()]]), text)

def str_split(string, split_length=1):
    """Method splits string to substrings
    
    Args:
       string (str): original string
       split_length (int): substrin length     
               
    Returns:            
       list: list of strings  
    
    """
            
    return list(filter(None, re.split('(.{1,%d})' % split_length, string)))


def strip_accents(text):
    """Function strip accents from input text
    
    Args:
       text (str): Input text string        
               
    Returns:            
       str: text  
    
    """
    
    try:
        
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)
