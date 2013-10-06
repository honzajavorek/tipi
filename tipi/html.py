# -*- coding: utf-8 -*-


import re
from string import whitespace
from collections import namedtuple, MutableSequence

import lxml.html


CharAddress = namedtuple('CharAddress', [
    'char',
    'element',
    'attr',
    'index',
])


class HTMLFragment(MutableSequence):
    """HTML tree with string-like sequence interface for accessing text
    content of tags.
    """

    output_encoding = 'utf-8'

    _root_tag = '_htmlfragment'
    _strip_root_re = (
        re.compile(r'^<{0}>'.format(_root_tag)),
        re.compile(r'</{0}>$'.format(_root_tag)),
    )

    _has_body_re = re.compile(r'<body', re.I)
    _body_re = re.compile(r'<body[^>]+>.*</body>', re.I | re.S)

    not_relevant_tags = ['style', 'script']

    def __init__(self, html):
        self.string = html
        self.has_body = False
        self.tree = self._parse(html)
        self.adresses = self._analyze(self.tree)

    def _parse(self, html):
        """Parse given string as HTML and return it's etree representation."""
        if self._has_body_re.search(html):
            tree = lxml.html.document_fromstring(html).find('.//body')
            self.has_body = True
        else:
            tree = lxml.html.fragment_fromstring(html,
                                                 create_parent=self._root_tag)

        if tree.tag != self._root_tag:
            # ensure the root element exists even if not really needed,
            # so the tree has always the same structure
            root = lxml.html.HtmlElement()
            root.tag = self._root_tag
            root.append(tree)
            return root
        return tree

    def _analyze(self, tree):  # NOQA
        """Analyze given tree and create mapping of indexes to character
        adresses.
        """
        adresses = []
        for el in self.tree.iter():
            if self._is_not_relevant(el):
                texts = [(el.tail, 'tail')]
            else:
                texts = [(el.text, 'text'), (el.tail, 'tail')]

            for text, attr in texts:
                if not text:
                    continue
                for i, char in enumerate(text):
                    if char in whitespace:
                        char = ' '
                    adresses.append(CharAddress(char, el, attr, i))

        # remove leading and trailing whitespace
        while adresses and adresses[0].char == ' ':
            del adresses[0]
        while adresses and adresses[-1].char == ' ':
            del adresses[-1]

        return adresses

    def _is_not_relevant(self, el):
        """Tell about given element whether it's contents should be exposed
        in the sequence of characters.
        """
        return (
            not isinstance(el, lxml.html.HtmlElement)  # comments, etc.
            or el.tag in self.not_relevant_tags
        )

    def __iter__(self):
        """Iterate over characters, one by one."""
        return iter(addr.char for addr in self.adresses)

    def __getitem__(self, index):
        """Provide character by it's index."""
        return self.adresses[index].char

    def _mutate_tree(self, index, fn):
        addr = self.adresses[index]
        chars = list(getattr(addr.element, addr.attr))
        fn(chars, addr)
        setattr(addr.element, addr.attr, ''.join(chars))

    def __setitem__(self, index, value):
        """Set character to given value by it's index."""
        if not isinstance(value, basestring):
            raise TypeError('Only character can be set.')
        if len(value) == 0:
            return self.__delitem__(index)
        if len(value) != 1:
            raise ValueError('Only single character can be set.')

        def set_item(chars, addr):
            chars[addr.index] = value
            self.adresses[index] = CharAddress(value, *addr[1:])

        self._mutate_tree(index, set_item)

    def __delitem__(self, index):
        def del_item(chars, addr):
            del chars[addr.index]

        self._mutate_tree(index, del_item)
        self.adresses = self._analyze(self.tree)

    def __len__(self):
        return len(self.addresses)

    def insert(self, index, value):
        if not isinstance(value, basestring):
            raise TypeError('Only character can be inserted.')
        if len(value) == 0:
            return
        if len(value) != 1:
            raise ValueError('Only single character can be inserted.')

        def insert_item(chars, addr):
            chars.insert(addr.index, value)

        self._mutate_tree(index, insert_item)
        self.adresses = self._analyze(self.tree)

    def __unicode__(self):
        s = lxml.html.tostring(self.tree, encoding=self.output_encoding)
        s = s.decode(self.output_encoding)

        for pattern in self._strip_root_re:  # strip the root tag
            s = pattern.sub('', s)
        if self.has_body:
            s = self._body_re.sub(s, self.string)  # use the tree as body

        return s
