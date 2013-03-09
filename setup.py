#!/usr/bin/env python
from setuptools import setup

# @hack: PyContracts dependency PyParsing needs version 2.0.0 to work with Python 3 but this version doesn't work with Python 2.
import sys
pyparsing_version_condition = '<'
if sys.version_info[0] >= 3:
    pyparsing_version_condition = '>='

setup(setup_requires=['pyparsing%s2.0.0' % pyparsing_version_condition,
                      'd2to1'],
      d2to1=True)
