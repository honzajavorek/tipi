# -*- coding: utf-8 -*-


import re
from string import whitespace
from collections import namedtuple, MutableSequence

import lxml.html


__all__ = ('HTMLFragment',)


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
        self.addresses = self._analyze_tree(self.tree)

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

    def _analyze_tree(self, tree):  # NOQA
        """Analyze given tree and create mapping of indexes to character
        addresses.
        """
        addresses = []
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
                    addresses.append(CharAddress(char, el, attr, i))

        # remove leading and trailing whitespace
        while addresses and addresses[0].char == ' ':
            del addresses[0]
        while addresses and addresses[-1].char == ' ':
            del addresses[-1]

        return addresses

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
        return iter(addr.char for addr in self.addresses)

    def _validate_index(self, index):
        """Validates given index, eventually raises errors."""
        if isinstance(index, slice):
            if index.step and index.step != 1:
                raise IndexError('Step is not allowed.')
            indexes = (index.start, index.stop)
        else:
            indexes = (index,)
        for index in indexes:
            if index < 0:
                raise IndexError('Negative indexes are not allowed.')

    def __getitem__(self, index):
        """Provide character by it's index. Works also with slices,
        but step is not implemented.
        """
        self._validate_index(index)
        if isinstance(index, slice):
            return ''.join(
                addr.char for addr in
                self.addresses[index.start:index.stop]
            )
        return self.addresses[index].char

    def __setitem__(self, index, value):
        """Set character to given value by it's index. Works also with
        slices, but step is not implemented.
        """
        self._validate_index(index)
        if not isinstance(value, basestring):
            raise TypeError('Only characters can be set.')

        if isinstance(index, slice):
            # mutate the tree, first prepare changes
            addrs = self.addresses[index.start:index.stop]
            changes = {}

            target_size = len(addrs)
            change_size = max(len(value), target_size)

            for i in xrange(change_size):
                addr = addrs[i if i < target_size else -1]
                change_key = (addr.element, addr.attr)

                chars, deleted = changes.get(
                    change_key,  # if already changed, take from mapping
                    (list(getattr(addr.element, addr.attr)), 0)  # from tree
                )

                c = value[i:i + 1]  # new character replacing the old one
                if target_size < change_size and addr.index < i:
                    # in case there is less target space than is required
                    # to store the new value, start inserting characters
                    chars.insert(i, c)
                else:
                    # overwrite characters, adjust indexing with the number
                    # of already deleted positions
                    chars[addr.index - deleted:addr.index - deleted + 1] = c

                if not c:
                    # count deleted positions in this particular character set
                    deleted += 1
                changes[change_key] = (chars, deleted)

            # record to tree, all changes at once
            for (el, attr), (chars, deleted) in changes.items():
                setattr(el, attr, ''.join(chars))
        else:
            if len(value) > 1:
                raise ValueError('Only single character can be set.')

            # mutate the tree
            addr = self.addresses[index]
            chars = list(getattr(addr.element, addr.attr))
            chars[addr.index] = value
            setattr(addr.element, addr.attr, ''.join(chars))

        # re-analyze the tree
        self.addresses = self._analyze_tree(self.tree)

    def __delitem__(self, index):
        """Set character to empty string by it's index. Works also with
        slices, but step is not implemented.
        """
        self.__setitem__(index, '')

    def __len__(self):
        return len(self.addresses)

    def insert(self, index, value):
        if not isinstance(value, basestring):
            raise TypeError('Only characters can be inserted.')
        if len(value) == 0:
            return
        if len(value) != 1:
            raise ValueError('Only single character can be inserted.')

        # mutate the tree
        addr = self.addresses[index]
        chars = list(getattr(addr.element, addr.attr))
        chars.insert(addr.index, value)
        setattr(addr.element, addr.attr, ''.join(chars))

        # re-analyze the tree
        self.addresses = self._analyze_tree(self.tree)

    def text(self):
        return ''.join(list(self))

    def __unicode__(self):
        s = lxml.html.tostring(self.tree, encoding=self.output_encoding)
        s = s.decode(self.output_encoding)

        for pattern in self._strip_root_re:  # strip the root tag
            s = pattern.sub('', s)
        if self.has_body:
            s = self._body_re.sub(s, self.string)  # use the tree as body

        return s
