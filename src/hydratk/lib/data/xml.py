# -*- coding: utf-8 -*-
"""This code is a part of Hydra Toolkit library

.. module:: lib.data.xmlgen
   :platform: Unix
   :synopsis: Utilities for advanced work and validation of xml data format
.. moduleauthor:: Petr Czaderna <pc@hydratk.org>

"""
from lxml import etree
from hydratk.lib.system import fs
import os
from hydratk.lib.exceptions.inputerror import InputError

class XMLValidate(object):
    _xml_schema = None
    
    def xsd_validate_file(self, xml_file):
        if os.path.exists(xml_file) and os.path.isfile(xml_file):
            content = fs.file_get_contents(xml_file)
            self.xsd_validate(content)
        else:
            raise InputError("File doesn't exists: {0}".format(file))
    
    def xsd_validate(self, xml_str):
        if xml_str not in (None,''):
            doc = etree.fromstring(xml_str)
            self._xml_schema.assertValid(doc)
            
    def load_xsd_file(self, xsd_file):
        if os.path.exists(xsd_file) and os.path.isfile(xsd_file):
            content = fs.file_get_contents(xsd_file)
            self.load_xsd(content)
    
    def load_xsd(self, xsd_str):
        if xsd_str is not None and xsd_str != '':
            doc = etree.fromstring(xsd_str)
            self._xml_schema = etree.XMLSchema(doc)
