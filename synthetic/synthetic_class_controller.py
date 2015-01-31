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
        self._updateConstructorAndMembers()
    
    def synthesizeConstructor(self):
        self._syntheticMetaData().setConsumeArguments(True)

        # Update constructor and recreate accessors.
        self._updateConstructorAndMembers()
    
    @contract
    def setNamingConvention(self, namingConvention):
        """
    :type namingConvention: INamingConvention
"""
        # Remove getters and setters with old naming convention.
        self._removeSyntheticMembers()
        
        # Set new naming convention.
        self._syntheticMetaData().setNamingConvention(namingConvention)

        # Update constructor and recreate accessors.
        self._updateConstructorAndMembers()

    def _syntheticMetaData(self):
        # SyntheticMetaData does not exist...
        syntheticMetaDataName = '__syntheticMetaData__{className}'.format(className=self._class.__name__)
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

    def _updateConstructorAndMembers(self):
        """We overwrite constructor and accessors every time because the constructor might have to consume all
members even if their decorator is below the "synthesizeConstructor" decorator and it also might need to update
the getters and setters because the naming convention has changed.
"""
        syntheticMetaData = self._syntheticMetaData()
        constructor = self._constructorFactory.makeConstructor(syntheticMetaData.originalConstructor(),
                                                               syntheticMetaData.syntheticMemberList(),
                                                               syntheticMetaData.doesConsumeArguments())

        self._class.__init__ = constructor
        for syntheticMember in syntheticMetaData.syntheticMemberList():
            syntheticMember.apply(self._class,
                                  syntheticMetaData.originalMemberNameList(),
                                  syntheticMetaData.namingConvention())

    def _removeSyntheticMembers(self):
        syntheticMetaData = self._syntheticMetaData()
        for syntheticMember in syntheticMetaData.syntheticMemberList():
            syntheticMember.remove(self._class,
                                   syntheticMetaData.originalMemberNameList(),
                                   syntheticMetaData.namingConvention())
