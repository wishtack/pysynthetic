#-*- coding: utf-8 -*-
#
# Created on Dec 17, 2012
#
# @author: Younes JAAIDI
#
# $Id$
#

from .i_naming_convention import INamingConvention
from contracts import contract, new_contract, parse
import contracts

new_contract('INamingConvention', INamingConvention)

class SyntheticMember:
    
    _GETTER_KEY = 'getter'
    _SETTER_KEY = 'setter'

    # Mappings between accessor types and their names and methods.
    # @hack: I don't much like that.
    _NAMING_CONVENTION_ACCESSOR_NAME_METHOD_DICT = {_GETTER_KEY: 'getterName',
                                                    _SETTER_KEY: 'setterName'}
    
    @contract
    def __init__(self,
                 memberName,
                 defaultValue,
                 contract,
                 readOnly,
                 getterName,
                 setterName,
                 privateMemberName,
                 namingConvention):
        """
    :type memberName: str
    :type readOnly: bool
    :type getterName: str|None
    :type setterName: str|None
    :type privateMemberName: str|None
    :type namingConvention: INamingConvention
"""

        if privateMemberName is None:
            privateMemberName = '_%s' % memberName

        if contract is not None:
            contract = parse(contract)
            
        self._memberName = memberName
        self._defaultValue = defaultValue
        self._contract = contract
        self._readOnly = readOnly
        self._privateMemberName = privateMemberName
        self._namingConvention = namingConvention

        # Accessor names.
        self._accessorNameDict = {self._GETTER_KEY: getterName,
                                  self._SETTER_KEY: setterName}

    def memberName(self):
        return self._memberName
    
    def defaultValue(self):
        return self._defaultValue
    
    def contract(self):
        return self._contract
    
    def accessorDict(self, classNamingConvention):
        resultDict = {}
        resultDict[self._accessorName(self._GETTER_KEY, classNamingConvention)] = self._makeGetter()
        
        # No setter if read only member.
        if not self._readOnly:
            resultDict[self._accessorName(self._SETTER_KEY, classNamingConvention)] = self._makeSetter()
        return resultDict
    
    def privateMemberName(self):
        return self._privateMemberName

    def checkContract(self, argumentName, value):
        # No contract to check.
        if self._contract is None:
            return
        
        # Contracts are disabled.
        if contracts.all_disabled():
            return
        
        self._contract._check_contract(value = value, context = {argumentName: value})

    def _accessorName(self, accessorName, classNamingConvention):
        """
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
        return getattr(namingConvention, methodName)(self._memberName)

    def _makeGetter(self):
        def getter(instance):
            return getattr(instance, self.privateMemberName())

        return getter
    
    def _makeSetter(self):
        def setter(instance, value):
            if self._contract is not None:
                self.checkContract(self._memberName, value)
            setattr(instance, self.privateMemberName(), value)

        return setter
