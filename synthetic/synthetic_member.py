#-*- coding: utf-8 -*-
#
# Created on Dec 17, 2012
#
# @author: Younes JAAIDI
#
# $Id$
#

from contracts import contract, parse

class SyntheticMember:
    @contract
    def __init__(self,
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

        if privateMemberName is None:
            privateMemberName = '_%s' % memberName

        if contract is not None:
            contract = parse(contract)
            
        self._memberName = memberName
        self._defaultValue = defaultValue
        self._contract = contract
        self._readOnly = readOnly
        self._getterName = getterName
        self._setterName = setterName
        self._privateMemberName = privateMemberName

    def memberName(self):
        return self._memberName
    
    def defaultValue(self):
        return self._defaultValue
    
    def contract(self):
        return self._contract
    
    def isReadOnly(self):
        return self._readOnly
    
    def getterName(self):
        return self._getterName
    
    def setterName(self):
        return self._setterName

    def privateMemberName(self):
        return self._privateMemberName

    def getter(self):
        def getter(instance):
            return getattr(instance, self.privateMemberName())

        return getter
    
    def setter(self):
        # No setter if read only member.
        if self.isReadOnly():
            return None
        
        def setter(instance, value):
            if self._contract is not None:
                self.checkContract(self._memberName, value)
            setattr(instance, self.privateMemberName(), value)

        return setter

    def checkContract(self, argumentName, value):
        if self._contract is not None:
            self._contract._check_contract(value = value, context = {argumentName: value})
