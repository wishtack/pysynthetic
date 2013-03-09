#!/bin/sh

cat docs/description.rst \
    docs/resources.rst \
    docs/examples.rst | sed 's/:meth:`\([^` ]*\)[^`]*`/``\1``/g'

