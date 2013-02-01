#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import sys

if sys.version_info < (2, 7):
    raise Exception('Pysynthetic requires Python 2.7 or higher.')

# Dependencies
install_requires = ['pycontracts >= 1.4.0',
                    'pyparsing == 1.5.6']

setup(
    name="pysynthetic",
    version="0.1",
    platforms=['any'],
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=install_requires,
    zip_safe=True)

