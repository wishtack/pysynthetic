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
from .synthetic_member import SyntheticMember

new_contract('SyntheticMember', SyntheticMember)
new_contract('INamingConvetion', INamingConvention)

class DuplicateMemberNameError(Exception):

    @contract
    def __init__(self, memberName, className):
        """
    :type memberName: str
    :type className: str
"""
        super(DuplicateMemberNameError, self).__init__("Duplicate member name '%s' for class '%s'." % (memberName,
                                                                                                       className))
class SyntheticMetaData:

    def __init__(self, cls, originalConstructor, originalMemberNameList):
        """
    :type originalMemberNameList: list(str)
    :type namingConvention: INamingConvention|None
"""
        self._class = cls
        self._originalConstructor = originalConstructor
        self._originalMemberNameList = originalMemberNameList
        self._syntheticMemberList = []
        self._doesConsumeArguments = False
        self._namingConvention = None
    
    def originalConstructor(self):
        return self._originalConstructor

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
    
    def namingConvention(self):
        return self._namingConvention
    
    def setNamingConvention(self, namingConvention):
        """
    :type namingConvention: INamingConvention
"""
        self._namingConvention = namingConvention
