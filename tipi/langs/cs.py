# -*- coding: utf-8 -*- #
"""
Czech typography

Most regular expressions inspired by
`texytypo.py <https://gist.github.com/msgre/3805872>`, which is Python port
of typography rules from `Texy! <https://github.com/dg/texy/>`_ project.
"""


import re

from .base import base_replacements


__all__ = ('replacements',)


ch = ur'A-Za-z\u00C0-\u02FF\u0370-\u1EFF'

replacements = base_replacements + (
    # date 23. 1. 1978
    (
        re.compile(ur'(?<!\d)(\d{1,2}\.) (\d{1,2}\.) (\d\d)'),
        ur'\1\u00a0\2\u00a0\3'
    ),
    # date 23. 1.
    (
        re.compile(ur'(?<!\d)(\d{1,2}\.) (\d{1,2}\.)'),
        ur'\1\u00a0\2'
    ),
    # space between preposition and word
    (
        re.compile(
            (ur'(?<=[^0-9{0}])([\x17-\x1F]*[ksvzouiaKSVZOUIA][\x17-\x1F]*)'
             ur'\s+(?=[\x17-\x1F]*[0-9{0}])').format(ch),
            re.M | re.U | re.S
        ),
        ur'\1\u00a0'
    ),
    # double ""
    (
        re.compile(ur'(?<!"|\w)"(?! |")((?:[^"]+?|")+?)'
                   ur'(?<! |")"(?!["{0}])()'.format(ch), re.U),
        ur'\u201E\1\u201C'
    ),
    # single ''
    (
        re.compile(ur"(?<!'|\w)'(?! |')((?:[^']+?|')+?)"
                   ur"(?<! |')'(?!['{0}])()".format(ch), re.U),
        ur'\u201A\1\u2018'
    ),
)
