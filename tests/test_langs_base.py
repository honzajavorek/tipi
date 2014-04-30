# -*- coding: utf-8 -*-


from tipi import tipi as _tipi


tipi = lambda s: _tipi(s, lang='en')


def test_ascii_plain():
    assert tipi('ascii') == 'ascii'


def test_unicode_html():
    assert tipi(u'řeřicha') == u'řeřicha'

    s = (
        u'<p>Její číslo je <strong class="tel">765-876-888</strong>...</p>'
    )
    assert tipi(s) == (
        u'<p>Její číslo je <strong class="tel">765–876–888</strong>…</p>'
    )


def test_ellipsis():
    assert tipi(u'nevím, no...!') == u'nevím, no…!'
    assert tipi(u'nevím, <b>no</b>...!') == u'nevím, <b>no</b>…!'


def test_en_dash_numbers():
    assert tipi(u'123-123-123') == u'123–123–123'
    assert tipi(u'123-<b>123</b>-123') == u'123–<b>123</b>–123'


def test_en_dash_alphanum_alphanum():
    assert tipi(u'Brno--Žabovřesky') == u'Brno–Žabovřesky'
    assert tipi(u'Brno--<b>Žabovřesky</b>') == u'Brno–<b>Žabovřesky</b>'


def test_en_dash_price():
    assert tipi(u'42,- za kus') == u'42,– za kus'
    assert tipi(u'<b>42,</b>- za kus') == u'<b>42,</b>– za kus'


def test_em_dash():
    assert tipi(u'blbý --- blbější!') == u'blbý\u00a0— blbější!'
    assert tipi(u'blbý <i>--- blbě</i>jší!') == u'blbý\u00a0<i>— blbě</i>jší!'


def test_nbsp_before_dash():
    assert tipi(u'blbý - blbější!') == u'blbý\u00a0– blbější!'
    assert tipi(u'blbý <i>- blbě</i>jší!') == u'blbý\u00a0<i>– blbě</i>jší!'


def test_left_right_arrow():
    assert tipi(u'a &lt;-&gt; b') == u'a ↔ b'
    assert tipi(u'a &lt;--&gt; <i>b</i>') == u'a ↔ <i>b</i>'


def test_right_arrow():
    assert tipi(u'a -&gt; b') == u'a → b'
    assert tipi(u'a --&gt; <i>b</i>') == u'a → <i>b</i>'


def test_left_arrow():
    assert tipi(u'a &lt;- b') == u'a ← b'
    assert tipi(u'a &lt;-- <i>b</i>') == u'a ← <i>b</i>'


def test_right_double_arrow():
    assert tipi(u'a =&gt; b') == u'a ⇒ b'
    assert tipi(u'a ==&gt; <i>b</i>') == u'a ⇒ <i>b</i>'


def test_plus_minus():
    assert tipi(u'a +- b') == u'a ± b'
    assert tipi(u'a +- <i>b</i>') == u'a ± <i>b</i>'


def test_dimension_sign():
    assert tipi(u'a x b') == u'a x b'
    assert tipi(u'1 x 2') == u'1 × 2'
    assert tipi(u'1 x <i>2</i>') == u'1 × <i>2</i>'

    assert tipi(u'ax ') == u'ax '
    assert tipi(u'0x') == u'0×'
    assert tipi(u'<i>200</i>x') == u'<i>200</i>×'


def test_trademark():
    assert tipi(u'tipi(TM)') == u'tipi™'
    assert tipi(u'tipi<sup>(TM)</sup>') == u'tipi<sup>™</sup>'


def test_registered():
    assert tipi(u'tipi(R)') == u'tipi®'
    assert tipi(u'tipi<sup>(R)</sup>') == u'tipi<sup>®</sup>'


def test_copyright():
    assert tipi(u'(C) 1987') == u'© 1987'
    assert tipi(u'<small>(C)</small> 1987') == u'<small>©</small> 1987'


def test_euro():
    assert tipi(u'1000 (EUR)') == u'1000 €'
    assert tipi(u'<b>1000</b> (EUR)') == u'<b>1000</b> €'


def test_phone_number():
    assert tipi(u'632 212 882') == u'632\u00a0212\u00a0882'
    assert tipi(u'<b>+420</b> 632') == u'<b>+420</b>\u00a0632'


def test_space_between_number_and_word_or_symbol():
    assert tipi(u'exactly 10 USD in cash') == (
        u'exactly 10\u00a0USD in cash'
    )
    assert tipi(u'exactly <b>10</b> USD in cash') == (
        u'exactly <b>10</b>\u00a0USD in cash'
    )


def test_space_before_last_short_word():
    assert tipi(
        u'<p>Roses are red,<br>'
        u'Violets are blue,<br>'
        u'Sugar is sweet,<br>'
        u'And so are\u00a0you.</p>'
    ) == (
        u'<p>Roses are red,<br>'
        u'Violets are blue,<br>'
        u'Sugar is sweet,<br>'
        u'And so are\u00a0you.</p>'
    )
