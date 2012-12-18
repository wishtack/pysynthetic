#-*- coding: utf-8 -*-
#
# Created on Dec 17, 2012
#
# @author: Younes JAAIDI
#
# $Id: $
#

from contracts import contract
import inspect

from synthetic.i_naming_convention import INamingConvention
from synthetic.synthetic_meta_data import SyntheticMetaData
from synthetic.synthetic_member import SyntheticMember

class SyntheticDecoratorFactory:

    @contract
    def syntheticMemberDecorator(self,
                                 memberName : str,
                                 defaultValue,
                                 contract : 'str|None',
                                 readOnly : bool,
                                 namingConvention : INamingConvention,
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
            cls.__syntheticMetaData__.insertSyntheticMemberAtBegin(syntheticMember)
            
            self._overrideConstructor(cls)
            self._makeGetter(cls, namingConvention, syntheticMember)
            self._makeSetter(cls, namingConvention, syntheticMember)
            return cls
        return decoratorFunction

    def syntheticConstructorDecorator(self):
        def decoratorFunction(cls):
            # Creating synthesization data if it does not exist.
            self._makeSyntheticDataIfNotExists(cls)
            
            # This will be used later to tell the new constructor to consume parameters to initialize members.
            cls.__syntheticMetaData__.setConsumeArguments(True)
            
            self._overrideConstructor(cls)
            return cls
        return decoratorFunction

    def _makeSyntheticDataIfNotExists(self, cls):
        if not hasattr(cls, '__syntheticMetaData__'):
            cls.__syntheticMetaData__ = SyntheticMetaData(originalConstructor = cls.__init__)

    def _overrideConstructor(self, cls):
        # Retrieving synthesized member list and original init method.
        originalConstructor = cls.__syntheticMetaData__.originalConstructor()
        syntheticMemberList = cls.__syntheticMetaData__.syntheticMemberList()
        doesConsumeArguments = cls.__syntheticMetaData__.doesConsumeArguments()
        
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

    def _makeGetter(self, cls, namingConvention, syntheticMember):
        def getter(instance):
            return getattr(instance, syntheticMember.privateMemberName())
        setattr(cls, self._getterName(namingConvention, syntheticMember), getter)
    
    def _makeSetter(self, cls, namingConvention, syntheticMember):
        # No setter if read only member.
        if syntheticMember.isReadOnly():
            return
        
        def setter(instance, value):
            setattr(instance, syntheticMember.privateMemberName(), value)
        setattr(cls, self._setterName(namingConvention, syntheticMember), setter)

    def _getterName(self, namingConvention, syntheticMember):
        getterName = syntheticMember.getterName()
        if getterName is None:
            getterName = namingConvention.getterName(syntheticMember.memberName())
        return getterName
    
    def _setterName(self, namingConvention, syntheticMember):
        setterName = syntheticMember.setterName()
        if setterName is None:
            setterName = namingConvention.setterName(syntheticMember.memberName())
        return setterName
