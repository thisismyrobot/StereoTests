#!/usr/bin/env python2.7

import doctest


files = ("stereotools.txt",)
opts = doctest.REPORT_ONLY_FIRST_FAILURE|doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE

for f in files:
    doctest.testfile(f, optionflags=opts)
