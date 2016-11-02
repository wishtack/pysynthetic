# -*- coding: utf-8 -*-
#
# Created on Oct 30, 2016
import inspect

from contracts import new_contract, contract

from .synthetic_member import SyntheticMember

new_contract('SyntheticMember', SyntheticMember)


class SyntheticComparisonFactory(object):

    @contract
    def makeEqualFunction(self, originalEqualFunction, syntheticMemberList):
        """
        :param list(SyntheticMember) syntheticMemberList: a list of the class' synthetic members.
        """
        def equal(instance, other):
            if instance.__class__ is not other.__class__:
                return NotImplemented

            for m in syntheticMemberList:
                if getattr(instance, m.privateMemberName()) != getattr(other, m.privateMemberName()):
                    return False

            if inspect.isfunction(originalEqualFunction) or inspect.ismethod(originalEqualFunction):
                return originalEqualFunction(instance, other)

            return True

        return equal

    @contract
    def makeNotEqualFunction(self, originalNotEqualFunction, syntheticMemberList):
        """
        :param list(SyntheticMember) syntheticMemberList: a list of the class' synthetic members.
        """

        def not_equal(instance, other):
            if instance.__class__ is not other.__class__:
                return NotImplemented

            for m in syntheticMemberList:
                if getattr(instance, m.privateMemberName()) != getattr(other, m.privateMemberName()):
                    return True

            if inspect.isfunction(originalNotEqualFunction) or inspect.ismethod(originalNotEqualFunction):
                return originalNotEqualFunction(instance, other)

            return False

        return not_equal

    @contract
    def makeHashFunction(self, originalHashFunction, syntheticMemberList):
        """
        :param list(SyntheticMember) syntheticMemberList: a list of the class' synthetic members.
        """
        if originalHashFunction is None:
            return None

        for member in syntheticMemberList:
            if not member.readOnly():
                return None

        # All synthetic members are read-only: generate a hash function.
        def hash_function(instance):
            values = [getattr(instance, m.privateMemberName()) for m in syntheticMemberList]
            if inspect.isfunction(originalHashFunction) or inspect.ismethod(originalHashFunction):
                values.append(originalHashFunction(instance))
            return hash(tuple(values))

        return hash_function
