#-*- coding: utf-8 -*-
#
# Created on Dec 17, 2012
#
# @author: Younes JAAIDI
#
# $Id: $
#

from contracts import contract
from synthetic.naming_convention_camel_case import NamingConventionCamelCase
from synthetic.i_naming_convention import INamingConvention
from synthetic.synthetic_decorator_factory import SyntheticDecoratorFactory

@contract
def synthesizeMember(memberName,
               defaultValue = None,
               contract = None,
               readOnly = False,
               namingConvention = NamingConventionCamelCase(),
               getterName = None,
               setterName = None,
               privateMemberName = None):
    """
        :type memberName: str
        :type readOnly: bool
        :type namingConvention: INamingConvention
        :type getterName: str|None
        :type setterName: str|None
        :type privateMemberName: str|None
    """
    return SyntheticDecoratorFactory().syntheticMemberDecorator(memberName,
                                                                defaultValue,
                                                                contract,
                                                                readOnly,
                                                                namingConvention,
                                                                getterName,
                                                                setterName,
                                                                privateMemberName)

def synthesizeConstructor():
    return SyntheticDecoratorFactory().syntheticConstructorDecorator()
