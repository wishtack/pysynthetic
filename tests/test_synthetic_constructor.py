#-*- coding: utf-8 -*-
#
# Created on Dec 17, 2012
#
# @author: Younes JAAIDI
#
# $Id$
#

from contracts import ContractNotRespected
from synthetic import synthesizeConstructor, synthesize_constructor, synthesizeMember, synthesizeProperty
import contracts
import unittest

@synthesizeMember('minimalistMember')
@synthesizeProperty('minimalistProperty')
@synthesizeMember('memberWithDefaultValue', default = "default")
@synthesizeProperty('propertyWithDefaultValue', default = "default")
@synthesizeConstructor()
class TestConstructor:
    pass

@synthesizeMember('minimalistMember')
@synthesizeProperty('minimalistProperty')
@synthesize_constructor()
@synthesizeMember('memberWithDefaultValue', default = "default")
@synthesizeProperty('propertyWithDefaultValue', default = "default")
class TestConstructorRandomDecoratorPosition:
    pass


@synthesizeMember('baseMember')
@synthesizeProperty('baseProperty')
@synthesizeConstructor()
class TestBase:
    pass

@synthesizeMember('intermediateMember')
@synthesizeProperty('intermediateProperty')
@synthesizeConstructor()
class TestIntermediate(TestBase):
    pass

@synthesizeMember('childMember')
@synthesizeProperty('childProperty')
@synthesizeConstructor()
class TestChild(TestIntermediate):
    pass

@synthesizeMember('memberString', contract = str)
@synthesizeMember('memberStringList', contract = 'list(str)')
@synthesizeProperty('propertyString', contract = str)
@synthesizeProperty('propertyStringList', contract = 'list(str)')
@synthesizeConstructor()
class TestContract:
    pass

@synthesizeMember('implicitMember')
@synthesizeMember('overriddenMember')
@synthesizeProperty('implicitProperty')
@synthesizeProperty('overriddenProperty')
@synthesizeConstructor()
class TestCustomConstructor:
    # It's important to test annotations, this force us to use "getfullargspec" instead of "getargspec".
    def __init__(self, overriddenMember, overriddenProperty, extraArgument, defaultValueMember = None):
        self._overriddenMemberArgument = overriddenMember
        self._overriddenPropertyArgument = overriddenProperty
        self._extraArgument = extraArgument
        self._defaultValueMemberArgument = defaultValueMember
        self._overriddenMember = "overriddenMember"
        self._overriddenProperty = "overriddenProperty"

@synthesizeMember('memberA')
@synthesizeProperty('propertyB')
@synthesizeMember('memberC')
@synthesizeProperty('propertyD')
@synthesizeConstructor()
class TestVariadicAndKewordedConstructor:
    def __init__(self, memberA, propertyB, *args, **kwargs):
        self._aArgument = memberA
        self._bArgument = propertyB
        self._args = args
        self._kwargs = kwargs

