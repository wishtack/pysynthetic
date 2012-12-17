#-*- coding: utf-8 -*-
#
# Created on Dec 17, 2012
#
# @author: Younes JAAIDI
#
# $Id: $
#

from synthetic.i_accessor_name_maker import IAccessorNameMaker

class AccessorNameMakerCamelCase(IAccessorNameMaker):
    
    def getterName(self, memberName):
        return memberName
    
    def setterName(self, memberName):
        memberNameFirstLetter = memberName[:1].upper()
        memberNameEnd = memberName[1:]
        return 'set%s%s' % (memberNameFirstLetter, memberNameEnd)
