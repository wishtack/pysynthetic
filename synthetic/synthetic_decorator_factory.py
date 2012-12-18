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
import inspect



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
            self._makeSyntheticDataIfNotExists(cls)
            
            # Inserting this member at the beginning of the member list of synthesization data attribute
            # because decorators are called in reversed order.
            cls._syntheticData.insertSyntheticMemberAtBegin(syntheticMember)
            
            self._overrideConstructor(cls)
            self._makeGetter(cls, accessorNameMaker, syntheticMember)
            self._makeSetter(cls, accessorNameMaker, syntheticMember)
            return cls
        return decoratorFunction

    def syntheticConstructorDecorator(self):
        def decoratorFunction(cls):
            # Creating synthesization data if it does not exist.
            self._makeSyntheticDataIfNotExists(cls)
            
            # This will be used later to tell the new constructor to consume parameters to initialize members.
            cls._syntheticData.setConsumeArguments(True)
            
            self._overrideConstructor(cls)
            return cls
        return decoratorFunction

    def _makeSyntheticDataIfNotExists(self, cls):
        if not hasattr(cls, '_syntheticData'):
            cls._syntheticData = SyntheticData(originalConstructor = cls.__init__)

    def _overrideConstructor(self, cls):
        # Retrieving synthesized member list and original init method.
        originalConstructor = cls._syntheticData.originalConstructor()
        syntheticMemberList = cls._syntheticData.syntheticMemberList()
        doesConsumeArguments = cls._syntheticData.doesConsumeArguments()
        
        # New init method that initializes members and calls the original init method.
        def init(instance, *args, **kwargs):
            # _consumeParameters will tell us which arguments have been used in order to remove them.
            argList = list(args)
            
            # We initialize members in a reversed order in order to be able to remove used args just after using them.
            for index, syntheticMember in reversed(list(enumerate(syntheticMemberList))):
                memberName = syntheticMember.memberName()
                
                # Default value.
                value = syntheticMember.defaultValue()

                # Tells if the argument is expected to be used by the original constructor.
                mustKeepArgument = self._mustKeepArgument(originalConstructor, memberName)
                
                if doesConsumeArguments:
                    value = self._consumeArgument(memberName,
                                                  index,
                                                  argList,
                                                  kwargs,
                                                  value,
                                                  mustKeepArgument)
                
                # Initalizing member with a value.
                setattr(instance,
                        syntheticMember.privateMemberName(),
                        value)
            
            originalConstructor(instance, *argList, **kwargs)
        
        # Setting init method.
        cls.__init__ = init

    @contract
    def _consumeArgument(self,
                         memberName: str,
                         memberIndex: int,
                         argList: list,
                         kwargs: dict,
                         defaultValue,
                         mustKeepArgument: bool):
        """Returns member's value from kwargs if found or from args if found or default value otherwise.
It will also remove used values from kwargs and args after using them."""
        
        value = defaultValue
        
        # Using value from args.
        if len(argList) > memberIndex:
            value = argList[memberIndex]
            # Removing value from args.
            if not mustKeepArgument:
                del argList[memberIndex]
        
        # Using value from kwargs.
        if memberName in kwargs:
            value = kwargs[memberName]
            if not mustKeepArgument:
                del kwargs[memberName]
        
        return value

    @contract
    def _mustKeepArgument(self, originalConstructor, memberName: str):
        if not inspect.isfunction(originalConstructor):
            return False
        
        argSpec = inspect.getargspec(originalConstructor)
        
        # Original constructor is expecting variadic arguments or keyworded arguments.
        if argSpec.varargs is not None or argSpec.keywords is not None:
            return True
        
        # Argument is expected.
        if memberName in argSpec.args:
            return True
        
        return False

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
