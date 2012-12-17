#-*- coding: utf-8 -*-
#
# Created on Dec 17, 2012
#
# @author: Younes JAAIDI
#
# $Id: $
#

from abc import abstractmethod

class IAccessorNameMaker:
    
    @abstractmethod
    def getterName(self, memberName):
        raise NotImplementedError()

    @abstractmethod
    def setterName(self, memberName):
        raise NotImplementedError()
