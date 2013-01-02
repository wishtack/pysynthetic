#-*- coding: utf-8 -*-
#
# Created on Dec 17, 2012
#
# @author: Younes JAAIDI
#
# $Id: $
#

from contracts import contract, new_contract
from synthetic.i_naming_convention import INamingConvention
from synthetic.synthetic_decorator_factory import SyntheticDecoratorFactory

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
                                                                privateMemberName)

def synthesizeConstructor():
    return SyntheticDecoratorFactory().syntheticConstructorDecorator()

def namingConvention(namingConvention):
    """
    :type namingConvention: INamingConvention
"""
    return SyntheticDecoratorFactory().namingConventionDecorator(namingConvention)
