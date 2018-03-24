# -*- coding: utf-8 -*-
"""Useful module for solving Python 2 and 3 compatibility problems
 
 .. module:: lib.compat.contentfix
    :platform: Unix
    :synopsis: Useful module for solving Python 2 and 3 content encoding/decoding compatibility problems
 .. moduleauthor:: Petr Czaderna <pc@hydratk.org>
 
"""

import codecs


def slash_escape(err):
    """Function escapes undecoded part of unicode data, codec error handler

    Args:
       err (obj): UnicodeDecode instance

    Returns:
       tuple: str (undecoded part), int (position where encoding should continue)

    """

    thebyte = err.object[err.start:err.end]
    repl = u'\\x' + hex(ord(thebyte))[2:]
    return (repl, err.end)

codecs.register_error('slash_escape', slash_escape)
