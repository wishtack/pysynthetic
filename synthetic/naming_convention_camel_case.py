#-*- coding: utf-8 -*-
#
# Created on Dec 17, 2012
#
# @author: Younes JAAIDI
#
# $Id$
#

from .i_naming_convention import INamingConvention

class NamingConventionCamelCase(INamingConvention):
    
    def getterName(self, memberName):
        return memberName
    
    def setterName(self, memberName):
        memberNameFirstLetter = memberName[:1].upper()
        memberNameEnd = memberName[1:]
        return 'set%s%s' % (memberNameFirstLetter, memberNameEnd)
