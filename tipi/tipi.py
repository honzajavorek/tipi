# -*- coding: utf-8 -*-


from .langs import langs
from .html import HTMLFragment


__all__ = ('tipi',)


def replace(html, patterns=None):
    """Performs replacements on given HTML string with given patterns.
    No replacements take place in case no patterns are given.
    """
    if not patterns:
        return html

    html = HTMLFragment(html)
    text = html.text()

    for pattern in patterns:
        def replace(match):
            repl = match.expand(pattern[1])
            print match.group(0), pattern[1]
            print repr(html[match.start():match.end()]), repr(repl)
            html[match.start():match.end()] = repl  # mutates html
            return repl

        while True:
            text, n = pattern[0].subn(replace, text, count=1)
            if not n:
                break

    return unicode(html)


def tipi(html, lang='en'):
    """Performs language-sensitive typographic replacements on given HTML
    string according. No replacements take place in case of unknown language.
    """
    return replace(html, patterns=langs[lang])
