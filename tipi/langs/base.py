# -*- coding: utf-8 -*- #
"""
Basic typography rules

Most regular expressions inspired by
`texytypo.py <https://gist.github.com/msgre/3805872>`, which is Python port
of typography rules from `Texy! <https://github.com/dg/texy/>`_ project.
"""


import re


__all__ = ('base_replacements',)


ch = ur'A-Za-z\u00C0-\u02FF\u0370-\u1EFF'

base_replacements = (
    # ellipsis ...
    (
        re.compile(ur'(?<![.\u2026])\.{3,4}(?![.\u2026])', re.M | re.U),
        u'\u2026'
    ),
    # en dash 123-123
    (
        re.compile(ur'(?<=[\d ])-(?=[\d ]|$)'),
        u'\u2013'
    ),
    # en dash alphanum--alphanum
    (
        re.compile(ur'(?<=[^!*+,/:;<=>@\\\\_|-])--(?=[^!*+,/:;<=>@\\\\_|-])'),
        u'\u2013'
    ),
    # en dash ,-
    (
        re.compile(ur',-'),
        ur",\u2013"
    ),
    # em dash ---
    (
        re.compile(ur' --- '),
        u'\u00a0\u2014 '
    ),
    # &nbsp; before dash (dash stays at line end)
    (
        re.compile(ur' ([\u2013\u2014])', re.U),
        ur'\u00a0\1'
    ),
    # left right arrow <-->
    (
        re.compile(ur' <-{1,2}> '),
        u' \u2194 '
    ),
    # right arrow -->
    (
        re.compile(ur' ?-{1,}> '),
        u' \u2192 '
    ),
    # left arrow <--
    (
        re.compile(ur' <-{1,} ?'),
        u' \u2190 '
    ),
    # right arrow ==>
    (
        re.compile(ur' ?={1,}> '),
        u' \u21d2 '
    ),
    # +-
    (
        re.compile(ur'\+-'),
        ur'\u00b1'
    ),
    # dimension sign 123 x 123...
    (
        re.compile(ur'(\d+) x (?=\d)'),
        ur'\1 \u00d7 '
    ),
    # dimension sign 123x
    (
        re.compile(ur'(?<=\d)x(?= |,|.|$)', re.M),
        ur'\u00d7'
    ),
    # trademark (TM)
    (
        re.compile(ur'((?<=\S)|(?<=\S ))\(TM\)', re.I),
        ur'\u2122'
    ),
    # registered (R)
    (
        re.compile(ur'((?<=\S)|(?<=\S ))\(R\)', re.I),
        ur'\u00ae'
    ),
    # copyright (C)
    (
        re.compile(ur'\(C\)((?=\S)|(?= \S))', re.I),
        ur'\u00a9'
    ),
    # Euro (EUR)
    (
        re.compile(ur'\(EUR\)'),
        ur'\u20ac'
    ),
    # (phone) number 1 123 123 123...
    (
        re.compile(ur'(\d) (?=\d{3})'),
        ur'\1\u00a0'
    ),
    # space before last short word
    (
        re.compile(
            ur'(?<=.{50})\s+(?=[\x17-\x1F]*\S{1,6}[\x17-\x1F]*$)',
            re.S | re.U
        ),
        u'\u00a0'
    ),
    # nbsp space between number (optionally followed by dot) and word, symbol,
    # punctation, currency symbol
    (
        re.compile(
            (ur'(?<= |\.|,|-|\+|\x16|\()([\x17-\x1F]*\d+\.?[\x17-\x1F]*)\s+'
             ur'(?=[\x17-\x1F]*[%{0}\u00B0-\u00be\u2020-\u214f])').format(ch),
            re.M | re.U
        ),
        ur'\1\u00a0',
    ),
    (
        re.compile(
            (ur'(?<=\d\u00A0)([\x17-\x1F]*\d+\.?[\x17-\x1F]*)\s+'
             ur'(?=[\x17-\x1F]*[%{0}\u00B0-\u00be\u2020-\u214f])').format(ch),
            re.M | re.U
        ),
        ur'\1\u00a0'
    ),
)
