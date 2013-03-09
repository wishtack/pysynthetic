#-*- coding: utf-8 -*-
#
# Created on Dec 17, 2012
#
# @author: Younes JAAIDI
#
# $Id$
#

from .i_member_delegate import IMemberDelegate
from .i_naming_convention import INamingConvention
from contracts import contract, new_contract, parse
import contracts

new_contract('IMemberDelegate', IMemberDelegate)
new_contract('INamingConvention', INamingConvention)

class SyntheticMember:
    
    @contract
    def __init__(self,
                 memberName,
                 default,
                 contract,
                 readOnly,
                 privateMemberName,
                 memberDelegate):
        """
    :type memberName: str
    :type readOnly: bool
    :type privateMemberName: str|None
    :type memberDelegate: IMemberDelegate

"""

        if privateMemberName is None:
            privateMemberName = '_%s' % memberName

        if contract is not None:
            contract = parse(contract)
            
        self._memberName = memberName
        self._default = default
        self._contract = contract
        self._readOnly = readOnly
        self._privateMemberName = privateMemberName
        self._memberDelegate = memberDelegate


    def memberName(self):
        return self._memberName
    
    def default(self):
        return self._default
    
    def privateMemberName(self):
        return self._privateMemberName

    def checkContract(self, argumentName, value):
        # No contract to check.
        if self._contract is None:
            return
        
        # Contracts are disabled.
        if contracts.all_disabled():
            return
        
        self._contract._check_contract(value = value, context = {argumentName: value})

    def apply(self, cls, originalMemberNameList, classNamingConvention):
        """
    :type cls: type
    :type originalMemberNameList: list(str)
    :type classNamingConvention: INamingConvention
"""
        self._memberDelegate.apply(cls = cls,
                                   originalMemberNameList = originalMemberNameList,
                                   memberName = self._memberName,
                                   classNamingConvention = classNamingConvention,
                                   getter = self._makeGetter(),
                                   setter = self._makeSetter())

    def remove(self, cls, originalMemberNameList, classNamingConvention):
        """
    :type cls: type
    :type originalMemberNameList: list(str)
    :type classNamingConvention: INamingConvention
"""
        self._memberDelegate.remove(cls = cls,
                                    originalMemberNameList = originalMemberNameList,
                                    memberName = self._memberName,
                                    classNamingConvention = classNamingConvention)

    def _makeGetter(self):
        def getter(instance):
            return getattr(instance, self._privateMemberName)

        return getter
    
    def _makeSetter(self):
        if self._readOnly:
            return None
        
        def setter(instance, value):
            if self._contract is not None:
                self.checkContract(self._memberName, value)
            setattr(instance, self._privateMemberName, value)

        return setter
