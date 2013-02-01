#-*- coding: utf-8 -*-
#
# Created on Jan 3, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#
from contracts import check, contract, new_contract
from .synthetic_member import SyntheticMember
import copy
import inspect

new_contract('SyntheticMember', SyntheticMember)

class SyntheticConstructorFactory:

    @contract
    def makeConstructor(self, originalConstructor, syntheticMemberList, doesConsumeArguments):
        """
    :type syntheticMemberList: list(SyntheticMember)
    :type doesConsumeArguments: bool
"""

        # Original constructor's expected args.
        originalConstructorExpectedArgList = []
        doesExpectVariadicArgs = False
        doesExpectKeywordedArgs = False
        
        if inspect.isfunction(originalConstructor) or inspect.ismethod(originalConstructor):
            argSpec = inspect.getargspec(originalConstructor)
            # originalConstructorExpectedArgList = expected args - self.
            originalConstructorExpectedArgList = argSpec.args[1:]
            doesExpectVariadicArgs = (argSpec.varargs is not None)
            doesExpectKeywordedArgs = (argSpec.keywords is not None)
        
        def init(instance, *args, **kwargs):

            if doesConsumeArguments:
                # Merge original constructor's args specification with member list and make an args dict.
                positionalArgumentKeyValueList = self._positionalArgumentKeyValueList(originalConstructorExpectedArgList,
                                                                                    syntheticMemberList,
                                                                                    args)

            # Set members values.
            for syntheticMember in syntheticMemberList:
                memberName = syntheticMember.memberName()
                
                # Default value.
                value = syntheticMember.defaultValue()

                # Constructor is synthesized.
                if doesConsumeArguments:
                    value = self._consumeArgument(memberName,
                                                  positionalArgumentKeyValueList,
                                                  kwargs,
                                                  value)

                    # Checking that the contract is respected.
                    syntheticMember.checkContract(value)

                # Initalizing member with a value.
                setattr(instance,
                        syntheticMember.privateMemberName(),
                        value)

            if doesConsumeArguments:
                # Remove superfluous arguments that have been used for synthesization but are not expected by constructor.
                args, kwargs = self._filterArgsAndKwargs(originalConstructorExpectedArgList,
                                                         doesExpectVariadicArgs,
                                                         doesExpectKeywordedArgs,
                                                         syntheticMemberList,
                                                         positionalArgumentKeyValueList,
                                                         kwargs)
            # Call original constructor.
            if originalConstructor is not None:
                originalConstructor(instance, *args, **kwargs)
        
        return init

    @contract
    def _positionalArgumentKeyValueList(self,
                                        originalConstructorExpectedArgList,
                                        syntheticMemberList,
                                        argTuple):
        """Transforms args tuple to a dictionary mapping argument names to values using original constructor
positional args specification, then it adds synthesized members at the end if they are not already present.
    :type syntheticMemberList: list(SyntheticMember)
    :type argTuple: tuple
"""
        
        # First, the list of expected arguments is set to original constructor's arg spec. 
        expectedArgList = copy.copy(originalConstructorExpectedArgList)
        
        # ... then we append members that are not already present.
        for syntheticMember in syntheticMemberList:
            memberName = syntheticMember.memberName()
            if memberName not in expectedArgList:
                expectedArgList.append(memberName)
        
        # Makes a list of tuples (argumentName, argumentValue) with each element of each list (expectedArgList, argTuple)
        # until the shortest list's end is reached.
        positionalArgumentKeyValueList = list(zip(expectedArgList, argTuple))
        
        # Add remanining arguments (those that are not expected by the original constructor).
        for argumentValue in argTuple[len(positionalArgumentKeyValueList):]:
            positionalArgumentKeyValueList.append((None, argumentValue))

        return positionalArgumentKeyValueList

    @contract
    def _consumeArgument(self,
                         memberName,
                         positionalArgumentKeyValueList,
                         kwargs,
                         defaultValue):
        """Returns member's value from kwargs if found or from positionalArgumentKeyValueList if found
or default value otherwise.
    :type memberName: str
    :type positionalArgumentKeyValueList: list(tuple)
    :type kwargs: dict(str:*)
"""
        # Warning: we use this dict to simplify the usage of the key-value tuple list but be aware that this will
        # merge superfluous arguments as they have the same key : None.
        positionalArgumentDict = dict(positionalArgumentKeyValueList)
     
        if memberName in kwargs:
            return kwargs[memberName]

        if memberName in positionalArgumentDict:
            return positionalArgumentDict[memberName]

        return defaultValue

    @contract
    def _filterArgsAndKwargs(self,
                           originalConstructorExpectedArgList,
                           doesExpectVariadicArgs,
                           doesExpectKeywordedArgs,
                           syntheticMemberList,
                           positionalArgumentKeyValueList,
                           keywordedArgDict):
        """Returns a tuple with variadic args and keyworded args after removing arguments that have been used to
synthesize members and that are not expected by the original constructor.
If original constructor accepts variadic args, all variadic args are forwarded.
If original constructor accepts keyworded args, all keyworded args are forwarded.
    :type originalConstructorExpectedArgList: list(str)
    :type doesExpectVariadicArgs: bool
    :type doesExpectKeywordedArgs: bool
    :type syntheticMemberList: list(SyntheticMember)
    :type positionalArgumentKeyValueList: list(tuple)
    :type keywordedArgDict: dict(str:*)
"""
        
        # List is initialized with all variadic arguments.
        positionalArgumentKeyValueList = copy.copy(positionalArgumentKeyValueList)
        
        # Warning: we use this dict to simplify the usage of the key-value tuple list but be aware that this will
        # merge superfluous arguments as they have the same key : None.
        positionalArgumentDict = dict(positionalArgumentKeyValueList)
        
        # Dict is initialized with all keyworded arguments.
        keywordedArgDict = keywordedArgDict.copy()
        
        for syntheticMember in syntheticMemberList:
            argumentName = syntheticMember.memberName()
            
            # Argument is expected by the original constructor.
            if argumentName in originalConstructorExpectedArgList:
                continue

            # We filter args only if original constructor does not expected variadic args. 
            if not doesExpectVariadicArgs and argumentName in positionalArgumentDict:
                positionalArgumentKeyValueList = list(filter(lambda pair: pair[0] != argumentName,
                                                             positionalArgumentKeyValueList))

            # We filter args only if original constructor does not expected keyworded args. 
            if not doesExpectKeywordedArgs and argumentName in keywordedArgDict:
                del keywordedArgDict[argumentName]

        positionalArgumentTuple = tuple([value for _, value in positionalArgumentKeyValueList])
        return positionalArgumentTuple, keywordedArgDict
