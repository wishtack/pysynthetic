#-*- coding: utf-8 -*-
#
# Created on Oct 30, 2016
#
from synthetic import synthesizeConstructor, synthesizeEquality, synthesize_equality, synthesizeMember, synthesizeProperty
import collections
import unittest


@synthesizeMember('minimalistMember')
@synthesizeProperty('minimalistProperty')
@synthesizeEquality()
class TestEquality(object):
    pass


@synthesizeMember('minimalistMember')
@synthesize_equality()
@synthesizeProperty('minimalistProperty')
class TestEqualityRandomDecoratorPosition(object):
    pass


@synthesizeMember('readonlyMember', readOnly=True)
@synthesizeProperty('readonlyProperty', readOnly=True)
@synthesizeEquality()
@synthesizeConstructor()
class TestImmutable(object):
    pass


@synthesizeMember('minimalistMember')
@synthesizeProperty('minimalistProperty')
@synthesizeMember('readonlyMember', readOnly=True)
@synthesizeProperty('readonlyProperty', readOnly=True)
@synthesizeEquality()
@synthesizeConstructor()
class TestPartiallyMutable(object):
    pass


@synthesizeMember('baseMember')
@synthesizeProperty('baseProperty')
@synthesizeEquality()
class TestBase(object):
    pass


@synthesizeMember('intermediateMember')
@synthesizeProperty('intermediateProperty')
@synthesizeEquality()
class TestIntermediate(TestBase):
    pass


@synthesizeMember('childMember', contract=int)
@synthesizeProperty('childProperty')
@synthesizeEquality()
class TestChild(TestIntermediate):
    pass


@synthesizeMember('readonlyMember', readOnly=True)
@synthesizeProperty('readonlyProperty', readOnly=True)
@synthesizeEquality()
@synthesizeConstructor()
class TestChildWithReadOnlyMembers(TestIntermediate):
    pass


@synthesizeMember('baseMember', readOnly=True)
@synthesizeMember('baseProperty', readOnly=True)
@synthesizeConstructor()
@synthesizeEquality()
class TestImmutableBase(object):
    pass


@synthesizeMember('childMember', readOnly=True)
@synthesizeProperty('childProperty', readOnly=True)
@synthesizeConstructor()
@synthesizeEquality()
class TestImmutableChild(TestImmutableBase):
    pass


class TestSynthesizeEquality(unittest.TestCase):
    def assertCompareEqual(self, first, second):
        self.assertEqual(True, first == second)
        self.assertEqual(False, first != second)

    def assertCompareNotEqual(self, first, second):
        self.assertEqual(False, first == second)
        self.assertEqual(True, first != second)

    def testMutableTypes(self):
        for cls in [TestEquality, TestEqualityRandomDecoratorPosition]:
            first = cls()
            second = cls()

            # Initial states are equal
            self.assertCompareEqual(first, second)

            # When setting both data members to the same values, return True
            first.setMinimalistMember(1)
            second.setMinimalistMember(1)
            first.minimalistProperty = 2
            second.minimalistProperty = 2

            self.assertCompareEqual(first, second)

            # Test on member not being equal
            first.setMinimalistMember(2)
            self.assertCompareNotEqual(first, second)

            # Revert to equality
            first.setMinimalistMember(second.minimalistMember())
            self.assertCompareEqual(first, second)

            # Test on property not being equal
            first.minimalistProperty = 1
            self.assertCompareNotEqual(first, second)

            # Test that these instances of mutable types are not hashable
            self.assertNotIsInstance(first, collections.Hashable)
            self.assertRaises(TypeError, lambda: hash(first))

    def testReturnNotEqualOnDifferingTypes(self):
        first = TestEquality()
        second = TestEqualityRandomDecoratorPosition()

        first.setMinimalistMember(1)
        second.setMinimalistMember(1)
        first.minimalistProperty = 2
        second.minimalistProperty = 2

        self.assertCompareNotEqual(first, second)

    def testImmutableType(self):
        first = TestImmutable(readonlyMember=1, readonlyProperty=2)
        second = TestImmutable(readonlyMember=1, readonlyProperty=2)

        self.assertCompareEqual(first, second)
        self.assertIsInstance(first, collections.Hashable)
        self.assertEqual(hash(first), hash(second))

    def testHashFunctionNotTrivial(self):
        """Ensure that member hashes are not combined with a simple XOR"""
        first = TestImmutable(readonlyMember=1, readonlyProperty=1)
        second = TestImmutable(readonlyMember=2, readonlyProperty=2)

        self.assertCompareNotEqual(first, second)
        self.assertIsInstance(first, collections.Hashable)
        self.assertNotEqual(hash(first), hash(second))

    def testInheritance(self):
        first = TestChild()
        second = TestChild()

        self.assertEqual(True, first == second)

        self._resetChildInstance(first)
        self._resetChildInstance(second)

        self.assertCompareEqual(first, second)

        first.setBaseMember(2)
        self.assertCompareNotEqual(first, second)
        self._resetChildInstance(first)

        first.baseProperty = 1
        self.assertCompareNotEqual(first, second)
        self._resetChildInstance(first)

        first.setIntermediateMember(4)
        self.assertCompareNotEqual(first, second)
        self._resetChildInstance(first)

        first.intermediateProperty = 3
        self.assertCompareNotEqual(first, second)
        self._resetChildInstance(first)

        first.setChildMember(6)
        self.assertCompareNotEqual(first, second)
        self._resetChildInstance(first)

        first.childProperty = 5
        self.assertCompareNotEqual(first, second)
        self._resetChildInstance(first)

    def testInheritanceOfMutableClassByImmutableClassIsNotHashable(self):
        first = TestChildWithReadOnlyMembers(readonlyMember=1, readonlyProperty=2)
        self.assertNotIsInstance(first, collections.Hashable)

    def testInheritanceImmutable(self):
        first = TestImmutableChild(baseMember=1, baseProperty=2, childMember=3, childProperty=4)
        second = TestImmutableChild(baseMember=1, baseProperty=2, childMember=3, childProperty=4)

        self.assertCompareEqual(first, second)
        self.assertIsInstance(first, collections.Hashable)
        self.assertEqual(hash(first), hash(second))

    def testBaseClassHashIsTakenInAccountInChildHash(self):
        first = TestImmutableChild(baseMember=4, baseProperty=3, childMember=3, childProperty=4)
        second = TestImmutableChild(baseMember=1, baseProperty=2, childMember=3, childProperty=4)

        self.assertCompareNotEqual(first, second)
        self.assertIsInstance(first, collections.Hashable)
        self.assertNotEqual(hash(first), hash(second))

    @staticmethod
    def _resetChildInstance(instance):
        instance.setBaseMember(1)
        instance.baseProperty = 2
        instance.setIntermediateMember(3)
        instance.intermediateProperty = 4
        instance.setChildMember(5)
        instance.childProperty = 6
