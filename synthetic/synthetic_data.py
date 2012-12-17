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

class SyntheticData:
    def __init__(self, originalInitMethod):
        self._originalInitMethod = originalInitMethod
        self._syntheticMemberList = []
    
    def originalInitMethod(self):
        return self._originalInitMethod

    @contract
    def appendSyntheticMember(self, synthesizedMember : SyntheticMember):
        self._syntheticMemberList.append(synthesizedMember)
    
    def syntheticMemberList(self):
        return self._syntheticMemberList
