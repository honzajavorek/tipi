# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

PY3 = sys.version_info >= (3, 0)

if PY3:
    unicode = str
    basestring = str
    range = range

    class ToStringMixin(object):
        def __str__(self):
            return self.to_string()

else:
    unicode = unicode
    basestring = basestring
    range = xrange

    class ToStringMixin(object):
        def __unicode__(self):
            return self.to_string()
