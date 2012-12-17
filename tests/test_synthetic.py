
from synthetic import synthesizeMember, AccessorNameMakerUnderscore
import unittest

@synthesizeMember('minimalistMember')
@synthesizeMember('memberWithDefaultValue', defaultValue = "default")
@synthesizeMember('customMember',
            getterName = 'giveMeTheCustomMember',
            setterName = 'giveThisToTheCustumMember',
            privateMemberName = '_internalPrivateSecretMemberThatShouldNeverBeUsedOutsideThisClass')
class TestBasic:
    pass

@synthesizeMember('member', accessorNameMaker = AccessorNameMakerUnderscore())
class TestUnderscore:
    pass

@synthesizeMember('readOnlyMember', readOnly = True)
class TestReadOnly:
    pass

class TestSynthesizer(unittest.TestCase):

    def testSynthesize(self):
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
    
    def testSynthesizeWithAccessorNameMakerUnderscore(self):
        pass
    
    def testContract(self):
        pass
    
    def testReadOnly(self):
        instance = TestReadOnly()
        
        self.assertTrue(hasattr(instance, 'readOnlyMember'))
        self.assertFalse(hasattr(instance, 'setReadOnlyMember'))

if __name__ == "__main__":
    unittest.main()
