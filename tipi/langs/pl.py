# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

"""
Polish typography
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
        '\u201E\\1\u201D'
    ),
    # single ''
    (
        re.compile(r"(?<!'|\w)'(?! |')((?:[^']+?|')+?)"
                   r"(?<! |')'(?!['{0}])()".format(ch), re.U),
        '\u201A\\1\u2019'
    ),
)
