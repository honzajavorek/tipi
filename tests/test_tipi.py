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

    def test_replace_everywhere(self):
        s = 'Whose <strong>motorcycle</strong> motorcycle is this?'
        patterns = (
            (re.compile(r'motorcycle'), ur'motor-cycle'),
        )
        assert (
            replace(s, patterns)
            ==
            ('Whose <strong>motor-cycle</strong> motor-cycle is this?')
        )

    def test_replace_inside_given_tags_only(self):
        s = 'Whose <strong><b>motorcycle</b></strong> motorcycle is this?'
        patterns = (
            (re.compile(r'motorcycle'), ur'motor-cycle', ['strong']),
        )
        assert (
            replace(s, patterns)
            ==
            ('Whose <strong><b>motor-cycle</b></strong> motorcycle is this?')
        )

    def test_replace_outside_given_tags_only(self):
        s = (
            'Whose <strong><b>motorcycle</b></strong> '
            '<b>motorcycle</b> is this?'
        )
        patterns = (
            (re.compile(r'motorcycle'), ur'motor-cycle', ['-strong']),
        )
        assert (
            replace(s, patterns)
            ==
            (
                'Whose <strong><b>motorcycle</b></strong> '
                '<b>motor-cycle</b> is this?'
            )
        )
