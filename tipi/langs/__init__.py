# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import warnings

from tipi.repl import Replacement


__all__ = ('langs',)


class MissingLanguageError(LookupError):
    pass


class LangsLoader(object):
    """Dynamically loads replacements for given languages."""

    def __init__(self):
        self._langs = {}

    def _load(self, lang):
        try:
            lang = __import__('tipi.langs.' + lang, fromlist=[''])
        except ImportError:
            raise MissingLanguageError
        try:
            return [Replacement(*args) for args in lang.replacements]
        except AttributeError:
            raise MissingLanguageError

    def __getitem__(self, lang):
        """Returns list of replacements for given language."""
        if lang not in self._langs:
            try:
                self._langs[lang] = self._load(lang)
            except MissingLanguageError:
                warnings.warn(
                    "No such language available: '{0}'".format(lang),
                    ImportWarning
                )
        return self._langs.get(lang, [])


#! Repository of replacements for available languages.
#! For missing languages silently returns empty lists.
langs = LangsLoader()
