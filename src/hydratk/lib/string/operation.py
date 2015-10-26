'''
Created on 28.10.2009

@author: CzadernaP
'''
import re

def mreplace(text, dic): 
    """ Replace in 'text' all occurences of any key in the given
    dictionary by its corresponding value.  Returns the new string."""     
    import re
    regex = re.compile("(%s)" % "|".join(map(re.escape, dic.keys())))    # For each match, look-up corresponding value in dictionary
    return regex.sub(lambda mo: str(dic[mo.string[mo.start():mo.end()]]), text)

def str_split(string, split_length=1):
    return filter(None, re.split('(.{1,%d})' % split_length, string))
