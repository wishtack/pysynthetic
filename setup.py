#!/usr/bin/env python
from setuptools import setup

setup(setup_requires=['d2to1'],
      tests_require = ['mock', 'nose'],
      test_suite = 'nose.collector',
      d2to1=True)
