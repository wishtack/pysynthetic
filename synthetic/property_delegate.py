#-*- coding: utf-8 -*-
#
# Created on Feb 28, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from .exceptions import SyntheticError
from .i_member_delegate import IMemberDelegate
from contracts import contract, new_contract

new_contract('IMemberFactory', IMemberDelegate)

class InvalidPropertyOverrideError(SyntheticError):

    @contract
    def __init__(self, memberName, className):
        """
    :type memberName: str
    :type className: str
"""
        super(InvalidPropertyOverrideError, self).__init__("Member '%s' for class '%s' must be overridden with a property." \
                                                           % (memberName, className))

class PropertyDelegate(IMemberDelegate):

    _KEY_PROPERTY_GET = 'fget'
    _KEY_PROPERTY_SET = 'fset'
    _KEY_PROPERTY_DEL = 'fdel'
    _KEY_PROPERTY_DOC = 'doc'

    def apply(self, cls, originalMemberNameList, memberName, classNamingConvention, getter, setter):
        """
    :type cls: type
    :type originalMemberNameList: list(str)
    :type memberName: str
    :type classNamingConvention: INamingConvention|None
"""
        # The new property.
        originalProperty = None
        if memberName in originalMemberNameList:
            member = getattr(cls, memberName)
            
            # There's already a member with that name and it's not a property
            if not isinstance(member, property):
                raise InvalidPropertyOverrideError(memberName, cls.__name__)
            
            # If property already exists, we will just modify it.
            originalProperty = member
        
        kwargs = {self._KEY_PROPERTY_GET: getattr(originalProperty, self._KEY_PROPERTY_GET, None) or getter,
                  self._KEY_PROPERTY_SET: getattr(originalProperty, self._KEY_PROPERTY_SET, None) or setter,
                  self._KEY_PROPERTY_DEL: getattr(originalProperty, self._KEY_PROPERTY_DEL, None) or None,
                  self._KEY_PROPERTY_DOC: getattr(originalProperty, self._KEY_PROPERTY_DOC, None) or None}
        setattr(cls, memberName, property(**kwargs))

    def remove(self, cls, originalMemberNameList, memberName, classNamingConvention):
        """
    :type cls: type
    :type originalMemberNameList: list(str)
    :type classNamingConvention: INamingConvention|None
"""
        if memberName not in originalMemberNameList:
            delattr(cls, memberName)
