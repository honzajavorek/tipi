# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import re

from tipi.repl import Replacement, replace


def test_simple_replace():
    s = 'Whose <strong class="vehicle">motorcycle</strong> is this?'
    replacements = (
        Replacement(re.compile(r'(motorcycle) (is)'), '\\1\u00a0\\2'),
    )
    assert (
        replace(s, replacements)
        ==
        'Whose <strong class="vehicle">motorcycle</strong>\u00a0is this?'
    )


def test_multiple_replace():
    s = 'Whose <strong class="vehicle">motorcycle</strong> is this?'
    replacements = (
        Replacement(re.compile(r'motorcycle'), 'motor-cycle'),
        Replacement(re.compile(r' '), '\u00a0'),
    )
    print(repr(replace(s, replacements)))
    assert (
        replace(s, replacements)
        ==
        ('Whose\u00a0<strong class="vehicle">motor-cycle'
         '</strong>\u00a0is\u00a0this?')
    )


def test_skipped_elements():
    repls = [Replacement(re.compile(r'motorcycle'), 'chopper')]

    assert (
        replace('<code><b>motorcycle</b></code><b>motorcycle</b>', repls)
        == '<code><b>motorcycle</b></code><b>chopper</b>'
    )
    assert (
        replace('<kbd><b>motorcycle</b></kbd><b>motorcycle</b>', repls)
        == '<kbd><b>motorcycle</b></kbd><b>chopper</b>'
    )
    assert (
        replace('<pre><b>motorcycle</b></pre><b>motorcycle</b>', repls)
        == '<pre><b>motorcycle</b></pre><b>chopper</b>'
    )
    assert (
        replace('<samp><b>motorcycle</b></samp><b>motorcycle</b>', repls)
        == '<samp><b>motorcycle</b></samp><b>chopper</b>'
    )
    assert (
        replace('<script><b>motorcycle</b></script><b>motorcycle</b>', repls)
        == '<script><b>motorcycle</b></script><b>chopper</b>'
    )
    assert (
        replace('<style><b>motorcycle</b></style><b>motorcycle</b>', repls)
        == '<style><b>motorcycle</b></style><b>chopper</b>'
    )
    assert (
        replace('<tt><b>motorcycle</b></tt><b>motorcycle</b>', repls)
        == '<tt><b>motorcycle</b></tt><b>chopper</b>'
    )


def test_textflow_elements():
    s = (
        '<h1>Pulp Fiction</h1>'
        '<h2>Whose motor</h2>'
        '<p>cycle is this?</p>'
        '<h2>Whose motor</h2>'
        '<p><b>cycle</b> is this?</p>'
        '<h2>Whose motor</h2>'
        'cycle is this?'
        '<h2>Whose motor</h2>'
        '<b>cycle</b> is this?'
        '<h2>Whose</h2>'
        'motor<img>cycle is this?'
        '<h2>Whose</h2>'
        'motor<p></p>cycle is this?'
    )
    replacements = (
        Replacement(re.compile(r'motorcycle'), 'motor-cycle'),
    )
    assert replace(s, replacements) == s
