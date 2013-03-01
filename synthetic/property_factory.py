#-*- coding: utf-8 -*-
#
# Created on Feb 28, 2013
#
# @author: Younes JAAIDI
#
# $Id$
#

from .i_member_factory import IMemberFactory
from contracts import new_contract

new_contract('IMemberFactory', IMemberFactory)

class PropertyFactory(IMemberFactory):

    def memberDict(self, memberName, getter, setter, classNamingConvention):
        """
    :type memberName: str
    :type classNamingConvention: INamingConvention:None
"""
        kwargs = {'fget': getter}
        if setter is not None:
            kwargs['fset'] = setter
        return {memberName: property(**kwargs)}
