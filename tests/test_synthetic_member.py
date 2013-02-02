#-*- coding: utf-8 -*-
#
# Created on Dec 17, 2012
#
# @author: Younes JAAIDI
#
# $Id$
#

from contracts import ContractNotRespected
from synthetic import synthesizeMember, namingConvention, NamingConventionUnderscore
import contracts
import unittest

@synthesizeMember('minimalistMember')
@synthesizeMember('memberWithDefaultValue', defaultValue = "default")
@synthesizeMember('customMember',
            getterName = 'giveMeTheCustomMember',
            setterName = 'giveThisToTheCustomMember',
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

@synthesizeMember('memberString', contract = str)
@synthesizeMember('memberStringList', contract = 'list(str)')
class TestContract:
    pass

@synthesizeMember('member_with_custom_getter_setter')
@namingConvention(NamingConventionUnderscore())
@synthesizeMember('member_with_custom_getter')
@synthesizeMember('member_with_custom_setter')
class TestCustomAccessors:
    def member_with_custom_getter_setter(self):
        return 'member_with_custom_getter_setter_value'
    
    def set_member_with_custom_getter_setter(self, value):
        self._member_with_custom_getter_setter = 'member_with_custom_getter_setter_value'

    def member_with_custom_getter(self):
        return 'member_with_custom_getter_value'
    
    def set_member_with_custom_setter(self, value):
        self._member_with_custom_setter = 'member_with_custom_setter_value'

class TestSynthesizeMember(unittest.TestCase):

    def setUp(self):
        contracts.enable_all()

    def testOK(self):
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
        instance.giveThisToTheCustomMember("newValue")
        self.assertEqual("newValue", instance._internalPrivateSecretMemberThatShouldNeverBeUsedOutsideThisClass)
        self.assertEqual("newValue", instance.giveMeTheCustomMember())
    
    def testNamingConventionUnderscore(self):
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
    
    def testReadOnly(self):
        instance = TestReadOnly()
        
        self.assertTrue(hasattr(instance, 'readOnlyMember'))
        self.assertFalse(hasattr(instance, 'setReadOnlyMember'))
    
    def testCustomAccessors(self):
        """If accessors are overriden, they should not be synthesized.
We also check that there's no bug if the naming convention is changed.
"""
        instance = TestCustomAccessors()
        self.assertEqual(None, instance._member_with_custom_getter_setter)
        self.assertEqual(None, instance._member_with_custom_getter)
        self.assertEqual(None, instance._member_with_custom_setter)

        # Testing custom setters.
        instance.set_member_with_custom_getter_setter('placeholder')
        instance.set_member_with_custom_setter('placeholder')
        instance.set_member_with_custom_getter('value')
        
        self.assertEqual('member_with_custom_getter_setter_value', instance._member_with_custom_getter_setter)
        self.assertEqual('member_with_custom_setter_value', instance._member_with_custom_setter)
        self.assertEqual('value', instance._member_with_custom_getter)
        
        # Testing custom getters.
        instance = TestCustomAccessors()
        self.assertEqual(None, instance._member_with_custom_getter_setter)
        self.assertEqual(None, instance._member_with_custom_getter)
        self.assertEqual(None, instance._member_with_custom_setter)
        
        instance._member_with_custom_setter = 'value'
        self.assertEqual('member_with_custom_getter_setter_value', instance.member_with_custom_getter_setter())
        self.assertEqual('value', instance.member_with_custom_setter())
        self.assertEqual('member_with_custom_getter_value', instance.member_with_custom_getter())

    def testContract(self):
        instance = TestContract()
        
        # OK.
        instance.setMemberString("I love CamelCase!!!")
        instance.setMemberStringList(["a", "b"])
        
        # Not OK.
        self.assertRaises(ContractNotRespected, instance.setMemberString, 10)
        self.assertRaises(ContractNotRespected, instance.setMemberStringList, ["a", 2])

        # Checking exception message.
        try:
            instance.setMemberString(10)
        except ContractNotRespected as e:
            self.assertEqual("""\
Expected type 'str', got 'int'.
checking: str   (memberString: Instance of int: 10)   for value: Instance of int: 10   """, str(e))

    def testContractDisabled(self):
        instance = TestContract()

        contracts.disable_all()

        # No exception is raised
        instance.setMemberString(10)
        instance.setMemberStringList(["a", 2])
