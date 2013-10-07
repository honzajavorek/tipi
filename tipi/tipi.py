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
            html[match.start():match.end()] = repl  # mutates html
            return repl
        text = pattern[0].sub(replace, text)

    return unicode(html)


def tipi(html, lang='en'):
    """Performs language-sensitive typographic replacements on given HTML
    string according. No replacements take place in case of unknown language.
    """
    return replace(html, patterns=langs[lang])
