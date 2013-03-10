#!/bin/sh

cat docs/description.rst \
    docs/resources.rst \
    docs/installation.rst \
    docs/examples.rst | sed 's/:meth:`\([^` ]*\)[^`]*`/``\1``/g'

