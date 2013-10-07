# -*- coding: utf-8 -*-


from .langs import langs
from .html import HTMLFragment


__all__ = ('tipi',)


class PatternReplacer(object):

    def __init__(self, html, pattern, replacement, filters=None):
        self.html = html
        self.pattern = pattern
        self.replacement = replacement
        self.filters = self._parse_filters(filters)

    def _parse_filters(self, filters):
        if not filters:
            return []

        funcs = []
        for f in filters:
            if isinstance(f, basestring):
                # filter by tag name
                if f.startswith('-'):
                    # replace only if not within this tag
                    funcs.append(
                        lambda s: f[1:] not in s.parent_tags
                    )
                else:
                    # replace only within this tag
                    funcs.append(
                        lambda s: f in s.parent_tags
                    )
            else:
                funcs.append(f)  # filter by custom function
        return funcs

    def replace(self):
        text = self.html.text()
        positions = []

        def perform_replacement(match):
            offset = sum(positions)
            start, stop = match.start() + offset, match.end() + offset

            s = self.html[start:stop]
            if all(f(s) for f in self.filters):  # allowed?
                repl = match.expand(self.replacement)
                self.html[start:stop] = repl
            else:
                repl = match.group()  # no replacement takes place

            positions.append(match.end())
            return repl

        while True:
            if positions:
                text = text[positions[-1]:]
            print repr(text)
            text, n = self.pattern.subn(perform_replacement, text, count=1)
            if not n:  # all is already replaced
                break


class Replacer(object):
    """Performs replacements on given HTML string with given patterns.
    No replacements take place in case no patterns are given.
    """

    html_fragment_cls = HTMLFragment

    def replace(self, html, patterns=None):
        if not patterns:
            return html  # no replacements

        html = self.html_fragment_cls(html)
        self.html = html

        for p in patterns:
            PatternReplacer(html, *p).replace()

        return unicode(self.html)


def tipi(html, lang='en'):
    """Performs language-sensitive typographic replacements on given HTML
    string. No replacements take place in case of unknown language.
    """
    return Replacer().replace(html, patterns=langs[lang])
