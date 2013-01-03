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
from synthetic.synthetic_member import SyntheticMember

new_contract('SyntheticMember', SyntheticMember)
new_contract('INamingConvetion', INamingConvention)

class SyntheticMetaData:
    def __init__(self, originalConstructor, namingConvention):
        """
    :type namingConvention: INamingConvention
"""
        self._originalConstructor = originalConstructor
        self._syntheticMemberList = []
        self._doesConsumeArguments = False
        self._namingConvention = namingConvention
    
    def originalConstructor(self):
        return self._originalConstructor

    @contract
    def insertSyntheticMemberAtBegin(self, synthesizedMember):
        """
    :type synthesizedMember: SyntheticMember 
"""
        self._syntheticMemberList.insert(0, synthesizedMember)
    
    def syntheticMemberList(self):
        return self._syntheticMemberList
    
    def doesConsumeArguments(self):
        """Tells if the generated constructor must consume parameters or just use the default values."""
        return self._doesConsumeArguments

    def setConsumeArguments(self, _consumeArguments):
        self._doesConsumeArguments = _consumeArguments
    
    def namingConvention(self):
        return self._namingConvention
    
    def setNamingConvention(self, namingConvention):
        """
    :type namingConvention: INamingConvention
"""
        self._namingConvention = namingConvention
