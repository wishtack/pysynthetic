#-*- coding: utf-8 -*-
#
# Created on Dec 17, 2012
#
# @author: Younes JAAIDI
#
# $Id$
#

from contracts import contract, new_contract
from .i_naming_convention import INamingConvention
from .synthetic_decorator_factory import SyntheticDecoratorFactory
from .naming_convention_camel_case import NamingConventionCamelCase
from .naming_convention_underscore import NamingConventionUnderscore

new_contract('INamingConvention', INamingConvention)

@contract
def synthesizeMember(memberName,
               defaultValue = None,
               contract = None,
               readOnly = False,
               getterName = None,
               setterName = None,
               privateMemberName = None):
    """
    CamelCase naming convention is assumed. Naming convention can be overriden using 'naming_convention' or 'namingConvention' decorators.

    :type memberName: str
    :type readOnly: bool
    :type getterName: str|None
    :type setterName: str|None
    :type privateMemberName: str|None
"""
    return SyntheticDecoratorFactory().syntheticMemberDecorator(memberName,
                                                                defaultValue,
                                                                contract,
                                                                readOnly,
                                                                getterName,
                                                                setterName,
                                                                privateMemberName,
                                                                namingConvention = NamingConventionCamelCase())

@contract
def synthesize_member(memberName,
               defaultValue = None,
               contract = None,
               readOnly = False,
               getterName = None,
               setterName = None,
               privateMemberName = None):
    """
    Underscore naming convention is assumed. Naming convention can be overriden using 'naming_convention' or 'namingConvention' decorators.

    :type memberName: str
    :type readOnly: bool
    :type getterName: str|None
    :type setterName: str|None
    :type privateMemberName: str|None
"""
    return SyntheticDecoratorFactory().syntheticMemberDecorator(memberName,
                                                                defaultValue,
                                                                contract,
                                                                readOnly,
                                                                getterName,
                                                                setterName,
                                                                privateMemberName,
                                                                namingConvention = NamingConventionUnderscore())

def synthesizeConstructor():
    return SyntheticDecoratorFactory().syntheticConstructorDecorator()

def namingConvention(namingConvention):
    """
    :type namingConvention: INamingConvention
"""
    return SyntheticDecoratorFactory().namingConventionDecorator(namingConvention)

synthesize_constructor = synthesizeConstructor
naming_convention = namingConvention
