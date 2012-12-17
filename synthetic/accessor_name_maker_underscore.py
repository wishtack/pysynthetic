#-*- coding: utf-8 -*-
#
# Created on Dec 17, 2012
#
# @author: Younes JAAIDI
#
# $Id: $
#

from synthetic.i_accessor_name_maker import IAccessorNameMaker

class AccessorNameMakerUnderscore(IAccessorNameMaker):
    
    def getterName(self, memberName):
        return memberName
    
    def setterName(self, memberName):
        return 'set_%s' % memberName
