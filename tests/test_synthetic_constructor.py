#-*- coding: utf-8 -*-
#
# Created on Dec 17, 2012
#
# @author: Younes JAAIDI
#
# $Id$
#

import unittest

from synthetic import synthesizeMember, synthesizeConstructor

@synthesizeMember('minimalistMember')
@synthesizeMember('memberWithDefaultValue', defaultValue = "default")
@synthesizeConstructor()
class TestConstructor:
    pass

@synthesizeMember('minimalistMember')
@synthesizeConstructor()
@synthesizeMember('memberWithDefaultValue', defaultValue = "default")
class TestConstructorRandomDecoratorPosition:
    pass


@synthesizeMember('baseMember')
@synthesizeConstructor()
class TestBase:
    pass

@synthesizeMember('intermediateMember')
@synthesizeConstructor()
class TestIntermediate(TestBase):
    pass

@synthesizeMember('childMember')
@synthesizeConstructor()
class TestChild(TestIntermediate):
    pass

@synthesizeMember('implicitMember')
@synthesizeMember('overridenMember')
@synthesizeConstructor()
class TestCustomConstructor:
    # It's important to test annotations, this force us to use "getfullargspec" instead of "getargspec".
    def __init__(self, overridenMember, extraMember, defaultValueMember = None):
        self._overridenMemberArgument = overridenMember
        self._extraMemberArgument = extraMember
        self._defaultValueMemberArgument = defaultValueMember
        self._overridenMember = "overriden"

@synthesizeMember('a')
@synthesizeMember('b')
@synthesizeMember('c')
@synthesizeConstructor()
class TestVariadicAndKewordedConstructor:
    def __init__(self, a, *args, **kwargs):
        self._aArgument = a
        self._args = args
        self._kwargs = kwargs

