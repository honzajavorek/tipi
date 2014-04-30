# -*- coding: utf-8 -*-


import cgi

from tipi import tipi


def test_plaintext():
    assert tipi(u'a &lt;- b -&gt; c') == u'a ← b → c'
    assert tipi(u'a <- b -> c') == u'a  c'
    assert tipi(cgi.escape(u'a <- b -> c')) == u'a ← b → c'
