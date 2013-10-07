# -*- coding: utf-8 -*-


from tipi.langs import LangsLoader


class LangsLoaderWithCounter(LangsLoader):

    _counter = 0

    def _load(self, lang):
        self._counter += 1
        return super(LangsLoaderWithCounter, self)._load(lang)


class TestLangsLoader(object):

    def test_load_existing(self):
        langs = LangsLoader()
        l = langs['cs']
        assert isinstance(l, (tuple, list))
        assert list(l) != []

    def test_load_non_existing(self):
        langs = LangsLoader()
        l = langs['Le Big-Mac']
        assert isinstance(l, (tuple, list))
        assert list(l) == []

    def test_load_existing_multiple_times(self):
        langs = LangsLoaderWithCounter()
        langs['cs']
        assert langs._counter == 1
        langs['cs']
        assert langs._counter == 1

    def test_load_non_existing_multiple_times(self):
        langs = LangsLoaderWithCounter()
        langs['Le Big-Mac']
        assert langs._counter == 1
        langs['Le Big-Mac']
        assert langs._counter == 2
