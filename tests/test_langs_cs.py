# -*- coding: utf-8 -*-


from tipi import tipi as _tipi


tipi = lambda s: _tipi(s, lang='cs')


def test_date():
    assert tipi(u'kdy? 23. 1. 1978?') == u'kdy? 23.\u00a01.\u00a01978?'
    assert tipi(u'kdy? <b>23. </b>1. 1978?') == (
        u'kdy? <b>23.\u00a0</b>1.\u00a01978?'
    )

    assert tipi(u'kdy? 23. 1.?') == u'kdy? 23.\u00a01.?'
    assert tipi(u'kdy? <b>23. </b>1.?') == (
        u'kdy? <b>23.\u00a0</b>1.?'
    )


def test_space_between_preposition_and_word():
    assert tipi(u'zůstat u HTML') == u'zůstat u\u00a0HTML'
    assert tipi(u'zůstat u <i>HTML</i>') == u'zůstat u\u00a0<i>HTML</i>'


def test_double_quotes():
    assert tipi(u'''"brutal" "quote's"''') == (
        u'''„brutal“ „quote's“'''
    )


def test_single_quotes():
    assert tipi(u"""'brutal' 'quote's'""") == (
        u"""‚brutal‘ ‚quote's‘"""
    )
