
Tipi
====

Tipi is for typographic replacements in HTML.

Status: ACTIVE
--------------

Under active development and maintenance.

.. image:: https://travis-ci.org/honzajavorek/tipi.png?branch=master
   :target: https://travis-ci.org/honzajavorek/tipi
.. image:: https://coveralls.io/repos/honzajavorek/tipi/badge.png?branch=master
    :target: https://coveralls.io/r/honzajavorek/tipi?branch=master
.. image:: https://pypip.in/v/tipi/badge.png
    :target: http://pypi.python.org/pypi/tipi/
.. image:: https://pypip.in/d/tipi/badge.png
    :target: http://pypi.python.org/pypi/tipi/

Ideas behind this project
-------------------------

- Input is HTML code, output is the same HTML code with changes in typography (entities, spaces, quotes, etc.).
- `You can't parse HTML with regex. <http://stackoverflow.com/a/1732454/325365>`_
- The best existing HTML parser and *tokenizer* for Python is `lxml <http://lxml.de/>`_.
- There are more languages than English in the world. Each of them has different typographic rules.

Installation
------------

Easy::

    $ pip install tipi

Quickstart
----------

Usage of tipi is very straightforward:

.. code-block:: python

    >>> from tipi import tipi
    >>> html = '<p>"Zavolej mi na číslo <strong class="tel">765-876-888</strong>," řekla, a zmizela...</p>'
    >>> html = tipi(html, lang='cs')
    >>> html
    '<p>\u201eZavolej mi na \u010d\xed\xadslo <strong class="tel">765\u2013876\u2013888</strong>,\u201c \u0159ekla, a\xa0zmizela\u2026</p>'
    >>> print html
    <p>„Zavolej mi na čí­slo <strong class="tel">765–876–888</strong>,“ řekla, a zmizela…</p>

Remember that tipi is designed to work with HTML. In case you need to perform replacements on plaintext, escape it first:

.. code-block:: python

    >>> fron tipi import tipi
    >>> tipi('b -> c')  # this works only by coincidence!
    u'b → c'
    >>> tipi('a <- b -> c')
    u'a  c'
    >>> import cgi
    >>> html = cgi.escape(u'a <- b -> c')
    >>> html
    u'a &lt;- b -&gt; c'
    >>> tipi(html)
    u'a ← b → c'

Features
--------

- Support for multiple languages.
- Language-sensitive replacements for single quotes and double quotes.
- Ellipsis, dashes, nonbreakable spaces, ...
- Arrows (--> turned into → ), dimensions (12 × 30).
- Symbols (trademark, registered, copyright, EUR, ...)

Alternatives
------------

- `Typogrify <https://github.com/mintchaos/typogrify>`_ - English only, adds markup for styling, on top of `smartypants <http://web.chad.org/projects/smartypants.py/>`_
- `cstypo <https://github.com/yetty/cstypo>`_ - Czech only, not working well with HTML

Plans
-----

- Inspiration from `Typogrify <http://static.mintchaos.com/projects/typogrify/>`_?
- Get some inspiration from `Dero's <http://typografie.dero.name/typografie-entity.php>`_ and `Typomil's <http://typomil.com/typografie-na-webu/znakove-entity.htm>`_ typography guides.
- Get some inspiration from `Liteera.cz <http://www.liteera.cz/>`_) (`source <https://is.muni.cz/auth/th/172528/fi_b?info=1;zpet=%2Fauth%2Fvyhledavani%2F%3Fsearch%3Djakub%20fiala%26start%3D1>`_).
- Maybe also some inspiration `from here <http://www.webtvorba.cz/web/typografie-na-webu.html>`_.

License: MIT
------------

© 2013-2014 Jan Javorek <mail@honzajavorek.cz>

This work is licensed under `MIT license <https://en.wikipedia.org/wiki/MIT_License>`_.
