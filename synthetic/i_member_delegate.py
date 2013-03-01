#-*- coding: utf-8 -*-
#
# Created on Feb 28, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from abc import abstractmethod

class IMemberDelegate:
    
    @abstractmethod
    def apply(self, cls, originalMemberNameList, memberName, classNamingConvention, getter, setter):
        raise NotImplementedError()

    @abstractmethod
    def remove(self, cls, originalMemberNameList, memberName, classNamingConvention):
        raise NotImplementedError()
