#-*- coding: utf-8 -*-
#
# Created on Feb 28, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from .i_member_factory import IMemberFactory
from .i_naming_convention import INamingConvention
from contracts import new_contract

new_contract('INamingConvention', INamingConvention)

class AccessorFactory(IMemberFactory):

    _GETTER_KEY = 'getter'
    _SETTER_KEY = 'setter'
    
    # Mappings between accessor types and their names and methods.
    # @hack: I don't much like that.
    _NAMING_CONVENTION_ACCESSOR_NAME_METHOD_DICT = {_GETTER_KEY: 'getterName',
                                                    _SETTER_KEY: 'setterName'}

    def __init__(self, namingConvention, getterName, setterName):
        """
    :type namingConvention: INamingConvention
    :type getterName: str|None
    :type setterName: str|None
"""
        self._namingConvention = namingConvention
        # Accessor names.
        self._accessorNameDict = {self._GETTER_KEY: getterName,
                                  self._SETTER_KEY: setterName}

    def memberDict(self, memberName, getter, setter, classNamingConvention):
        """
    :type classNamingConvention: INamingConvention|None
"""
        resultDict = {}
        resultDict[self._accessorName(memberName, self._GETTER_KEY, classNamingConvention)] = getter
        
        # No setter if read only member.
        if setter is not None:
            resultDict[self._accessorName(memberName, self._SETTER_KEY, classNamingConvention)] = setter
        return resultDict

    def _accessorName(self, memberName, accessorName, classNamingConvention):
        """
    :type memberName: str
    :type accessorName: str
    :type classNamingConvention: INamingConvention|None
"""        
        # Using user's custom getter or setter name.
        customAccessorName = self._accessorNameDict[accessorName]
        if customAccessorName is not None:
            return customAccessorName
        
        # If the class has a custom naming convention, we use it. Cf. 'namingConvention' decorator.
        # Otherwise, we use the member's naming convention, camelCase or underscore depending on the decorator that was used
        # (respectively synthesizeMember or synthesize_member).
        namingConvention = self._namingConvention
        if classNamingConvention is not None:
            namingConvention = classNamingConvention

        # @hack: I don't much like that...
        methodName = self._NAMING_CONVENTION_ACCESSOR_NAME_METHOD_DICT[accessorName]
        # Using naming convention to transform member's name to an accessor name.
        return getattr(namingConvention, methodName)(memberName)
