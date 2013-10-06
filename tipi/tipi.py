# -*- coding: utf-8 -*-


from tipi.html import HTMLFragment


def tipi(html, lang='en'):
    try:
        lang = __import__('tipi.lang.' + lang, fromlist=[''])
        patterns = lang.patterns
    except (ImportError, AttributeError):
        return html  # returned unchanged silently, language is not supported

    html = HTMLFragment(html)
    text = html.text()

    for pattern in patterns:
        def replace(match):
            repl = match.expand(pattern[1])
            html[match.start():match.end()] = repl  # mutate html, side effect
            return repl
        text = pattern[0].sub(replace, text)

    return unicode(html)
