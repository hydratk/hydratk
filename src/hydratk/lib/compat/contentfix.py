# -*- coding: utf-8 -*-
"""Useful module for solving Python 2 and 3 compatibility problems
 
 .. module:: lib.compat.contentfix
    :platform: Unix
    :synopsis: Useful module for solving Python 2 and 3 content encoding/decoding compatibility problems
 .. moduleauthor:: Petr Czaderna <pc@hydratk.org>
 
"""

import codecs


def slash_escape(err):
    """ codecs error handler. err is UnicodeDecode instance. return
    a tuple with a replacement for the unencodable part of the input
    and a position where encoding should continue"""
    # print err, dir(err), err.start, err.end, err.object[:err.start]
    thebyte = err.object[err.start:err.end]
    repl = u'\\x' + hex(ord(thebyte))[2:]
    return (repl, err.end)

codecs.register_error('slash_escape', slash_escape)
