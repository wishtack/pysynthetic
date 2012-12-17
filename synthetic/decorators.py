#-*- coding: utf-8 -*-
#
# Created on Dec 17, 2012
#
# @author: Younes JAAIDI
#
# $Id: $
#

from contracts import contract
from synthetic.accessor_name_maker_camel_case import AccessorNameMakerCamelCase
from synthetic.i_accessor_name_maker import IAccessorNameMaker
from synthetic.synthetic_decorator_factory import SyntheticDecoratorFactory

@contract
def synthesizeMember(memberName : str,
               defaultValue = None,
               contract : 'str|None' = None,
               readOnly : bool = False,
               accessorNameMaker : IAccessorNameMaker = AccessorNameMakerCamelCase(),
               getterName : 'str|None' = None,
               setterName : 'str|None' = None,
               privateMemberName : 'str|None' = None):
    return SyntheticDecoratorFactory().syntheticMemberDecorator(memberName,
                                                                defaultValue,
                                                                contract,
                                                                readOnly,
                                                                accessorNameMaker,
                                                                getterName,
                                                                setterName,
                                                                privateMemberName)

def synthesizeConstructor():
    return SyntheticDecoratorFactory().syntheticConstructorDecorator()
