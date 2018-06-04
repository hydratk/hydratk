# -*- coding: utf-8 -*-
"""Module for string pretty formatting

.. module:: lib.string.prettify
   :platform: Unix
   :synopsis: Module for string pretty formatting
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""


def dict_prettify(dict, left_indent=4, indent_level = 1, indent_chr = ' '):
    """Method formats  dictionary structure to the indented tree styled string 

    Args:
       dict (dict): dictionary variable 
       left_indent (int): number of indent spaces from left
       indent_chr (str): indent character, default is space character

    Returns:            
       result (str): indented tree styled string

    """
    result = ''
        
    if type(dict).__name__ != 'dict':
        raise TypeError('Invalid input type, dictionary expected got: {0}'.format(dict))
    
    result += left_indent * indent_level * indent_chr + "{\n"
    indent_level += 1
    
    for key, val in dict.items():
        if type(val).__name__ == 'dict':            
            result += left_indent * indent_level * indent_chr + "'{key}' : {val}".format(key=key,val=dict_prettify(val, left_indent, indent_level, indent_chr))            
        else:
            if type(val).__name__ == 'str':
                val = "'{0}'".format(val)
                                
            result += left_indent * indent_level * indent_chr + "'{key}' : {val},\n".format(key=key,val=val)
        
    indent_level -= 1
    
    result += left_indent * indent_level * indent_chr + "}\n"
    
    return result
        
    
def xml_prettify(xml_str):
    """Method reformats xml to use indentation

    Args:
       xml_str (str): raw xml  

    Returns:            
       str: indented xml  

    """

    from xml.dom.minidom import parseString
    reparsed = parseString(xml_str)
    return '\n'.join([line for line in reparsed.toprettyxml(indent=' ' * 2).split('\n') if line.strip()])
