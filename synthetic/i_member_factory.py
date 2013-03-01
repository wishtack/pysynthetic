#-*- coding: utf-8 -*-
#
# Created on Feb 28, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from abc import abstractmethod

class IMemberFactory:
    
    @abstractmethod
    def memberDict(self, memberName, getter, setter, classNamingConvention):
        raise NotImplementedError()
