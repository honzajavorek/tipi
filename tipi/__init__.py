# -*- coding: utf-8 -*- #


__title__ = 'tipi'
__version__ = '0.0.1'
__author__ = 'Honza Javorek'
__license__ = 'MIT'
__copyright__ = 'Copyright 2013 Honza Javorek'


from tipi.langs import langs
from tipi.repl import replace


__all__ = ('tipi',)


def tipi(html, lang='en'):
    """Performs language-sensitive typographic replacements on given HTML
    string. No replacements take place in case of unknown language.
    """
    return replace(html, replacements=langs[lang])
