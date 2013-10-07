# -*- coding: utf-8 -*-


import pytest

from tipi.html import HTMLFragment


def strip_whitespace(s):
    return ' '.join(s.split())


class TestHTMLFragment(object):

    def test_pass_text_get_text(self):
        s = 'Whose motorcycle is this?'
        assert unicode(HTMLFragment(s)) == s

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
        assert unicode(s) == (
            '<strong>Vincent:</strong> Royale with Cheese. '
            '<!-- Quarter Pounder -->'
        )
        assert s[21] == 'C'

    def test_del_text_by_index(self):
        s = HTMLFragment(
            '<strong>Vincent:</strong> Royale with cheese. '
            '<!-- Quarter Pounder -->'
        )
        del s[3]
        assert unicode(s) == (
            '<strong>Vinent:</strong> Royale with cheese. '
            '<!-- Quarter Pounder -->'
        )
        assert s[3] == 'e'

    def test_insert_text_by_index(self):
        s = HTMLFragment(
            '<strong>Vincent:</strong> Royale with cheese. '
            '<!-- Quarter Pounder -->'
        )
        s.insert(7, 's')
        assert unicode(s) == (
            '<strong>Vincents:</strong> Royale with cheese. '
            '<!-- Quarter Pounder -->'
        )
        assert s[7] == 's'

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
        assert unicode(s) == (
            '<strong>incent:</strong> Royale with cheese. '
            '<!-- Quarter Pounder -->'
        )
        assert s[0] == 'i'

    def test_insert_no_chars(self):
        s = HTMLFragment(
            '<strong>Vincent:</strong> Royale with cheese. '
            '<!-- Quarter Pounder -->'
        )
        s.insert(0, '')
        assert unicode(s) == (
            '<strong>Vincent:</strong> Royale with cheese. '
            '<!-- Quarter Pounder -->'
        )
        assert s[0] == 'V'

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

    def test_set_unicode(self):
        s = HTMLFragment(
            '<strong>Vincent:</strong> Royale with cheese. '
            '<!-- Quarter Pounder -->'
        )
        s[0] = u'Ž'
        assert unicode(s) == (
            u'<strong>Žincent:</strong> Royale with cheese. '
            u'<!-- Quarter Pounder -->'
        )
        assert s[0] == u'Ž'

    def test_get_slice(self):
        s = HTMLFragment(
            '<strong>Vincent:</strong> Royale with cheese. '
            '<!-- Quarter Pounder -->'
        )
        assert s[3:10] == 'cent: R'

    def test_set_short_slice(self):
        s = HTMLFragment(
            '<strong>Vincent:</strong> Royale with cheese. '
            '<!-- Quarter Pounder -->'
        )
        s[0:7] = 'Jules'
        assert unicode(s) == (
            '<strong>Jules:</strong> Royale with cheese. '
            '<!-- Quarter Pounder -->'
        )
        assert s[4] == 's' and s[5] == ':'

    def test_set_long_slice_with_offset(self):
        s = HTMLFragment(
            '<strong>Vincent:</strong> <b>Royale with</b> cheese.'
        )
        s[16:20] = 'without'
        assert unicode(s) == (
            '<strong>Vincent:</strong> <b>Royale without</b> cheese.'
        )
        assert s[20] == 'o'

    def test_set_short_slice_between_tags(self):
        s = HTMLFragment(
            '<strong>Vincent:</strong> <b>Royale with</b> cheese.'
        )
        s[5:21] = 'Jules Jules'
        assert unicode(s) == (
            '<strong>VinceJul</strong>e<b>s Jules</b>cheese.'
        )
        assert s[5] == 'J'

    def test_set_long_slice_between_tags(self):
        s = HTMLFragment(
            '<strong>Vincent:</strong> <b>Royale with</b> cheese.'
        )
        s[5:21] = 'Jules Jules Jules Jules Jules'
        assert unicode(s) == (
            '<strong>VinceJul</strong>e<b>s Jules Jul</b>es Jules Julescheese.'
        )
        assert s[5] == 'J'

    def test_set_long_slice_between_tags_no_constraint(self):
        s = HTMLFragment(
            '<strong>Vincent:</strong> <b>Royale with</b> cheese.'
        )
        s[5:] = 'Jules Jules Jules Jules Jules'
        assert unicode(s) == (
            '<strong>VinceJul</strong>e<b>s Jules Jul</b>es Jules Jules'
        )
        assert s[5] == 'J'

    def test_insert_slice(self):
        s = HTMLFragment(
            '<strong>Vincent:</strong> <b>Royale</b> with cheese.'
        )
        s[14:14] = ' Quarter Pounder'
        assert unicode(s) == (
            '<strong>Vincent:</strong> '
            '<b>Royale Quarter Pounder</b> with cheese.'
        )
        assert s[16] == 'Q'

    def test_insert_slice_to_end(self):
        s = HTMLFragment(
            '<strong>Vincent:</strong> <b>Royale</b> with cheese.'
        )
        s[50:] = 'Quarter Pounder'
        assert unicode(s) == (
            '<strong>Vincent:</strong> '
            '<b>Royale</b> with cheese.Quarter Pounder'
        )

    def test_insert_slice_to_beginning(self):
        s = HTMLFragment(
            '<strong>Vincent:</strong> <b>Royale</b> with cheese.'
        )
        s[0:0] = 'Quarter Pounder'
        assert unicode(s) == (
            'Quarter Pounder<strong>Vincent:</strong> '
            '<b>Royale</b> with cheese.'
        )

    def test_insert_slice_to_empty_string(self):
        s = HTMLFragment('')
        s[0:0] = 'Quarter Pounder'
        assert unicode(s) == 'Quarter Pounder'

    def test_set_long_slice(self):
        s = HTMLFragment(
            '<strong>Vincent:</strong> Royale with cheese. '
            '<!-- Quarter Pounder -->'
        )
        s[0:7] = 'Vincent to Jules'
        assert unicode(s) == (
            '<strong>Vincent to Jules:</strong> Royale with cheese. '
            '<!-- Quarter Pounder -->'
        )
        assert s[11] == 'J' and s[16] == ':'

    def test_del_slice(self):
        s = HTMLFragment(
            '<strong>Vincent:</strong> Royale with cheese. '
            '<!-- Quarter Pounder -->'
        )
        del s[0:10]
        assert unicode(s) == (
            '<strong></strong>oyale with cheese. '
            '<!-- Quarter Pounder -->'
        )
        assert s[1] == 'y'

    def test_step(self):
        s = HTMLFragment(
            '<strong>Vincent:</strong> Royale with cheese. '
            '<!-- Quarter Pounder -->'
        )
        with pytest.raises(IndexError):
            s[0:5:2]
        with pytest.raises(IndexError):
            s[0:5:2] = 'Jules'
        with pytest.raises(IndexError):
            del s[0:5:2]

    def test_negative_index(self):
        s = HTMLFragment(
            '<strong>Vincent:</strong> Royale with cheese. '
            '<!-- Quarter Pounder -->'
        )
        with pytest.raises(IndexError):
            s[-5]
        with pytest.raises(IndexError):
            s[0:-5]
        with pytest.raises(IndexError):
            s[-5] = 'a'
        with pytest.raises(IndexError):
            s[0:-5] = 'Jules'
        with pytest.raises(IndexError):
            del s[-5]
        with pytest.raises(IndexError):
            del s[0:-5]

    def test_parent_element_on_item(self):
        s = HTMLFragment('Whose motorcycle is <strong>this</strong>?')
        assert s[0].element is None
        assert s[21].element.tag == 'strong'

    def test_parent_element_on_slice(self):
        s = HTMLFragment('Whose <div>motorcycle is <b>this</b>?</div>')
        assert s[0:3].element is None
        assert s[7:10].element.tag == 'div'
        assert s[21:22].element.tag == 'b'
        assert s[7:21].element.tag == 'div'
        assert s[0:50].element is None

    def test_get_slice_from_empty_string(self):
        s = HTMLFragment('')
        assert s[0:5] == ''

    def test_set_slice_to_empty_string(self):
        s = HTMLFragment('')
        s[0:5] = 'Fabienne'
        assert unicode(s) == 'Fabienne'

    def test_del_slice_to_empty_string(self):
        s = HTMLFragment('')
        del s[0:5]
        assert unicode(s) == ''
