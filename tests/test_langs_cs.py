# -*- coding: utf-8 -*-


from tipi import tipi


def test_ascii():
    assert tipi('ascii', 'cs') == 'ascii'


def test_unicode():
    assert tipi(u'řeřicha', 'cs') == u'řeřicha'

    s = (
        u'<p>"Zavolej mi na číslo <strong class="tel">765-876-888</strong>," '
        u'řekla, a zmizela...</p>'
    )
    assert tipi(s, lang='cs') == (
        u'<p>„Zavolej mi na číslo <strong class="tel">765–876–888</strong>,“ '
        u'řekla, a zmizela…</p>'
    )


def test_ellipsis():
    assert tipi(u'nevím, no...!', 'cs') == u'nevím, no…!'
    assert tipi(u'nevím, <b>no</b>...!', 'cs') == u'nevím, <b>no</b>…!'


def test_en_dash_numbers():
    assert tipi(u'123-123-123', 'cs') == u'123–123–123'
    assert tipi(u'123-<b>123</b>-123', 'cs') == u'123–<b>123</b>–123'
