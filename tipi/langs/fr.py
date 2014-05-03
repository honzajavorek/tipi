# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

"""
French typography
"""


import re

from .base import base_replacements


__all__ = ('replacements',)


ch = r'A-Za-z\u00C0-\u02FF\u0370-\u1EFF'

replacements = base_replacements + (
    # double ""
    (
        re.compile(r'(?<!"|\w)"(?! |")((?:[^"]+?|")+?)'
                   r'(?<! |")"(?!["{0}])()'.format(ch), re.U),
        '\u00AB\\1\u00BB'
    ),
    # single ''
    (
        re.compile(r"(?<!'|\w)'(?! |')((?:[^']+?|')+?)"
                   r"(?<! |')'(?!['{0}])()".format(ch), re.U),
        '\u2039\\1\u203A'
    ),
)
