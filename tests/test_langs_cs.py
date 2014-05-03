# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from tipi import tipi as _tipi


tipi = lambda s: _tipi(s, lang='cs')


def test_date():
    assert tipi('kdy? 23. 1. 1978?') == 'kdy? 23.\u00a01.\u00a01978?'
    assert tipi('kdy? <b>23. </b>1. 1978?') == (
        'kdy? <b>23.\u00a0</b>1.\u00a01978?'
    )

    assert tipi('kdy? 23. 1.?') == 'kdy? 23.\u00a01.?'
    assert tipi('kdy? <b>23. </b>1.?') == (
        'kdy? <b>23.\u00a0</b>1.?'
    )


def test_space_between_preposition_and_word():
    assert tipi('zůstat u HTML') == 'zůstat u\u00a0HTML'
    assert tipi('zůstat u <i>HTML</i>') == 'zůstat u\u00a0<i>HTML</i>'


def test_double_quotes():
    assert tipi('''"brutal" "quote's"''') == (
        '''„brutal“ „quote's“'''
    )


def test_single_quotes():
    assert tipi(u"""'brutal' 'quote's'""") == (
        """‚brutal‘ ‚quote's‘"""
    )
