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


def test_default_filters():
    repls = [Replacement(re.compile(r'motorcycle'), ur'chopper')]

    assert (
        replace('<code><b>motorcycle</b></code> <b>motorcycle</b>', repls)
        == '<code><b>motorcycle</b></code> <b>chopper</b>'
    )
    assert (
        replace('<kbd><b>motorcycle</b></kbd> <b>motorcycle</b>', repls)
        == '<kbd><b>motorcycle</b></kbd> <b>chopper</b>'
    )
    assert (
        replace('<pre><b>motorcycle</b></pre> <b>motorcycle</b>', repls)
        == '<pre><b>motorcycle</b></pre> <b>chopper</b>'
    )
    assert (
        replace('<samp><b>motorcycle</b></samp> <b>motorcycle</b>', repls)
        == '<samp><b>motorcycle</b></samp> <b>chopper</b>'
    )
    assert (
        replace('<script><b>motorcycle</b></script> <b>motorcycle</b>', repls)
        == '<script><b>motorcycle</b></script> <b>chopper</b>'
    )
    assert (
        replace('<style><b>motorcycle</b></style> <b>motorcycle</b>', repls)
        == '<style><b>motorcycle</b></style> <b>chopper</b>'
    )
    assert (
        replace('<tt><b>motorcycle</b></tt> <b>motorcycle</b>', repls)
        == '<tt><b>motorcycle</b></tt> <b>chopper</b>'
    )
