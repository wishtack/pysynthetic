#-*- coding: utf-8 -*-
#
# Created on Dec 17, 2012
#
# @author: Younes JAAIDI
#
# $Id: $
#

from contracts import contract

from synthetic.i_accessor_name_maker import IAccessorNameMaker
from synthetic.synthetic_data import SyntheticData
from synthetic.synthetic_member import SyntheticMember


class SyntheticDecoratorFactory:

    @contract
    def syntheticMemberDecorator(self,
                                 memberName : str,
                                 defaultValue,
                                 contract : 'str|None',
                                 readOnly : bool,
                                 accessorNameMaker : IAccessorNameMaker,
                                 getterName : 'str|None',
                                 setterName : 'str|None',
                                 privateMemberName : 'str|None'):
        syntheticMember = SyntheticMember(memberName,
                                          defaultValue,
                                          contract,
                                          readOnly,
                                          getterName,
                                          setterName,
                                          privateMemberName)
        
        def decoratorFunction(cls):
            # Creating synthesization data if it does not exist.
            self._makeSyntheticData(cls)
            
            # Adding this member to synthesization data attribute.
            cls._syntheticData.appendSyntheticMember(syntheticMember)
            
            self._overrideInit(cls)
            self._makeGetter(cls, accessorNameMaker, syntheticMember)
            self._makeSetter(cls, accessorNameMaker, syntheticMember)
            return cls
        return decoratorFunction

    def _makeSyntheticData(self, cls):
        if not hasattr(cls, '_syntheticData'):
            cls._syntheticData = SyntheticData(originalInitMethod = cls.__init__)

    def _overrideInit(self, cls):
        # Retrieving synthesized member list and original init method.
        originalInitMethod = cls._syntheticData.originalInitMethod()
        syntheticMemberList = cls._syntheticData.syntheticMemberList()
        
        # New init method that initializes members and calls the original init method.
        def init(instance, *args, **kwargs):
            for syntheticMember in syntheticMemberList:
                setattr(instance,
                        syntheticMember.privateMemberName(),
                        syntheticMember.defaultValue())
            originalInitMethod(instance, *args, **kwargs)
        
        # Setting init method.
        cls.__init__ = init

    def _makeGetter(self, cls, accessorNameMaker, syntheticMember):
        def getter(instance):
            return getattr(instance, syntheticMember.privateMemberName())
        setattr(cls, self._getterName(accessorNameMaker, syntheticMember), getter)
    
    def _makeSetter(self, cls, accessorNameMaker, syntheticMember):
        # No setter if read only member.
        if syntheticMember.isReadOnly():
            return
        
        def setter(instance, value):
            setattr(instance, syntheticMember.privateMemberName(), value)
        setattr(cls, self._setterName(accessorNameMaker, syntheticMember), setter)

    def _getterName(self, accessorNameMaker, syntheticMember):
        getterName = syntheticMember.getterName()
        if getterName is None:
            getterName = accessorNameMaker.getterName(syntheticMember.memberName())
        return getterName
    
    def _setterName(self, accessorNameMaker, syntheticMember):
        setterName = syntheticMember.setterName()
        if setterName is None:
            setterName = accessorNameMaker.setterName(syntheticMember.memberName())
        return setterName
