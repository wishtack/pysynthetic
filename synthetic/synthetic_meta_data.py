#-*- coding: utf-8 -*-
#
# Created on Dec 17, 2012
#
# @author: Younes JAAIDI
#
# $Id$
#

from .exceptions import SyntheticError
from .i_naming_convention import INamingConvention
from .synthetic_member import SyntheticMember
from contracts import contract, new_contract

new_contract('SyntheticMember', SyntheticMember)
new_contract('INamingConvetion', INamingConvention)

class DuplicateMemberNameError(SyntheticError):

    @contract
    def __init__(self, memberName, className):
        """
    :type memberName: str
    :type className: str
"""
        super(DuplicateMemberNameError, self).__init__("Duplicate member name '%s' for class '%s'." % (memberName,
                                                                                                       className))

class SyntheticMetaData:

    def __init__(self, cls, originalConstructor, originalEqualFunction, originalNotEqualFunction, originalHashFuction, originalMemberNameList):
        """
        :type originalMemberNameList: list(str)
        :type namingConvention: INamingConvention|None
        """
        self._class = cls
        self._originalConstructor = originalConstructor
        self._originalEqualFunction = originalEqualFunction
        self._originalNotEqualFunction = originalNotEqualFunction
        self._originalHashFunction = originalHashFuction
        self._originalMemberNameList = originalMemberNameList
        self._syntheticMemberList = []
        self._doesConsumeArguments = False
        self._hasEqualityGeneration = False
        self._namingConvention = None
    
    def originalConstructor(self):
        return self._originalConstructor

    def originalEqualFunction(self):
        return self._originalEqualFunction

    def originalNotEqualFunction(self):
        return self._originalNotEqualFunction

    def originalHashFunction(self):
        return self._originalHashFunction

    def originalMemberNameList(self):
        return self._originalMemberNameList

    @contract
    def insertSyntheticMemberAtBegin(self, synthesizedMember):
        """
    :type synthesizedMember: SyntheticMember
    :raises DuplicateMemberNameError
"""
        memberName = synthesizedMember.memberName()
        if memberName in [m.memberName() for m in self._syntheticMemberList]:
            raise DuplicateMemberNameError(memberName, self._class.__name__)
        
        self._syntheticMemberList.insert(0, synthesizedMember)
    
    def syntheticMemberList(self):
        return self._syntheticMemberList
    
    def doesConsumeArguments(self):
        """Tells if the generated constructor must consume parameters or just use the default values."""
        return self._doesConsumeArguments

    def setConsumeArguments(self, _consumeArguments):
        self._doesConsumeArguments = _consumeArguments

    def hasEqualityGeneration(self):
        """Tells if __eq__ and __neq__ functions should be generated"""
        return self._hasEqualityGeneration

    def setEqualityGeneration(self, equalityGeneration):
        self._hasEqualityGeneration = equalityGeneration
    
    def namingConvention(self):
        return self._namingConvention
    
    def setNamingConvention(self, namingConvention):
        """
    :type namingConvention: INamingConvention
"""
        self._namingConvention = namingConvention
