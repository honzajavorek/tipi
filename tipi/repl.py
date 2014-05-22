# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from tipi.compat import unicode
from tipi.html import HTMLFragment


__all__ = ('Replacement', 'replace')


class Replacement(object):
    """Replacement representation."""

    skipped_tags = (
        'code', 'kbd', 'pre', 'samp', 'script', 'style', 'tt', 'xmp'
    )
    textflow_tags = (
        'b', 'big', 'i', 'small', 'tt', 'abbr', 'acronym', 'cite',
        'dfn', 'em', 'kbd', 'strong', 'samp', 'var', 'a', 'bdo', 'q', 'script',
        'span', 'sub', 'sup'
    )

    def __init__(self, pattern, replacement):
        self.pattern = pattern
        self.replacement = replacement

    def _is_replacement_allowed(self, s):
        """Tests whether replacement is allowed on given piece of HTML text."""
        if any(tag in s.parent_tags for tag in self.skipped_tags):
            return False
        if any(tag not in self.textflow_tags for tag in s.involved_tags):
            return False
        return True

    def replace(self, html):
        """Perform replacements on given HTML fragment."""
        self.html = html
        text = html.text()
        positions = []

        def perform_replacement(match):
            offset = sum(positions)
            start, stop = match.start() + offset, match.end() + offset

            s = self.html[start:stop]
            if self._is_replacement_allowed(s):
                repl = match.expand(self.replacement)
                self.html[start:stop] = repl
            else:
                repl = match.group()  # no replacement takes place

            positions.append(match.end())
            return repl

        while True:
            if positions:
                text = text[positions[-1]:]

            text, n = self.pattern.subn(perform_replacement, text, count=1)
            if not n:  # all is already replaced
                break


def replace(html, replacements=None):
    """Performs replacements on given HTML string."""
    if not replacements:
        return html  # no replacements
    html = HTMLFragment(html)

    for r in replacements:
        r.replace(html)

    return unicode(html)
