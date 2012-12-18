#-*- coding: utf-8 -*-
#
# Created on Dec 17, 2012
#
# @author: Younes JAAIDI
#
# $Id: $
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

@synthesizeMember('minimalistMember')
@synthesizeMember('overridenMember')
@synthesizeConstructor()
class TestCustomConstructor:
    def __init__(self, overridenMember, extraMember):
        self._overridenMemberArgument = overridenMember
        self._extraMemberArgument = extraMember
        self._overridenMember = "overriden"

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
        self.assertRaises(TypeError, TestCustomConstructor, "minimalist", "overriden")
        
        for instance in [TestCustomConstructor("minimalist", "original", "extra"),
                         TestCustomConstructor("minimalist", "original", extraMember = "extra"),
                         TestCustomConstructor("minimalist", overridenMember = "original", extraMember = "extra"),
                         TestCustomConstructor(minimalistMember = "minimalist", overridenMember = "original", extraMember = "extra")]:
            self.assertEqual("minimalist", instance.minimalistMember())
            self.assertEqual("overriden", instance.overridenMember())
            self.assertEqual("original", instance._overridenMemberArgument)
            self.assertEqual("extra", instance._extraMemberArgument)
