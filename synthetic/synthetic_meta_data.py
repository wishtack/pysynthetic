#-*- coding: utf-8 -*-
#
# Created on Dec 17, 2012
#
# @author: Younes JAAIDI
#
# $Id: $
#
from contracts import contract

from synthetic.synthetic_member import SyntheticMember

class SyntheticMetaData:
    def __init__(self, originalConstructor):
        self._originalConstructor = originalConstructor
        self._syntheticMemberList = []
        self._doesConsumeArguments = False
    
    def originalConstructor(self):
        return self._originalConstructor

    @contract
    def insertSyntheticMemberAtBegin(self, synthesizedMember : SyntheticMember):
        self._syntheticMemberList.insert(0, synthesizedMember)
    
    def syntheticMemberList(self):
        return self._syntheticMemberList
    
    def doesConsumeArguments(self):
        """Tells if the generated constructor must consume parameters or just use the default values."""
        return self._doesConsumeArguments

    def setConsumeArguments(self, _consumeArguments):
        self._doesConsumeArguments = _consumeArguments
