
Tipi
====

Tipi will be a tool for converting plain ASCII punctuation characters into HTML entities according to basic typography rules.

Status: ACTIVE
--------------

Under active development and maintenance.

Ideas behind this project
-------------------------

- Input is HTML code, output is the same HTML code with changes in typography (entities, spaces, quotes, etc.).
- `You can't parse HTML with regex. <http://stackoverflow.com/a/1732454/325365>`_
- The best existing HTML parser and *tokenizer* for Python is `lxml <http://lxml.de/>`_.
- There are more languages than English in the world. Each of them has different typographic rules.

Alternatives
------------

- `Typogrify <https://github.com/mintchaos/typogrify>`_ - English only, adds markup for styling, on top of `smartypants <http://web.chad.org/projects/smartypants.py/>_`
- `cstypo <https://github.com/yetty/cstypo>`_ - Czech only, not working well with HTML

Plans
-----

- Inspiration from `Typogrify <http://static.mintchaos.com/projects/typogrify/>`_?
- Coupling with `Markdown <https://bitbucket.org/jeunice/mdx_smartypants/src/251fb53a1885/mdx_smartypants.py>`_. Coupling with Django, Jinja2.
- Get some inspiration from `Texy! <https://github.com/dg/texy/blob/master/Texy/modules/TexyTypographyModule.php>`_
- Get some inspiration from `Dero's <http://typografie.dero.name/typografie-entity.php>`_ and `Typomil's <http://typomil.com/typografie-na-webu/znakove-entity.htm>`_ typography guides.
- Get some inspiration from `Liteera.cz <http://www.liteera.cz/>`_) (`source <https://is.muni.cz/auth/th/172528/fi_b?info=1;zpet=%2Fauth%2Fvyhledavani%2F%3Fsearch%3Djakub%20fiala%26start%3D1>`_).
- Maybe also some inspiration `from here <http://www.webtvorba.cz/web/typografie-na-webu.html>`_.
- `Texy! rules extracted to RegExps <https://gist.github.com/msgre/3805872>`_.
- `Texy! tests <https://github.com/dg/texy/tree/release-2.x/tests/Texy>`_.

License: MIT
------------

© 2013 Jan Javorek <mail@honzajavorek.cz>

This work is licensed under `MIT license <https://en.wikipedia.org/wiki/MIT_License>`_.
