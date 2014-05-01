# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

"""
Basic typography rules

Most regular expressions inspired by
`texytypo.py <https://gist.github.com/msgre/3805872>`, which is Python port
of typography rules from `Texy! <https://github.com/dg/texy/>`_ project.
"""


import re


__all__ = ('base_replacements',)


ch = r'A-Za-z\u00C0-\u02FF\u0370-\u1EFF'

base_replacements = (
    # ellipsis ...
    (
        re.compile(r'(?<![.\u2026])\.{3,4}(?![.\u2026])', re.M | re.U),
        '\u2026'
    ),
    # en dash 123-123
    (
        re.compile(r'(?<=[\d ])-(?=[\d ]|$)'),
        '\u2013'
    ),
    # en dash alphanum--alphanum
    (
        re.compile(r'(?<=[^!*+,/:;<=>@\\\\_|-])--(?=[^!*+,/:;<=>@\\\\_|-])'),
        '\u2013'
    ),
    # en dash ,-
    (
        re.compile(r',-'),
        ",\u2013"
    ),
    # em dash ---
    (
        re.compile(r' --- '),
        '\u00a0\u2014 '
    ),
    # &nbsp; before dash (dash stays at line end)
    (
        re.compile(r' ([\u2013\u2014])', re.U),
        '\u00a0\\1'
    ),
    # left right arrow <-->
    (
        re.compile(r' <-{1,2}> '),
        ' \u2194 '
    ),
    # right arrow -->
    (
        re.compile(r' ?-{1,}> '),
        ' \u2192 '
    ),
    # left arrow <--
    (
        re.compile(r' <-{1,} ?'),
        ' \u2190 '
    ),
    # right arrow ==>
    (
        re.compile(r' ?={1,}> '),
        ' \u21d2 '
    ),
    # +-
    (
        re.compile(r'\+-'),
        '\u00b1'
    ),
    # dimension sign 123 x 123...
    (
        re.compile(r'(\d+) x (?=\d)'),
        '\\1 \u00d7 '
    ),
    # dimension sign 123x
    (
        re.compile(r'(?<=\d)x(?= |,|.|$)', re.M),
        '\u00d7'
    ),
    # trademark (TM)
    (
        re.compile(r'((?<=\S)|(?<=\S ))\(TM\)', re.I),
        '\u2122'
    ),
    # registered (R)
    (
        re.compile(r'((?<=\S)|(?<=\S ))\(R\)', re.I),
        '\u00ae'
    ),
    # copyright (C)
    (
        re.compile(r'\(C\)((?=\S)|(?= \S))', re.I),
        '\u00a9'
    ),
    # Euro (EUR)
    (
        re.compile(r'\(EUR\)'),
        '\u20ac'
    ),
    # (phone) number 1 123 123 123...
    (
        re.compile(r'(\d) (?=\d{3})'),
        '\\1\u00a0'
    ),
    # space before last short word
    (
        re.compile(
            r'(?<=.{50})\s+(?=[\x17-\x1F]*\S{1,6}[\x17-\x1F]*$)',
            re.S | re.U
        ),
        '\u00a0'
    ),
    # nbsp space between number (optionally followed by dot) and word, symbol,
    # punctation, currency symbol
    (
        re.compile(
            (r'(?<= |\.|,|-|\+|\x16|\()([\x17-\x1F]*\d+\.?[\x17-\x1F]*)\s+'
             r'(?=[\x17-\x1F]*[%{0}\u00B0-\u00be\u2020-\u214f])').format(ch),
            re.M | re.U
        ),
        '\\1\u00a0',
    ),
    (
        re.compile(
            (r'(?<=\d\u00A0)([\x17-\x1F]*\d+\.?[\x17-\x1F]*)\s+'
             r'(?=[\x17-\x1F]*[%{0}\u00B0-\u00be\u2020-\u214f])').format(ch),
            re.M | re.U
        ),
        '\\1\u00a0'
    ),
)
