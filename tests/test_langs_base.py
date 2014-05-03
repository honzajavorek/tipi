# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from tipi import tipi as _tipi


tipi = lambda s: _tipi(s, lang='en')


def test_ascii_plain():
    assert tipi('ascii') == 'ascii'


def test_unicode_html():
    assert tipi('řeřicha') == 'řeřicha'

    s = (
        '<p>Její číslo je <strong class="tel">765-876-888</strong>...</p>'
    )
    assert tipi(s) == (
        '<p>Její číslo je <strong class="tel">765–876–888</strong>…</p>'
    )


def test_ellipsis():
    assert tipi('nevím, no...!') == 'nevím, no…!'
    assert tipi('nevím, <b>no</b>...!') == 'nevím, <b>no</b>…!'


def test_en_dash_numbers():
    assert tipi('123-123-123') == '123–123–123'
    assert tipi('123-<b>123</b>-123') == '123–<b>123</b>–123'


def test_en_dash_alphanum_alphanum():
    assert tipi('Brno--Žabovřesky') == 'Brno–Žabovřesky'
    assert tipi('Brno--<b>Žabovřesky</b>') == 'Brno–<b>Žabovřesky</b>'


def test_en_dash_price():
    assert tipi('42,- za kus') == '42,– za kus'
    assert tipi('<b>42,</b>- za kus') == '<b>42,</b>– za kus'


def test_em_dash():
    assert tipi('blbý --- blbější!') == 'blbý\u00a0— blbější!'
    assert tipi('blbý <i>--- blbě</i>jší!') == 'blbý\u00a0<i>— blbě</i>jší!'


def test_nbsp_before_dash():
    assert tipi('blbý - blbější!') == 'blbý\u00a0– blbější!'
    assert tipi('blbý <i>- blbě</i>jší!') == 'blbý\u00a0<i>– blbě</i>jší!'


def test_left_right_arrow():
    assert tipi('a &lt;-&gt; b') == 'a ↔ b'
    assert tipi('a &lt;--&gt; <i>b</i>') == 'a ↔ <i>b</i>'


def test_right_arrow():
    assert tipi('a -&gt; b') == 'a → b'
    assert tipi('a --&gt; <i>b</i>') == 'a → <i>b</i>'


def test_left_arrow():
    assert tipi('a &lt;- b') == 'a ← b'
    assert tipi('a &lt;-- <i>b</i>') == 'a ← <i>b</i>'


def test_right_double_arrow():
    assert tipi('a =&gt; b') == 'a ⇒ b'
    assert tipi('a ==&gt; <i>b</i>') == 'a ⇒ <i>b</i>'


def test_plus_minus():
    assert tipi('a +- b') == 'a ± b'
    assert tipi('a +- <i>b</i>') == 'a ± <i>b</i>'


def test_dimension_sign():
    assert tipi('a x b') == 'a x b'
    assert tipi('1 x 2') == '1 × 2'
    assert tipi('1 x <i>2</i>') == '1 × <i>2</i>'

    assert tipi('ax ') == 'ax '
    assert tipi('0x') == '0×'
    assert tipi('<i>200</i>x') == '<i>200</i>×'


def test_trademark():
    assert tipi('tipi(TM)') == 'tipi™'
    assert tipi('tipi<sup>(TM)</sup>') == 'tipi<sup>™</sup>'


def test_registered():
    assert tipi('tipi(R)') == 'tipi®'
    assert tipi('tipi<sup>(R)</sup>') == 'tipi<sup>®</sup>'


def test_copyright():
    assert tipi('(C) 1987') == '© 1987'
    assert tipi('<small>(C)</small> 1987') == '<small>©</small> 1987'


def test_euro():
    assert tipi('1000 (EUR)') == '1000 €'
    assert tipi('<b>1000</b> (EUR)') == '<b>1000</b> €'


def test_phone_number():
    assert tipi('632 212 882') == '632\u00a0212\u00a0882'
    assert tipi('<b>+420</b> 632') == '<b>+420</b>\u00a0632'


def test_space_between_number_and_word_or_symbol():
    assert tipi('exactly 10 USD in cash') == (
        'exactly 10\u00a0USD in cash'
    )
    assert tipi('exactly <b>10</b> USD in cash') == (
        'exactly <b>10</b>\u00a0USD in cash'
    )


def test_space_before_last_short_word():
    assert tipi(
        '<p>Roses are red,<br>'
        'Violets are blue,<br>'
        'Sugar is sweet,<br>'
        'And so are\u00a0you.</p>'
    ) == (
        '<p>Roses are red,<br>'
        'Violets are blue,<br>'
        'Sugar is sweet,<br>'
        'And so are\u00a0you.</p>'
    )
