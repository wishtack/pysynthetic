
from .i_naming_convention import INamingConvention
from .naming_convention_camel_case import NamingConventionCamelCase
from .naming_convention_underscore import NamingConventionUnderscore
from .decorators import naming_convention, synthesize_constructor, synthesize_equality, \
                        synthesize_member, synthesize_property, \
                        namingConvention, synthesizeConstructor, synthesizeEquality, \
                        synthesizeMember, synthesizeProperty

from .property_delegate import InvalidPropertyOverrideError
from .synthetic_meta_data import DuplicateMemberNameError

__all__ = ['DuplicateMemberNameError', 'InvalidPropertyOverrideError', 'INamingConvention',
           'NamingConventionCamelCase', 'NamingConventionUnderscore',
           'namingConvention', 'synthesizeEquality', 'synthesizeConstructor',
           'synthesizeMember', 'synthesizeProperty',
           'naming_convention', 'synthesize_equality', 'synthesize_constructor',
           'synthesize_member', 'synthesize_property']

__version__ = "0.5.1"

