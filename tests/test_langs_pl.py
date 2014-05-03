# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from tipi import tipi as _tipi


tipi = lambda s: _tipi(s, lang='pl')


def test_double_quotes():
    assert tipi('''"brutal" "quote's"''') == (
        '''„brutal” „quote's”'''
    )


def test_single_quotes():
    assert tipi("""'brutal' 'quote's'""") == (
        """‚brutal’ ‚quote's’"""
    )
