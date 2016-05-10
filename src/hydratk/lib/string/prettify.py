# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit library

.. module:: lib.string.prettify
   :platform: Unix
   :synopsis: Module for string pretty formatting
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""

def xml_prettify(xml_str):
    """Method reformats xml to use indentation
    
    Args:
       xml_str (str): raw xml  
               
    Returns:            
       str: indented xml  
    
    """
        
    from xml.dom.minidom import parseString
    reparsed = parseString(xml_str)
    return '\n'.join([line for line in reparsed.toprettyxml(indent=' '*2).split('\n') if line.strip()])