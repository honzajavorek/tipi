# -*- coding: utf-8 -*- #

"""
French typography
"""


import re

from .base import base_replacements


__all__ = ('replacements',)


ch = ur'A-Za-z\u00C0-\u02FF\u0370-\u1EFF'

replacements = base_replacements + (
    # double ""
    (
        re.compile(ur'(?<!"|\w)"(?! |")((?:[^"]+?|")+?)'
                   ur'(?<! |")"(?!["{0}])()'.format(ch), re.U),
        ur'\u00AB\1\u00BB'
    ),
    # single ''
    (
        re.compile(ur"(?<!'|\w)'(?! |')((?:[^']+?|')+?)"
                   ur"(?<! |')'(?!['{0}])()".format(ch), re.U),
        ur'\u2039\1\u203A'
    ),
)
