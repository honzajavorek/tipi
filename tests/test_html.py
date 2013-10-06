# -*- coding: utf-8 -*-


import pytest

from tipi.html import HTMLFragment


def strip_whitespace(s):
    return ' '.join(s.split())


class TestHTMLFragment(object):

    def test_pass_unwrapped_fragment_get_unwrapped_fragment(self):
        s = 'Whose motorcycle is <strong>this</strong>?'
        assert unicode(HTMLFragment(s)) == s

    def test_pass_wrapped_fragment_get_wrapped_fragment(self):
        s = '<p>Whose motorcycle is <strong>this</strong>?</p>'
        assert unicode(HTMLFragment(s)) == s

    def test_pass_document_get_document(self):
        s = '''
        <!DOCTYPE html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <title>Fabienne</title>
            <link rel="stylesheet" href="style.css">
            <script src="script.js"></script>
            <style>p { color: red; }</style>
          </head>
          <body class="zed dead">
            <!-- page content -->
            It's a chopper, baby.
          </body>
        </html>
        '''
        s1 = strip_whitespace(unicode(HTMLFragment(s)))
        s2 = strip_whitespace(s)
        assert s1 == s2

    def test_unicode(self):
        s = u'<em>Řeřicha</em> stands for cress in <strong>Czech</strong>.'
        assert unicode(HTMLFragment(s)) == s

    def test_html_entities_conversions(self):
        s1 = unicode(HTMLFragment('<b>Honey&nbsp;Bunny</b> &copy;'))
        s2 = u'<b>Honey\xa0Bunny</b> \xa9'
        assert s1 == s2

    def test_get_text_by_index(self):
        s = HTMLFragment('''
        The Wolf:
        <p>
            That's <strong>thirty</strong> minutes away.
            <!-- The Wolf -->
            I'll be there in <strong>ten</strong>.
        </p>
        ''')
        assert s[0] == 'T'
        assert s[31] == 'T'
        assert s[36] == 's'
        assert s[53] == ' '
        assert s[58] == 't'
        assert s[93] == 'I'
        assert s[110] == 't'

    def test_set_text_by_index(self):
        s = HTMLFragment(
            '<strong>Vincent:</strong> Royale with cheese. '
            '<!-- Quarter Pounder -->'
        )
        s[21] = 'C'
        assert s[21] == 'C'
        assert unicode(s) == (
            '<strong>Vincent:</strong> Royale with Cheese. '
            '<!-- Quarter Pounder -->'
        )

    def test_del_text_by_index(self):
        s = HTMLFragment(
            '<strong>Vincent:</strong> Royale with cheese. '
            '<!-- Quarter Pounder -->'
        )
        del s[3]
        assert s[3] == 'e'
        assert unicode(s) == (
            '<strong>Vinent:</strong> Royale with cheese. '
            '<!-- Quarter Pounder -->'
        )

    def test_insert_text_by_index(self):
        s = HTMLFragment(
            '<strong>Vincent:</strong> Royale with cheese. '
            '<!-- Quarter Pounder -->'
        )
        s.insert(7, 's')
        assert s[7] == 's'
        assert unicode(s) == (
            '<strong>Vincents:</strong> Royale with cheese. '
            '<!-- Quarter Pounder -->'
        )

    def test_set_multi_chars(self):
        s = HTMLFragment(
            '<strong>Vincent:</strong> Royale with cheese. '
            '<!-- Quarter Pounder -->'
        )
        with pytest.raises(ValueError):
            s[0] = 'Jules'

    def test_insert_multi_chars(self):
        s = HTMLFragment(
            '<strong>Vincent:</strong> Royale with cheese. '
            '<!-- Quarter Pounder -->'
        )
        with pytest.raises(ValueError):
            s.insert(0, 'Jules')

    def test_set_no_chars(self):
        s = HTMLFragment(
            '<strong>Vincent:</strong> Royale with cheese. '
            '<!-- Quarter Pounder -->'
        )
        s[0] = ''
        assert s[0] == 'i'
        assert unicode(s) == (
            '<strong>incent:</strong> Royale with cheese. '
            '<!-- Quarter Pounder -->'
        )

    def test_insert_no_chars(self):
        s = HTMLFragment(
            '<strong>Vincent:</strong> Royale with cheese. '
            '<!-- Quarter Pounder -->'
        )
        s.insert(0, '')
        assert s[0] == 'V'
        assert unicode(s) == (
            '<strong>Vincent:</strong> Royale with cheese. '
            '<!-- Quarter Pounder -->'
        )

    def test_set_bad_type(self):
        s = HTMLFragment(
            '<strong>Vincent:</strong> Royale with cheese. '
            '<!-- Quarter Pounder -->'
        )
        with pytest.raises(TypeError):
            s[0] = 42

    def test_insert_bad_type(self):
        s = HTMLFragment(
            '<strong>Vincent:</strong> Royale with cheese. '
            '<!-- Quarter Pounder -->'
        )
        with pytest.raises(TypeError):
            s.insert(0, 42)