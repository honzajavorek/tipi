# -*- coding: utf-8 -*-


import re

from tipi.repl import Replacement, replace


def test_simple_replace():
    s = 'Whose <strong class="vehicle">motorcycle</strong> is this?'
    replacements = (
        Replacement(re.compile(r'(motorcycle) (is)'), ur'\1\u00a0\2'),
    )
    assert (
        replace(s, replacements)
        ==
        u'Whose <strong class="vehicle">motorcycle</strong>\u00a0is this?'
    )


def test_multiple_replace():
    s = 'Whose <strong class="vehicle">motorcycle</strong> is this?'
    replacements = (
        Replacement(re.compile(r'motorcycle'), ur'motor-cycle'),
        Replacement(re.compile(r' '), ur'\u00a0'),
    )
    assert (
        replace(s, replacements)
        ==
        (u'Whose\u00a0<strong class="vehicle">motor-cycle'
         u'</strong>\u00a0is\u00a0this?')
    )


def test_replace_everywhere():
    s = 'Whose <strong>motorcycle</strong> motorcycle is this?'
    replacements = (
        Replacement(re.compile(r'motorcycle'), ur'motor-cycle'),
    )
    assert (
        replace(s, replacements)
        ==
        ('Whose <strong>motor-cycle</strong> motor-cycle is this?')
    )


def test_replace_inside_given_tags_only():
    s = 'Whose <b>motorcycle</b> motorcycle is this?'
    replacements = (
        Replacement(re.compile(r'motorcycle'), ur'motor-cycle', ['b']),
    )
    assert (
        replace(s, replacements)
        ==
        ('Whose <b>motor-cycle</b> motorcycle is this?')
    )


def test_replace_outside_given_tags_only():
    s = (
        'Whose <i><b>motorcycle</b></i> '
        '<b>motorcycle</b> is this?'
    )
    replacements = (
        Replacement(re.compile(r'motorcycle'), ur'motor-cycle', ['-i']),
    )
    assert (
        replace(s, replacements)
        ==
        (
            'Whose <i><b>motorcycle</b></i> '
            '<b>motor-cycle</b> is this?'
        )
    )
