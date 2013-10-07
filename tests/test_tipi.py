# -*- coding: utf-8 -*-


import re

from tipi.tipi import replace


class TestReplace(object):

    def test_simple_replace(self):
        s = 'Whose <strong class="vehicle">motorcycle</strong> is this?'
        patterns = (
            (re.compile(r'(motorcycle) (is)'), ur'\1\u00a0\2'),
        )
        assert (
            replace(s, patterns)
            ==
            u'Whose <strong class="vehicle">motorcycle</strong>\u00a0is this?'
        )

    def test_multiple_replace(self):
        s = 'Whose <strong class="vehicle">motorcycle</strong> is this?'
        patterns = (
            (re.compile(r'motorcycle'), ur'motor-cycle'),
            (re.compile(r' '), ur'\u00a0'),
        )
        assert (
            replace(s, patterns)
            ==
            (u'Whose\u00a0<strong class="vehicle">motor-cycle'
             u'</strong>\u00a0is\u00a0this?')
        )
