#-*- coding: utf-8 -*-
#
# Created on Dec 14, 2012
#
# @author: Younes JAAIDI
#
# $Id: $
#

from abc import abstractmethod
from contracts import contract
from types import FunctionType

class AccessorNameMaker:
    
    @abstractmethod
    def getterName(self, memberName):
        raise NotImplementedError()

    @abstractmethod
    def setterName(self, memberName):
        raise NotImplementedError()

class AccessorNameMakerCamelCase(AccessorNameMaker):
    
    def getterName(self, memberName):
        return memberName
    
    def setterName(self, memberName):
        memberNameFirstLetter = memberName[:1].upper()
        memberNameEnd = memberName[1:]
        return 'set%s%s' % (memberNameFirstLetter, memberNameEnd)

class AccessorNameMakerUnderscore(AccessorNameMaker):
    
    def getterName(self, memberName):
        return memberName
    
    def setterName(self, memberName):
        return 'set_%s' % memberName

class SynthesizedMember:
    @contract
    def __init__(self,
                 memberName : str,
                 defaultValue,
                 contract : 'string|None',
                 accessorNameMaker : AccessorNameMaker,
                 getterName : 'string|None',
                 setterName : 'string|None',
                 privateMemberName : 'string|None'):
        
        if getterName is None:
            getterName = accessorNameMaker.getterName(memberName)

        if setterName is None:
            setterName = accessorNameMaker.setterName(memberName)
        
        if privateMemberName is None:
            privateMemberName = '_%s' % memberName
            
        self._memberName = memberName
        self._defaultValue = defaultValue
        self._contract = contract
        self._accessorNameMaker = accessorNameMaker
        self._getterName = getterName
        self._setterName = setterName
        self._privateMemberName = privateMemberName
        
        # Making getter/setter and decorator.
        self._getter = self._makeGetter()
        self._setter = self._makeSetter()
        self._decorator = self._makeDecorator()

    def decorator(self):
        return self._decorator

    def _makeDecorator(self):
        def decoratorFunction(cls):
            setattr(cls, '__init__', self._makeInit(cls)) 
            setattr(cls, self._getterName, self._getter)
            setattr(cls, self._setterName, self._setter)        
            return cls
        return decoratorFunction

    def _makeInit(self, cls):
        # @todo MemberSynthesizationData with SynthesizedMemberList and OriginalInitMethod.
        cls._originalInitMethod = getattr(cls, '_originalInitMethod', getattr(cls, '__init__'))
        
        def init(instance, *args, **kwargs):
            setattr(instance, self._privateMemberName, self._defaultValue)
            cls._originalInitMethod(instance, *args, **kwargs)
        return init

    def _makeGetter(self):
        def getter(instance):
            return getattr(instance, self._privateMemberName)
        return getter
    
    def _makeSetter(self):
        def setter(instance, value):
            setattr(instance, self._privateMemberName, value)
        return setter
    

@contract
def synthesizeMember(memberName : str,
               defaultValue : 'str|None' = None,
               contract : 'str|None' = None,
               accessorNameMaker : AccessorNameMaker = AccessorNameMakerCamelCase(),
               getterName : 'str|None' = None,
               setterName : 'str|None' = None,
               privateMemberName : 'str|None' = None):
    return SynthesizedMember(memberName, defaultValue, contract, accessorNameMaker, getterName, setterName, privateMemberName).decorator()

# @todo: synthesizeProperty

# @todo: synthesizeInit

