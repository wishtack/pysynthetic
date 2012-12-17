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
class Base:
    pass

@synthesizeMember('intermediateMember')
@synthesizeConstructor()
class Intermediate(Base):
    pass

@synthesizeMember('childMember')
@synthesizeConstructor()
class Child(Intermediate):
    pass


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
        instance = Child(1, 2, 3)
        self.assertEqual(1, instance.childMember())
        self.assertEqual(2, instance.intermediateMember())
        self.assertEqual(3, instance.baseMember())
        
        instance = Child(childMember = 1, intermediateMember = 2, baseMember = 3)
        self.assertEqual(1, instance.childMember())
        self.assertEqual(2, instance.intermediateMember())
        self.assertEqual(3, instance.baseMember())

        instance = Child(baseMember = 3)
        self.assertEqual(3, instance.baseMember())
