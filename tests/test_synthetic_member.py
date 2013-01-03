#-*- coding: utf-8 -*-
#
# Created on Dec 17, 2012
#
# @author: Younes JAAIDI
#
# $Id$
#

import unittest

from synthetic import synthesizeMember, namingConvention, NamingConventionUnderscore

@synthesizeMember('minimalistMember')
@synthesizeMember('memberWithDefaultValue', defaultValue = "default")
@synthesizeMember('customMember',
            getterName = 'giveMeTheCustomMember',
            setterName = 'giveThisToTheCustumMember',
            privateMemberName = '_internalPrivateSecretMemberThatShouldNeverBeUsedOutsideThisClass')
class TestBasic:
    pass

@synthesizeMember('first_member')
@namingConvention(NamingConventionUnderscore())
@synthesizeMember('second_member')
@synthesizeMember('third_member', getterName = 'third_member_custom_getter')
@synthesizeMember('fourth_member', setterName = 'fourth_member_custom_setter')
class TestUnderscore:
    pass

@synthesizeMember('readOnlyMember', readOnly = True)
class TestReadOnly:
    pass

class TestSynthesizeMember(unittest.TestCase):

    def testSynthesizeMember(self):
        instance = TestBasic()
        
        # Default default ;) member value is None.
        self.assertEqual(None, instance.minimalistMember())
        
        # Default set and get test. 
        instance.setMinimalistMember(10)
        self.assertEqual(10, instance.minimalistMember())
        
        # Checking custom default value.
        self.assertEqual("default", instance.memberWithDefaultValue())
        
        # With custom accessor names and constructor value, default names don't work...
        self.assertFalse(hasattr(instance, 'customMember'))
        self.assertFalse(hasattr(instance, 'setCustomMember'))
        self.assertFalse(hasattr(instance, '_customMember'))

        # ... but custom names work.
        instance.giveThisToTheCustumMember("newValue")
        self.assertEqual("newValue", instance._internalPrivateSecretMemberThatShouldNeverBeUsedOutsideThisClass)
        self.assertEqual("newValue", instance.giveMeTheCustomMember())
    
    def testSynthesizeWithNamingConventionUnderscore(self):
        instance = TestUnderscore()
        
        # Default default ;) member value is None.
        self.assertEqual(None, instance.first_member())
        self.assertEqual(None, instance.second_member())
        self.assertEqual(None, instance.third_member_custom_getter())
        self.assertEqual(None, instance.fourth_member())
        
        # Default set and get test. 
        instance.set_first_member(10)
        instance.set_second_member(20)
        instance.set_third_member(30)
        instance.fourth_member_custom_setter(40)
        self.assertEqual(10, instance.first_member())
        self.assertEqual(20, instance.second_member())
        self.assertEqual(30, instance.third_member_custom_getter())
        self.assertEqual(40, instance.fourth_member())
        
        # Checking that the default naming convention "CamelCase" was not used.
        self.assertFalse(hasattr(instance, 'setFirst_member'))
        self.assertFalse(hasattr(instance, 'setSecond_member'))
        self.assertFalse(hasattr(instance, 'setThird_member'))
        self.assertFalse(hasattr(instance, 'setFourth_member'))
        self.assertFalse(hasattr(instance, 'third_member'))
        self.assertFalse(hasattr(instance, 'set_fourth_member'))
        
    def testContract(self):
        pass
    
    def testReadOnly(self):
        instance = TestReadOnly()
        
        self.assertTrue(hasattr(instance, 'readOnlyMember'))
        self.assertFalse(hasattr(instance, 'setReadOnlyMember'))

if __name__ == "__main__":
    unittest.main()
