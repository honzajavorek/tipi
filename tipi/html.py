# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import re
from string import whitespace
from collections import namedtuple, MutableSequence

import lxml.html

from tipi.compat import unicode, basestring, range, ToStringMixin


__all__ = ('HTMLFragment',)


class cached_property(object):

    def __init__(self, factory, attr_name=None):
        self._attr_name = attr_name or factory.__name__
        self._factory = factory

    def __get__(self, instance, owner):
        attr = self._factory(instance)
        setattr(instance, self._attr_name, attr)
        return attr


class HTMLString(unicode):
    """String with information about parent HTML elements."""

    def __new__(cls, addresses):
        chars = ''.join(addr.char for addr in addresses)
        s = super(HTMLString, cls).__new__(cls, chars)
        s._addresses = addresses
        return s

    @cached_property
    def parent_tags(self):
        """Provides tags of all parent HTML elements."""
        tags = set()

        for addr in self._addresses:
            if addr.attr == 'text':
                tags.add(addr.element.tag)
            tags.update(el.tag for el in addr.element.iterancestors())

        tags.discard(HTMLFragment._root_tag)
        return frozenset(tags)

    @cached_property
    def involved_tags(self):
        """Provides all HTML tags directly involved in this string."""
        if len(self._addresses) < 2:
            # there can't be a tag boundary if there's only 1 or 0 characters
            return frozenset()

        # creating 'parent_sets' mapping, where the first item in tuple
        # is the address of character and the second is set
        # of character's parent HTML elements
        parent_sets = []

        # meanwhile we are creatingalso a set of common parents so we can
        # put them away later on (we're not interested in them as
        # they're only some global wrappers)
        common_parents = set()

        for addr in self._addresses:
            parents = set()
            if addr.attr == 'text':
                parents.add(addr.element)
            parents.update(addr.element.iterancestors())

            parent_sets.append((addr, parents))
            if not common_parents:
                common_parents = parents
            else:
                common_parents &= parents

        # constructing final set of involved tags
        involved_tags = set()
        prev_addr = None

        for addr, parents in parent_sets:
            parents = parents - common_parents
            involved_tags.update(p.tag for p in parents)

            # hidden tags - sometimes there are tags without text which
            # can hide between characters, but they actually break textflow
            is_tail_of_hidden = (
                prev_addr and
                addr.attr == 'tail' and
                prev_addr.element != addr.element
            )
            if is_tail_of_hidden:
                involved_tags.add(addr.element)

            prev_addr = addr

        return frozenset(involved_tags)


Text = namedtuple('TextAddress', 'content element attr')


CharAddress = namedtuple('CharAddress', 'char element attr index')


class HTMLFragment(MutableSequence, ToStringMixin):
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

    skipped_tags = ['style', 'script']

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

    def _iter_texts(self, tree):
        """Iterates over texts in given HTML tree."""
        skip = (
            not isinstance(tree, lxml.html.HtmlElement)  # comments, etc.
            or tree.tag in self.skipped_tags
        )
        if not skip:
            if tree.text:
                yield Text(tree.text, tree, 'text')
            for child in tree:
                for text in self._iter_texts(child):
                    yield text
        if tree.tail:
            yield Text(tree.tail, tree, 'tail')

    def _analyze_tree(self, tree):
        """Analyze given tree and create mapping of indexes to character
        addresses.
        """
        addresses = []
        for text in self._iter_texts(tree):
            for i, char in enumerate(text.content):
                if char in whitespace:
                    char = ' '
                addresses.append(CharAddress(char, text.element, text.attr, i))

        # remove leading and trailing whitespace
        while addresses and addresses[0].char == ' ':
            del addresses[0]
        while addresses and addresses[-1].char == ' ':
            del addresses[-1]

        return addresses

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
            if index is not None and index < 0:
                raise IndexError('Negative indexes are not allowed.')

    def __getitem__(self, index):
        """Provide character by it's index. Works also with slices,
        but step is not implemented.
        """
        self._validate_index(index)
        if isinstance(index, slice):
            return HTMLString(self.addresses[index.start:index.stop])
        return HTMLString([self.addresses[index]])

    def _find_pivot_addr(self, index):
        """Inserting by slicing can lead into situation where no addresses are
        selected. In that case a pivot address has to be chosen so we know
        where to add characters.
        """
        if not self.addresses or index.start == 0:
            return CharAddress('', self.tree, 'text', -1)  # string beginning
        if index.start > len(self.addresses):
            return self.addresses[-1]
        return self.addresses[index.start]

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
            pivot_addr = self._find_pivot_addr(index) if not addrs else None

            changes = {}

            target_size = len(addrs)
            change_size = max(len(value), target_size)

            for i in range(change_size):
                is_insert = (i >= target_size)
                addr = addrs[-1 if is_insert else i] if addrs else pivot_addr
                change_key = (addr.element, addr.attr)

                chars, deleted = changes.get(
                    change_key,  # if already changed, take from mapping
                    (list(getattr(addr.element, addr.attr) or ''), 0)  # tree
                )

                c = value[i:i + 1]  # new character replacing the old one
                if is_insert:
                    # in case there is less target space than is required
                    # to store the new value, start inserting characters
                    chars.insert(i - target_size + addr.index + 1, c)
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

    def to_string(self):
        s = lxml.html.tostring(self.tree, encoding=self.output_encoding)
        s = s.decode(self.output_encoding)

        for pattern in self._strip_root_re:  # strip the root tag
            s = pattern.sub('', s)
        if self.has_body:
            s = self._body_re.sub(s, self.string)  # use the tree as body

        return s
