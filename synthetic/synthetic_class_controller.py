#-*- coding: utf-8 -*-
#
# Created on Jan 3, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from .i_naming_convention import INamingConvention
from .synthetic_constructor_factory import SyntheticConstructorFactory
from .synthetic_member import SyntheticMember
from .synthetic_meta_data import SyntheticMetaData
from contracts import contract, new_contract
import inspect

new_contract('INamingConvention', INamingConvention)
new_contract('SyntheticMember', SyntheticMember)

class SyntheticClassController:
    
    def __init__(self, cls):
        self._constructorFactory = SyntheticConstructorFactory()
        self._class = cls
    
    @contract
    def addSyntheticMember(self, syntheticMember):
        """
    :type syntheticMember: SyntheticMember
"""
        # Inserting this member at the beginning of the member list of synthesization data attribute
        # because decorators are called in reversed order.
        self._syntheticMetaData().insertSyntheticMemberAtBegin(syntheticMember)

        # Update constructor and recreate accessors.
        self._updateConstructorAndAccessors()
    
    def synthesizeConstructor(self):
        self._syntheticMetaData().setConsumeArguments(True)

        # Update constructor and recreate accessors.
        self._updateConstructorAndAccessors()
    
    @contract
    def setNamingConvention(self, namingConvention):
        """
    :type namingConvention: INamingConvention
"""
        # Remove getters and setters with old naming convention.
        self._removeAccessorForEveryMember()
        
        # Set new naming convention.
        self._syntheticMetaData().setNamingConvention(namingConvention)

        # Update constructor and recreate accessors.
        self._updateConstructorAndAccessors()

    def _syntheticMetaData(self):
        # SyntheticMetaData does not exist...
        syntheticMetaDataName = '__syntheticMetaData__'
        if not hasattr(self._class, syntheticMetaDataName):
            # ...we create it.
            originalConstructor = getattr(self._class, '__init__', None)
            
            # List of existing methods (Python2: ismethod, Python3: isfunction).
            originalMemberList = inspect.getmembers(self._class)
            originalMemberNameList = [method[0] for method in originalMemberList]

            # Making the synthetic meta data.
            syntheticMetaData = SyntheticMetaData(cls = self._class,
                                                  originalConstructor = originalConstructor,
                                                  originalMemberNameList = originalMemberNameList)
            setattr(self._class, syntheticMetaDataName, syntheticMetaData)
        return getattr(self._class, syntheticMetaDataName)

    def _updateConstructorAndAccessors(self):
        """We overwrite constructor and accessors every time because the constructor might have to consume all
members even if their decorator is below the "synthesizeConstructor" decorator and it also might need to update
the getters and setters because the naming convention has changed.
"""
        syntheticMetaData = self._syntheticMetaData()
        constructor = self._constructorFactory.makeConstructor(syntheticMetaData.originalConstructor(),
                                                               syntheticMetaData.syntheticMemberList(),
                                                               syntheticMetaData.doesConsumeArguments())
        self._class.__init__ = constructor
        self._makeAccessorForEveryMember()

    def _makeAccessorForEveryMember(self):
        for memberName, member in self._memberIterable():
            self._tryToSetMember(memberName, member)

    def _removeAccessorForEveryMember(self):
        for memberName, _ in self._memberIterable():
            self._tryRemoveMember(memberName)
    
    def _memberIterable(self):
        syntheticMetaData = self._syntheticMetaData()
        classNamingConvention = syntheticMetaData.namingConvention()
        for syntheticMember in syntheticMetaData.syntheticMemberList():
            memberDict = syntheticMember.memberDict(classNamingConvention)
            for memberName, member in memberDict.items():
                yield memberName, member

    @contract
    def _tryToSetMember(self, accessorName, accessor):
        """
    :type accessorName: str
"""
        # Don't synthesize accessor if it is overriden by the user.
        if accessorName in self._syntheticMetaData().originalMemberNameList():
            return
        
        setattr(self._class, accessorName, accessor)

    @contract
    def _tryRemoveMember(self, accessorName):
        """
    :type accessorName: str
"""
        # Don't remove accessor if it is overriden by the user.
        if accessorName in self._syntheticMetaData().originalMemberNameList():
            return
        
        delattr(self._class, accessorName)
