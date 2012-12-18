#-*- coding: utf-8 -*-
#
# Created on Dec 17, 2012
#
# @author: Younes JAAIDI
#
# $Id: $
#

import unittest

from synthetic import synthesizeMember, NamingConventionUnderscore

@synthesizeMember('minimalistMember')
@synthesizeMember('memberWithDefaultValue', defaultValue = "default")
@synthesizeMember('customMember',
            getterName = 'giveMeTheCustomMember',
            setterName = 'giveThisToTheCustumMember',
            privateMemberName = '_internalPrivateSecretMemberThatShouldNeverBeUsedOutsideThisClass')
class TestBasic:
    pass

@synthesizeMember('member', namingConvention = NamingConventionUnderscore())
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
        self.assertEqual(None, instance.member())
        
        # Default set and get test. 
        instance.set_member(10)
        self.assertEqual(10, instance.member())
        
    def testContract(self):
        pass
    
    def testReadOnly(self):
        instance = TestReadOnly()
        
        self.assertTrue(hasattr(instance, 'readOnlyMember'))
        self.assertFalse(hasattr(instance, 'setReadOnlyMember'))

if __name__ == "__main__":
    unittest.main()
