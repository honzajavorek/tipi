# -*- coding: utf-8 -*- #

"""
Polish typography
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
        ur'\u201E\1\u201D'
    ),
    # single ''
    (
        re.compile(ur"(?<!'|\w)'(?! |')((?:[^']+?|')+?)"
                   ur"(?<! |')'(?!['{0}])()".format(ch), re.U),
        ur'\u201A\1\u2019'
    ),
)
