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
def synthesizeMember(memberName : str,
               defaultValue = None,
               contract : 'str|None' = None,
               readOnly : bool = False,
               namingConvention : INamingConvention = NamingConventionCamelCase(),
               getterName : 'str|None' = None,
               setterName : 'str|None' = None,
               privateMemberName : 'str|None' = None):
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
