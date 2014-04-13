
Tipi
====

.. image:: https://travis-ci.org/honzajavorek/tipi.png
   :target: https://travis-ci.org/honzajavorek/tipi

Tipi is for typographic replacements in HTML.

Status: ACTIVE
--------------

Under active development and maintenance.

Ideas behind this project
-------------------------

- Input is HTML code, output is the same HTML code with changes in typography (entities, spaces, quotes, etc.).
- `You can't parse HTML with regex. <http://stackoverflow.com/a/1732454/325365>`_
- The best existing HTML parser and *tokenizer* for Python is `lxml <http://lxml.de/>`_.
- There are more languages than English in the world. Each of them has different typographic rules.

Quickstart
----------

Usage of tipi is very straightforward::

    >>> from tipi import tipi
    >>> html = tipi('<p>"Zavolej mi na číslo <strong class="tel">765-876-888</strong>," řekla, a zmizela...</p>"', lang='cs')
    >>> html
    u'<p>\u201eZavolej mi na \u010d\xed\xadslo <strong class="tel">765\u2013876\u2013888</strong>,\u201c \u0159ekla, a\xa0zmizela\u2026</p>'
    >>> print html
    <p>„Zavolej mi na čí­slo <strong class="tel">765–876–888</strong>,“ řekla, a zmizela…</p>

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

© 2013 Jan Javorek <mail@honzajavorek.cz>

This work is licensed under `MIT license <https://en.wikipedia.org/wiki/MIT_License>`_.
