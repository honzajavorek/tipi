# -*- coding: utf-8 -*-


from tipi.html import HTMLFragment


__all__ = ('Replacement', 'replace')


class Replacement(object):
    """Replacement representation."""

    def __init__(self, pattern, replacement, filters=None):
        self.pattern = pattern
        self.replacement = replacement
        self.filters = self._parse_filters(filters)

    def _parse_filters(self, filters):
        """Parses filter definitions. Returns list of functions,
        each of them
        """
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

    def replace(self, html):
        """Perform replacements on given HTML fragment."""
        self.html = html
        text = html.text()
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


def replace(html, replacements=None):
    """Performs replacements on given HTML string with given replacements.
    No replacements take place in case no replacements are given.
    """
    if not replacements:
        return html  # no replacements
    html = HTMLFragment(html)

    for r in replacements:
        r.replace(html)

    return unicode(html)
