# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import cgi

from tipi import tipi


def test_plaintext():
    assert tipi('a &lt;- b -&gt; c') == 'a ← b → c'
    assert tipi('a <- b -> c') == 'a  c'
    assert tipi(cgi.escape('a <- b -> c')) == 'a ← b → c'
