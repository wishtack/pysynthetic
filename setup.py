#!/usr/bin/env python
from setuptools import setup

setup(tests_require = ['mock', 'nose'],
      test_suite = 'nose.collector')
