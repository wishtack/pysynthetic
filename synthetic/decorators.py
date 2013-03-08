#-*- coding: utf-8 -*-
#
# Created on Dec 17, 2012
#
# @author: Younes JAAIDI
#
# $Id$
#

from .accessor_delegate import AccessorDelegate
from .i_naming_convention import INamingConvention
from .property_delegate import PropertyDelegate
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
    When applied to a class, this decorator adds getter/setter methods to it and overrides the constructor in order to set\
    the default value of the member.
    By default, the getter will be named ``memberName``. (Ex.: ``memberName = 'member' => instance.member()``)
    
    By default, the setter will be named ``memberName`` with the first letter capitalized and 'set' prepended it to it.
    (Ex.: ``memberName = "member" => instance.setMember(...)``)

    By default, the private attribute containing the member's value will be named ``memberName`` with '_' prepended to it.

    Naming convention can be overridden with a custom one using :meth:`namingConvention <namingConvention>` decorator.

    :param memberName: Name of the member to synthesize.
    :type memberName: str
    :param default: Member's default value.
    :type default: *
    :param contract: Type constraint. See `PyContracts <http://andreacensi.github.com/contracts/>`_
    :type contract: *
    :param readOnly: If set to ``True``, the setter will not be added to the class.
    :type readOnly: bool
    :param getterName: Custom getter name. This can be useful when the member is a boolean. (Ex.: ``isAlive``)
    :type getterName: str|None
    :param setterName: Custom setter name.
    :type setterName: str|None
    :param privateMemberName: Custom name for the private attribute that contains the member's value.
    :type privateMemberName: str|None
"""
    accessorDelegate = AccessorDelegate(namingConvention = NamingConventionCamelCase(),
                                        getterName = getterName,
                                        setterName = setterName)
    return SyntheticDecoratorFactory().syntheticMemberDecorator(memberName = memberName,
                                                                defaultValue = default,
                                                                contract = contract,
                                                                readOnly = readOnly,
                                                                privateMemberName = privateMemberName,
                                                                memberDelegate = accessorDelegate)

@contract
def synthesize_member(member_name,
                      default = None,
                      contract = None,
                      read_only = False,
                      getter_name = None,
                      setter_name = None,
                      private_member_name = None):
    """
    When applied to a class, this decorator adds getter/setter methods to it and overrides the constructor in order to set\
    the default value of the member.
    By default, the getter will be named ``member_name``. (Ex.: ``member_name = 'member' => instance.member()``)
    
    By default, the setter will be named ``member_name`` with 'set\_' prepended it to it.
    (Ex.: ``member_name = 'member' => instance.set_member(...)``)

    By default, the private attribute containing the member's value will be named ``member_name`` with '_' prepended to it.

    Naming convention can be overridden with a custom one using :meth:`naming_convention <naming_convention>` decorator.

    :param member_name: Name of the member to synthesize.
    :type member_name: str
    :param default: Member's default value.
    :type default: *
    :param contract: Type constraint. See `PyContracts <http://andreacensi.github.com/contracts/>`_
    :type contract: *
    :param read_only: If set to ``True``, the setter will not be added to the class.
    :type read_only: bool
    :param getter_name: Custom getter name. This can be useful when the member is a boolean. (Ex.: ``is_alive``)
    :type getter_name: str|None
    :param setter_name: Custom setter name.
    :type setter_name: str|None
    :param private_member_name: Custom name for the private attribute that contains the member's value.
    :type private_member_name: str|None
"""
    accessorDelegate = AccessorDelegate(namingConvention = NamingConventionUnderscore(),
                                       getterName = getter_name,
                                       setterName = setter_name)
    return SyntheticDecoratorFactory().syntheticMemberDecorator(memberName = member_name,
                                                                defaultValue = default,
                                                                contract = contract,
                                                                readOnly = read_only,
                                                                privateMemberName = private_member_name,
                                                                memberDelegate = accessorDelegate)

@contract
def synthesizeProperty(propertyName,
                       default = None,
                       contract = None,
                       readOnly = False,
                       privateMemberName = None):
    """
    When applied to a class, this decorator adds a property to it and overrides the constructor in order to set\
    the default value of the property.

    :IMPORTANT: In order for this to work on python 2, you must use new objects that is to say that the class must inherit from object.

    By default, the private attribute containing the property's value will be named ``propertyName`` with '_' prepended to it.

    Naming convention can be overridden with a custom one using :meth:`namingConvention <namingConvention>` decorator.

    :param propertyName: Name of the property to synthesize.
    :type propertyName: str
    :param default: Property's default value.
    :type default: *
    :param contract: Type constraint. See `PyContracts <http://andreacensi.github.com/contracts/>`_
    :type contract: *
    :param readOnly: If set to ``True``, the property will not a have a setter.
    :type readOnly: bool
    :param privateMemberName: Custom name for the private attribute that contains the property's value.
    :type privateMemberName: str|None
"""
    return SyntheticDecoratorFactory().syntheticMemberDecorator(memberName = propertyName,
                                                                defaultValue = default,
                                                                contract = contract,
                                                                readOnly = readOnly,
                                                                privateMemberName = privateMemberName,
                                                                memberDelegate = PropertyDelegate())
@contract
def synthesize_property(property_name,
                        default = None,
                        contract = None,
                        read_only = False,
                        private_member_name = None):
    """
    When applied to a class, this decorator adds a property to it and overrides the constructor in order to set\
    the default value of the property.
    
    :IMPORTANT: In order for this to work on python 2, you must use new objects that is to say that the class must inherit from object.

    By default, the private attribute containing the property's value will be named ``property_name`` with '_' prepended to it.

    Naming convention can be overridden with a custom one using :meth:`naming_convention <naming_convention>` decorator.

    :param property_name: Name of the property to synthesize.
    :type property_name: str
    :param default: Property's default value.
    :type default: *
    :param contract: Type constraint. See `PyContracts <http://andreacensi.github.com/contracts/>`_
    :type contract: *
    :param read_only: If set to ``True``, the property will not a have a setter.
    :type read_only: bool
    :param private_member_name: Custom name for the private attribute that contains the property's value.
    :type private_member_name: str|None
"""
    return SyntheticDecoratorFactory().syntheticMemberDecorator(memberName = property_name,
                                                                defaultValue = default,
                                                                contract = contract,
                                                                readOnly = read_only,
                                                                privateMemberName = private_member_name,
                                                                memberDelegate = PropertyDelegate())

def synthesizeConstructor():
    """
    This class decorator will override the class's constructor by making it\
    implicitly consume values for synthesized members and properties.
"""
    return SyntheticDecoratorFactory().syntheticConstructorDecorator()


def namingConvention(namingConvention):
    """
    When applied to a class, this decorator will override the CamelCase naming convention of all (previous and following)
    :meth:`synthesizeMember` calls on the class to ``namingConvention``.

    :param namingConvention: The new naming convention.
    :type namingConvention: INamingConvention
"""
    return SyntheticDecoratorFactory().namingConventionDecorator(namingConvention)

def naming_convention(naming_convention):
    """
    When applied to a class, this decorator will override the underscore naming convention of all (previous and following)
    :meth:`synthesizeMember` calls on the class to ``naming_convention``.

    :param naming_convention: The new naming convention.
    :type naming_convention: INamingConvention
"""
    return SyntheticDecoratorFactory().namingConventionDecorator(naming_convention)  

synthesize_constructor = synthesizeConstructor
