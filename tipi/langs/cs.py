# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

"""
Czech typography

Most regular expressions inspired by
`texytypo.py <https://gist.github.com/msgre/3805872>`, which is Python port
of typography rules from `Texy! <https://github.com/dg/texy/>`_ project.
"""


import re

from .base import base_replacements


__all__ = ('replacements',)


ch = r'A-Za-z\u00C0-\u02FF\u0370-\u1EFF'

replacements = base_replacements + (
    # date 23. 1. 1978
    (
        re.compile(r'(?<!\d)(\d{1,2}\.) (\d{1,2}\.) (\d\d)'),
        '\\1\u00a0\\2\u00a0\\3'
    ),
    # date 23. 1.
    (
        re.compile(r'(?<!\d)(\d{1,2}\.) (\d{1,2}\.)'),
        '\\1\u00a0\\2'
    ),
    # space between preposition and word
    (
        re.compile(
            (r'(?<=[^0-9{0}])([\x17-\x1F]*[ksvzouiaKSVZOUIA][\x17-\x1F]*)'
             r'\s+(?=[\x17-\x1F]*[0-9{0}])').format(ch),
            re.M | re.U | re.S
        ),
        '\\1\u00a0'
    ),
    # double ""
    (
        re.compile(r'(?<!"|\w)"(?! |")((?:[^"]+?|")+?)'
                   r'(?<! |")"(?!["{0}])()'.format(ch), re.U),
        '\u201E\\1\u201C'
    ),
    # single ''
    (
        re.compile(r"(?<!'|\w)'(?! |')((?:[^']+?|')+?)"
                   r"(?<! |')'(?!['{0}])()".format(ch), re.U),
        '\u201A\\1\u2018'
    ),
)