class TestSynthesizeConstructor(unittest.TestCase):

    def testSynthesizeConstructor(self):
        
        for cls in [TestConstructor, TestConstructorRandomDecoratorPosition]:
            
            instance = cls()
            self.assertEqual(None, instance.minimalistMember())
            self.assertEqual("default", instance.memberWithDefaultValue())
    
            instance = cls(1)
            self.assertEqual(1, instance.minimalistMember())
            self.assertEqual("default", instance.memberWithDefaultValue())
    
            instance = cls(1, 2)
            self.assertEqual(1, instance.minimalistMember())
            self.assertEqual(2, instance.memberWithDefaultValue())
            
            instance = cls(1, memberWithDefaultValue = 2)
            self.assertEqual(1, instance.minimalistMember())
            self.assertEqual(2, instance.memberWithDefaultValue())
    
            instance = cls(memberWithDefaultValue = 2)
            self.assertEqual(None, instance.minimalistMember())
            self.assertEqual(2, instance.memberWithDefaultValue())
    
    def testSynthesizeConstructorWithInheritance(self):
        instance = TestChild(1, 2, 3)
        self.assertEqual(1, instance.childMember())
        self.assertEqual(2, instance.intermediateMember())
        self.assertEqual(3, instance.baseMember())
        
        instance = TestChild(childMember = 1, intermediateMember = 2, baseMember = 3)
        self.assertEqual(1, instance.childMember())
        self.assertEqual(2, instance.intermediateMember())
        self.assertEqual(3, instance.baseMember())

        instance = TestChild(baseMember = 3)
        self.assertEqual(None, instance.childMember())
        self.assertEqual(None, instance.intermediateMember())
        self.assertEqual(3, instance.baseMember())

    def testSynthesizeConstructorWithCustomConstructor(self):
        # TestCustomConstructor __init__ method takes 3 parameters (minimalistMember, overridenMember and extraMember) + self.
        self.assertRaises(TypeError, TestCustomConstructor)
        self.assertRaises(TypeError, TestCustomConstructor, "minimalist")
        
        # Two mandatory arguments.
        for instance in [TestCustomConstructor("original", "extra"),
                         TestCustomConstructor("original", extraMember = "extra"),
                         TestCustomConstructor(overridenMember = "original", extraMember = "extra")]:
            self.assertEqual(None, instance.implicitMember())
            self.assertEqual("overriden", instance.overridenMember())
            self.assertEqual("original", instance._overridenMemberArgument)
            self.assertEqual("extra", instance._extraMemberArgument)

        # Two mandatory arguments + defaultValueMember
        for instance in [TestCustomConstructor("original",
                                               "extra",
                                               "valueForDefaultValueMember"),
                         TestCustomConstructor("original",
                                               "extra",
                                               defaultValueMember = "valueForDefaultValueMember"),
                         TestCustomConstructor("original",
                                               extraMember = "extra",
                                               defaultValueMember = "valueForDefaultValueMember"),
                         TestCustomConstructor(overridenMember = "original",
                                               extraMember = "extra",
                                               defaultValueMember = "valueForDefaultValueMember")]:
            self.assertEqual(None, instance.implicitMember())
            self.assertEqual("overriden", instance.overridenMember())
            self.assertEqual("original", instance._overridenMemberArgument)
            self.assertEqual("extra", instance._extraMemberArgument)
            self.assertEqual("valueForDefaultValueMember", instance._defaultValueMemberArgument)

        # Two mandatory arguments + defaultValueMember + implicitMember.
        for instance in [TestCustomConstructor("original",
                                               "extra",
                                               "valueForDefaultValueMember",
                                               "implicit"),
                         TestCustomConstructor("original",
                                               "extra",
                                               "valueForDefaultValueMember",
                                               implicitMember = "implicit"),
                         TestCustomConstructor("original",
                                               "extra",
                                               defaultValueMember = "valueForDefaultValueMember",
                                               implicitMember = "implicit"),
                         TestCustomConstructor("original",
                                               extraMember = "extra",
                                               defaultValueMember = "valueForDefaultValueMember",
                                               implicitMember = "implicit"),
                         TestCustomConstructor(overridenMember = "original",
                                               extraMember = "extra",
                                               defaultValueMember = "valueForDefaultValueMember",
                                               implicitMember = "implicit")]:
            self.assertEqual("implicit", instance.implicitMember())
            self.assertEqual("overriden", instance.overridenMember())
            self.assertEqual("original", instance._overridenMemberArgument)
            self.assertEqual("extra", instance._extraMemberArgument)
            self.assertEqual("valueForDefaultValueMember", instance._defaultValueMemberArgument)

        # Two mandatory arguments + defaultValueMember + implicitMember + superfluous argument.
        self.assertRaises(TypeError,
                          TestCustomConstructor,
                          "original",
                          "extra",
                          "valueForDefaultValueMember",
                          "implicit",
                          "superfluous")
        self.assertRaises(TypeError,
                          TestCustomConstructor,
                          "original",
                          "extra",
                          "valueForDefaultValueMember",
                          "implicit",
                          superfluousMember = "superfluous")
        self.assertRaises(TypeError,
                          TestCustomConstructor,
                          "original",
                          "extra",
                          "valueForDefaultValueMember",
                          implicitMember = "implicit",
                          superfluousMember = "superfluous")
        self.assertRaises(TypeError,
                          TestCustomConstructor,
                          "original",
                          "extra",
                          "valueForDefaultValueMember",
                          implicitMember = "implicit",
                          superfluousMember = "superfluous")
        self.assertRaises(TypeError,
                          TestCustomConstructor,
                          "original",
                          "extra",
                          defaultValueMember = "valueForDefaultValueMember",
                          implicitMember = "implicit",
                          superfluousMember = "superfluous")
        self.assertRaises(TypeError,
                          TestCustomConstructor,
                          "original",
                          extraMember = "extra",
                          defaultValueMember = "valueForDefaultValueMember",
                          implicitMember = "implicit",
                          superfluousMember = "superfluous")
        self.assertRaises(TypeError,
                          TestCustomConstructor,
                          overridenMember = "original",
                          extraMember = "extra",
                          defaultValueMember = "valueForDefaultValueMember",
                          implicitMember = "implicit",
                          superfluousMember = "superfluous")
                
        # Using superfluous member while implicit member is not set.
        self.assertRaises(TypeError,
                          TestCustomConstructor,
                          "original",
                          "extra",
                          "valueForDefaultValueMember",
                          superfluousMember = "superfluous")
        # Using superfluous member while implicit member and member with default value are not set.
        self.assertRaises(TypeError,
                          TestCustomConstructor,
                          "original",
                          "extra",
                          superfluousMember = "superfluous")

    def testSynthesizeConstructorWithVariadicAndKeywordedArguments(self):
        instance = TestVariadicAndKewordedConstructor(1, 2, 3, 4, 5, c = 10, d = 11, e = 12)
        self.assertEqual(1, instance._aArgument)
        self.assertEqual((2, 3, 4, 5), instance._args)
        self.assertEqual({"c": 10, "d": 11, "e": 12}, instance._kwargs)
        self.assertEqual(1, instance.a())
        self.assertEqual(2, instance.b())
        self.assertEqual(10, instance.c())
