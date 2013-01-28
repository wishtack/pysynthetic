#-*- coding: utf-8 -*-
#
# Created on Dec 17, 2012
#
# @author: Younes JAAIDI
#
# $Id$
#

from contracts import contract, new_contract
from synthetic.i_naming_convention import INamingConvention
from synthetic.synthetic_class_controller import SyntheticClassController
from synthetic.synthetic_member import SyntheticMember

new_contract('INamingConvention', INamingConvention)
new_contract('SyntheticMember', SyntheticMember)

class SyntheticDecoratorFactory:

    @contract
    def syntheticMemberDecorator(self,
                                 memberName,
                                 defaultValue,
                                 contract,
                                 readOnly,
                                 getterName,
                                 setterName,
                                 privateMemberName):
        """
    :type memberName: str
    :type readOnly: bool
    :type getterName: str|None
    :type setterName: str|None
    :type privateMemberName: str|None
"""
        def decoratorFunction(cls):
            syntheticMember = SyntheticMember(memberName,
                                              defaultValue,
                                              contract,
                                              readOnly,
                                              getterName,
                                              setterName,
                                              privateMemberName)

            SyntheticClassController(cls).addSyntheticMember(syntheticMember)

            return cls
        return decoratorFunction

    def syntheticConstructorDecorator(self):
        def functionWrapper(cls):            
            # This will be used later to tell the new constructor to consume parameters to initialize members.
            SyntheticClassController(cls).synthesizeConstructor()

            return cls
        return functionWrapper
    
    def namingConventionDecorator(self, namingConvention):
        """
    :type namingConvention:INamingConvention
"""
        def decoratorFunction(cls):
            SyntheticClassController(cls).setNamingConvention(namingConvention)
            
            return cls
        return decoratorFunction
