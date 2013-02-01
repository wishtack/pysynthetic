#-*- coding: utf-8 -*-
#
# Created on Dec 17, 2012
#
# @author: Younes JAAIDI
#
# $Id$
#

from contracts import contract

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
