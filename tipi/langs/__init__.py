# -*- coding: utf-8 -*- #


__all__ = ('langs',)


class MissingLanguageError(LookupError):
    pass


class LangsLoader(object):
    """Dynamically loads replacement patterns for given languages."""

    def __init__(self):
        self._langs = {}

    def _load(self, lang):
        try:
            lang = __import__('tipi.langs.' + lang, fromlist=[''])
        except ImportError:
            raise MissingLanguageError
        try:
            return lang.patterns
        except AttributeError:
            raise MissingLanguageError

    def __getitem__(self, lang):
        """Returns list of patterns for given language."""
        if lang not in self._langs:
            try:
                self._langs[lang] = self._load(lang)
            except MissingLanguageError:
                pass  # TODO python warning
        return self._langs.get(lang, [])


#! Repository of replacement patterns for available languages.
#! For missing languages silently returns empty lists.
langs = LangsLoader()
