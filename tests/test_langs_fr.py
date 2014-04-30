# -*- coding: utf-8 -*-


from tipi import tipi as _tipi


tipi = lambda s: _tipi(s, lang='fr')


def test_double_quotes():
    assert tipi(u'''"brutal" "quote's"''') == (
        u'''«brutal» «quote's»'''
    )


def test_single_quotes():
    assert tipi(u"""'brutal' 'quote's'""") == (
        u"""‹brutal› ‹quote's›"""
    )