class TestSynthesizeConstructor(unittest.TestCase):

    def setUp(self):
        contracts.enable_all()

    def testOK(self):
        
        for cls in [TestConstructor, TestConstructorRandomDecoratorPosition]:
            
            instance = cls()
            self.assertEqual(None, instance.minimalistMember())
            self.assertEqual(None, instance.minimalistProperty)
            self.assertEqual("default", instance.memberWithDefaultValue())
            self.assertEqual("default", instance.propertyWithDefaultValue)
    
            instance = cls(1)
            self.assertEqual(1, instance.minimalistMember())
            self.assertEqual(None, instance.minimalistProperty)
            self.assertEqual("default", instance.memberWithDefaultValue())
            self.assertEqual("default", instance.propertyWithDefaultValue)
    
            instance = cls(1, 2)
            self.assertEqual(1, instance.minimalistMember())
            self.assertEqual(2, instance.minimalistProperty)
            self.assertEqual("default", instance.memberWithDefaultValue())
            self.assertEqual("default", instance.propertyWithDefaultValue)

            instance = cls(1, 2, 3)
            self.assertEqual(1, instance.minimalistMember())
            self.assertEqual(2, instance.minimalistProperty)
            self.assertEqual(3, instance.memberWithDefaultValue())
            self.assertEqual("default", instance.propertyWithDefaultValue)

            instance = cls(1, 2, 3, 4)
            self.assertEqual(1, instance.minimalistMember())
            self.assertEqual(2, instance.minimalistProperty)
            self.assertEqual(3, instance.memberWithDefaultValue())
            self.assertEqual(4, instance.propertyWithDefaultValue)
            
            instance = cls(1, memberWithDefaultValue = 2)
            self.assertEqual(1, instance.minimalistMember())
            self.assertEqual(None, instance.minimalistProperty)
            self.assertEqual(2, instance.memberWithDefaultValue())
            self.assertEqual("default", instance.propertyWithDefaultValue)
    
            instance = cls(propertyWithDefaultValue = 2)
            self.assertEqual(None, instance.minimalistMember())
            self.assertEqual(None, instance.minimalistProperty)
            self.assertEqual("default", instance.memberWithDefaultValue())
            self.assertEqual(2, instance.propertyWithDefaultValue)
    
    def testInheritance(self):
        instance = TestChild(1, 2, 3, 4, 5, 6)
        self.assertEqual(1, instance.childMember())
        self.assertEqual(2, instance.childProperty)
        self.assertEqual(3, instance.intermediateMember())
        self.assertEqual(4, instance.intermediateProperty)
        self.assertEqual(5, instance.baseMember())
        self.assertEqual(6, instance.baseProperty)
        
        instance = TestChild(childMember = 1,
                             childProperty = 2,
                             intermediateMember = 3,
                             intermediateProperty = 4,
                             baseMember = 5,
                             baseProperty = 6)
        self.assertEqual(1, instance.childMember())
        self.assertEqual(2, instance.childProperty)
        self.assertEqual(3, instance.intermediateMember())
        self.assertEqual(4, instance.intermediateProperty)
        self.assertEqual(5, instance.baseMember())
        self.assertEqual(6, instance.baseProperty)

        instance = TestChild(baseMember = 1, baseProperty = 2)
        self.assertEqual(None, instance.childMember())
        self.assertEqual(None, instance.childProperty)
        self.assertEqual(None, instance.intermediateMember())
        self.assertEqual(None, instance.intermediateProperty)
        self.assertEqual(1, instance.baseMember())
        self.assertEqual(2, instance.baseProperty)

    def testCustomConstructor(self):
        # TestCustomConstructor __init__ method takes 4 parameters
        # (overriddenMember, overriddenProperty and extraArgument) + self.
        self.assertRaises(TypeError, TestCustomConstructor)
        self.assertRaises(TypeError, TestCustomConstructor, "member")
        self.assertRaises(TypeError, TestCustomConstructor, "member", "property")
        
        # Two mandatory arguments.
        for instance in [TestCustomConstructor("overriddenMemberArgument", "overriddenPropertyArgument", "extra"),
                         TestCustomConstructor("overriddenMemberArgument", "overriddenPropertyArgument", extraArgument = "extra"),
                         TestCustomConstructor(overriddenMember = "overriddenMemberArgument",
                                               overriddenProperty = "overriddenPropertyArgument",
                                               extraArgument = "extra")]:
            
            self.assertEqual(None, instance.implicitMember())
            self.assertEqual("overriddenMember", instance.overriddenMember())
            self.assertEqual("overriddenProperty", instance.overriddenProperty)
            self.assertEqual("overriddenMemberArgument", instance._overriddenMemberArgument)
            self.assertEqual("overriddenPropertyArgument", instance._overriddenPropertyArgument)
            self.assertEqual("extra", instance._extraArgument)

        # Three mandatory arguments + defaultValueMember
        for instance in [TestCustomConstructor("overriddenMemberArgument",
                                               "overriddenPropertyArgument",
                                               "extra",
                                               "valueForDefaultValueMember"),
                         TestCustomConstructor("overriddenMemberArgument",
                                               "overriddenPropertyArgument",
                                               "extra",
                                               defaultValueMember = "valueForDefaultValueMember"),
                         TestCustomConstructor("overriddenMemberArgument",
                                               "overriddenPropertyArgument",
                                               extraArgument = "extra",
                                               defaultValueMember = "valueForDefaultValueMember"),
                         TestCustomConstructor(overriddenMember = "overriddenMemberArgument",
                                               overriddenProperty = "overriddenPropertyArgument",
                                               extraArgument = "extra",
                                               defaultValueMember = "valueForDefaultValueMember")]:
            self.assertEqual(None, instance.implicitMember())
            self.assertEqual("overriddenMember", instance.overriddenMember())
            self.assertEqual("overriddenProperty", instance.overriddenProperty)
            self.assertEqual("overriddenMemberArgument", instance._overriddenMemberArgument)
            self.assertEqual("overriddenPropertyArgument", instance._overriddenPropertyArgument)
            self.assertEqual("extra", instance._extraArgument)
            self.assertEqual("valueForDefaultValueMember", instance._defaultValueMemberArgument)

        # Three mandatory arguments + defaultValueMember + implicitMember.
        for instance in [TestCustomConstructor("overriddenMemberArgument",
                                               "overriddenPropertyArgument",
                                               "extra",
                                               "valueForDefaultValueMember",
                                               "implicitMember",
                                               "implicitProperty"),
                         TestCustomConstructor("overriddenMemberArgument",
                                               "overriddenPropertyArgument",
                                               "extra",
                                               "valueForDefaultValueMember",
                                               implicitMember = "implicitMember",
                                               implicitProperty = "implicitProperty"),
                         TestCustomConstructor("overriddenMemberArgument",
                                               "overriddenPropertyArgument",
                                               "extra",
                                               defaultValueMember = "valueForDefaultValueMember",
                                               implicitMember = "implicitMember",
                                               implicitProperty = "implicitProperty"),
                         TestCustomConstructor("overriddenMemberArgument",
                                               "overriddenPropertyArgument",
                                               extraArgument = "extra",
                                               defaultValueMember = "valueForDefaultValueMember",
                                               implicitMember = "implicitMember",
                                               implicitProperty = "implicitProperty"),
                         TestCustomConstructor(overriddenMember = "overriddenMemberArgument",
                                               overriddenProperty = "overriddenPropertyArgument",
                                               extraArgument = "extra",
                                               defaultValueMember = "valueForDefaultValueMember",
                                               implicitMember = "implicitMember",
                                               implicitProperty = "implicitProperty")]:
            self.assertEqual("implicitMember", instance.implicitMember())
            self.assertEqual("implicitProperty", instance.implicitProperty)
            self.assertEqual("overriddenMember", instance.overriddenMember())
            self.assertEqual("overriddenProperty", instance.overriddenProperty)
            self.assertEqual("overriddenMemberArgument", instance._overriddenMemberArgument)
            self.assertEqual("overriddenPropertyArgument", instance._overriddenPropertyArgument)
            self.assertEqual("extra", instance._extraArgument)
            self.assertEqual("valueForDefaultValueMember", instance._defaultValueMemberArgument)

        # Three mandatory arguments + defaultValueMember + implicitMember + implicitProperty + superfluous argument.
        self.assertRaises(TypeError,
                          TestCustomConstructor,
                          "overriddenMemberArgument",
                          "overriddenPropertyArgument",
                          "extra",
                          "valueForDefaultValueMember",
                          "implicitMember",
                          "implicitProperty",
                          "superfluous")
        self.assertRaises(TypeError,
                          TestCustomConstructor,
                          "overriddenMemberArgument",
                          "overriddenPropertyArgument",
                          "extra",
                          "valueForDefaultValueMember",
                          "implicitMember",
                          "implicitProperty",
                          superfluousMember = "superfluous")
        self.assertRaises(TypeError,
                          TestCustomConstructor,
                          "overriddenMemberArgument",
                          "overriddenPropertyArgument",
                          "extra",
                          "valueForDefaultValueMember",
                          implicitMember = "implicitMember",
                          implicitProperty = "implicitProperty",
                          superfluousMember = "superfluous")
        self.assertRaises(TypeError,
                          TestCustomConstructor,
                          "overriddenMemberArgument",
                          "overriddenPropertyArgument",
                          "extra",
                          "valueForDefaultValueMember",
                          implicitMember = "implicitMember",
                          implicitProperty = "implicitProperty",
                          superfluousMember = "superfluous")
        self.assertRaises(TypeError,
                          TestCustomConstructor,
                          "overriddenMemberArgument",
                          "overriddenPropertyArgument",
                          "extra",
                          defaultValueMember = "valueForDefaultValueMember",
                          implicitMember = "implicitMember",
                          implicitProperty = "implicitProperty",
                          superfluousMember = "superfluous")
        self.assertRaises(TypeError,
                          TestCustomConstructor,
                          "overriddenMemberArgument",
                          "overriddenPropertyArgument",
                          extraArgument = "extra",
                          defaultValueMember = "valueForDefaultValueMember",
                          implicitMember = "implicitMember",
                          implicitProperty = "implicitProperty",
                          superfluousMember = "superfluous")
        self.assertRaises(TypeError,
                          TestCustomConstructor,
                          overriddenMember = "overriddenMemberArgument",
                          overriddenProperty = "overriddenPropertyArgument",
                          extraArgument = "extra",
                          defaultValueMember = "valueForDefaultValueMember",
                          implicitMember = "implicitMember",
                          implicitProperty = "implicitProperty",
                          superfluousMember = "superfluous")
                
        # Using superfluous member while implicit member is not set.
        self.assertRaises(TypeError,
                          TestCustomConstructor,
                          "overriddenMemberArgument",
                          "overriddenPropertyArgument",
                          "extra",
                          "valueForDefaultValueMember",
                          superfluousMember = "superfluous")
        # Using superfluous member while implicit member and member with default value are not set.
        self.assertRaises(TypeError,
                          TestCustomConstructor,
                          "overriddenMemberArgument",
                          "overriddenPropertyArgument",
                          "extra",
                          superfluousMember = "superfluous")

    def testVariadicAndKeywordedArguments(self):
        instance = TestVariadicAndKewordedConstructor(1, 2, 3, 4, 5, memberC = 10, propertyD = 11, e = 12)
        self.assertEqual(1, instance._aArgument)
        self.assertEqual(2, instance._bArgument)
        self.assertEqual((3, 4, 5), instance._args)
        self.assertEqual({"memberC": 10, "propertyD": 11, "e": 12}, instance._kwargs)
        self.assertEqual(1, instance.memberA())
        self.assertEqual(2, instance.propertyB)
        self.assertEqual(10, instance.memberC())
        self.assertEqual(11, instance.propertyD)

    def testContract(self):
        # OK.
        validKwargs = {'memberString': "Be free! Kill bureaucracy!!!",
                       'propertyString': "Be free! Kill bureaucracy!!!",
                       'memberStringList': ["a", "b"],
                       'propertyStringList': ["a", "b"]}
        TestContract(**validKwargs)

        # memberString, propertyString, memberStringList and propertyStringList can't be None.
        self.assertRaises(ContractNotRespected, TestContract)
        
        # Invalid memberString.
        kwargs = validKwargs.copy()
        kwargs['memberString'] = 1234
        self.assertRaises(ContractNotRespected, TestContract, **kwargs)

        # Invalid propertyString.
        kwargs = validKwargs.copy()
        kwargs['propertyString'] = 1234
        self.assertRaises(ContractNotRespected, TestContract, **kwargs)

        # Invalid memberStringList.
        kwargs = validKwargs.copy()
        kwargs['memberStringList'] = ["a", 2]
        self.assertRaises(ContractNotRespected, TestContract, **kwargs)

        # Invalid propertyStringList.
        kwargs = validKwargs.copy()
        kwargs['propertyStringList'] = ["a", 2]
        self.assertRaises(ContractNotRespected, TestContract, **kwargs)

        # Checking exception message.
        try:
            TestContract()
        except ContractNotRespected as e:
            self.assertEqual("""\
Expected type 'str', got 'NoneType'.
checking: str   for value: Instance of NoneType: None   
Variables bound in inner context:
- memberString: Instance of NoneType: None""", str(e))

    def testContractDisabled(self):
        validKwargs = {'memberString': "Be free! Kill bureaucracy!!!",
                       'propertyString': "Be free! Kill bureaucracy!!!",
                       'memberStringList': ["a", "b"],
                       'propertyStringList': ["a", "b"]}
        
        # Disabling contracts.
        contracts.disable_all()
        
        # No exception is raised.
        TestContract()

        # Invalid memberString but no exception is raised.
        kwargs = validKwargs.copy()
        kwargs['memberString'] = 1234
        TestContract(**kwargs)

        # Invalid propertyString but no exception is raised.
        kwargs = validKwargs.copy()
        kwargs['propertyString'] = 1234
        TestContract(**kwargs)

        # Invalid memberStringList but no exception is raised.
        kwargs = validKwargs.copy()
        kwargs['memberStringList'] = ["a", 2]
        TestContract(**kwargs)

        # Invalid propertyStringList but no exception is raised.
        kwargs = validKwargs.copy()
        kwargs['propertyStringList'] = ["a", 2]
        TestContract(**kwargs)
