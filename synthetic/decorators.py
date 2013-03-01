#-*- coding: utf-8 -*-
#
# Created on Dec 17, 2012
#
# @author: Younes JAAIDI
#
# $Id$
#

from .accessor_factory import AccessorFactory
from .i_naming_convention import INamingConvention
from .property_factory import PropertyFactory
from .naming_convention_camel_case import NamingConventionCamelCase
from .naming_convention_underscore import NamingConventionUnderscore
from .synthetic_decorator_factory import SyntheticDecoratorFactory
from contracts import contract, new_contract

new_contract('INamingConvention', INamingConvention)

@contract
def synthesizeMember(memberName,
                     default = None,
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
    memberFactory = AccessorFactory(namingConvention = NamingConventionCamelCase(),
                                    getterName = getterName,
                                    setterName = setterName)
    return SyntheticDecoratorFactory().syntheticMemberDecorator(memberName = memberName,
                                                                defaultValue = default,
                                                                contract = contract,
                                                                readOnly = readOnly,
                                                                privateMemberName = privateMemberName,
                                                                memberFactory = memberFactory)

@contract
def synthesize_member(member_name,
                      default = None,
                      contract = None,
                      read_only = False,
                      getter_name = None,
                      setter_name = None,
                      private_member_name = None):
    """
    Underscore naming convention is assumed. Naming convention can be overriden using 'naming_convention' or 'namingConvention' decorators.

    :type member_name: str
    :type read_only: bool
    :type getter_name: str|None
    :type setter_name: str|None
    :type private_member_name: str|None
"""
    memberFactory = AccessorFactory(namingConvention = NamingConventionUnderscore(),
                                    getterName = getter_name,
                                    setterName = setter_name)
    return SyntheticDecoratorFactory().syntheticMemberDecorator(memberName = member_name,
                                                                defaultValue = default,
                                                                contract = contract,
                                                                readOnly = read_only,
                                                                privateMemberName = private_member_name,
                                                                memberFactory = memberFactory)

@contract
def synthesizeProperty(propertyName,
                       default = None,
                       contract = None,
                       readOnly = False,
                       privateMemberName = None):
    """
    :type propertyName: str
    :type readOnly: bool
    :type privateMemberName: str|None
"""
    return SyntheticDecoratorFactory().syntheticMemberDecorator(memberName = propertyName,
                                                                defaultValue = default,
                                                                contract = contract,
                                                                readOnly = readOnly,
                                                                privateMemberName = privateMemberName,
                                                                memberFactory = PropertyFactory())
@contract
def synthesize_property(property_name,
                       default = None,
                       contract = None,
                       read_only = False,
                       private_member_name = None):
    """
    :type property_name: str
    :type read_only: bool
    :type private_member_name: str|None
"""
    return SyntheticDecoratorFactory().syntheticMemberDecorator(memberName = property_name,
                                                                defaultValue = default,
                                                                contract = contract,
                                                                readOnly = read_only,
                                                                privateMemberName = private_member_name,
                                                                memberFactory = PropertyFactory())

def synthesizeConstructor():
    return SyntheticDecoratorFactory().syntheticConstructorDecorator()


def namingConvention(namingConvention):
    """
    :type namingConvention: INamingConvention
"""
    return SyntheticDecoratorFactory().namingConventionDecorator(namingConvention)

def naming_convention(naming_convention):
    """
    :type naming_convention: INamingConvention
"""
    return SyntheticDecoratorFactory().namingConventionDecorator(naming_convention)  

synthesize_constructor = synthesizeConstructor
