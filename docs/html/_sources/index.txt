.. PySynthetic documentation master file, created by
   sphinx-quickstart on Fri Mar  1 21:46:19 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Be synthetic with PySynthetic
#############################

@todo: ...description and motivation...

Examples
********

Synthetic properties
====================

With PySynthetic, the following code *(8 lines)*...
::

    from synthetic import synthesize_constructor, synthesize_property
    
    @synthesize_property('a', contract = int)
    @synthesize_property('b', contract = list)
    @synthesize_property('c', default = "", contract = str, read_only = True)
    @synthesize_constructor()
    class ShortAndClean(object):
        pass

... replaces this *(43 lines)*:
::

    from contracts import contract
    
    class ThisHurtsMyKeyboard(object):
    
        @contract
        def __init__(self, a, b, c = ""):
            """
        :type a: int
        :type b: list
        :type c: str
    """
            self._a = a
            self._b = b
            self._c = c
            
        @property
        def a(self):
            return self._a
        
        @a.setter
        @contract
        def a(self, value):
            """
        :type value: int
    """
            self._a = value
        
        @property
        def b(self):
            return self._b
        
        @b.setter
        @contract
        def b(self, value):
            """
        :type value: list
    """
            self._b = value
        
        @property 
        def c(self):
            return self._c

Synthetic accessors
===================

But, if you are more into accessors than properties, you can use :meth:`synthesize_member <synthetic.synthesize_member>` decorator instead.

This way, the following code *(8 lines)*...
::

    from synthetic import synthesize_constructor, synthesize_member
    
    @synthesize_member('a', contract = int)
    @synthesize_member('b', contract = list)
    @synthesize_member('c', default = "", contract = str, read_only = True)
    @synthesize_constructor()
    class ShortAndClean(object):
        pass

...will replace this *(37 lines)*:
::

    from contracts import contract
    
    class ThisHurtsMyKeyboard(object):
    
        @contract
        def __init__(self, a, b, c = ""):
            """
        :type a: int
        :type b: list
        :type c: str
    """
            self._a = a
            self._b = b
            self._c = c
            
        def a(self):
            return self._a
        
        @contract
        def set_a(self, value):
            """
        :type value: int
    """
            self._a = value
        
        def b(self):
            return self._b
        
        @contract
        def set_b(self, value):
            """
        :type value: list
    """
            self._b = value
        
        def c(self):
            return self._c

Advanced usage
**************

Override synthesized member's accessors
=======================================

One can override the synthesized member's accessors by simply explicitly writing the methods.

Override synthesized property
=============================

One can override the synthesized property by simply explicitly writing the properties.

**Remark:** For the moment, it's impossible to override the property's setter without overriding the getter.

Override synthesized constructor
================================

One can use synthesized constructors to initialize members and properties values and still override it
to implement some additional processing.

Example:
::

    @synthesize_constructor()
    @synthesize_property('value')
    class Double:
        def __init__(self):
            self._value *= 2

    print(Double(10).value)

Displays
::

    20

The custom constructor can consume extra arguments *(not synthesized members or properties)*.

For more examples, see product's unit tests.

Module documentation
********************

Underscore notation
===================

.. autofunction:: synthetic.naming_convention
.. autofunction:: synthetic.synthesize_constructor
.. autofunction:: synthetic.synthesize_member
.. autofunction:: synthetic.synthesize_property

CamelCase notation
==================

Sorry Guido, but I like CamelCase.

.. autofunction:: synthetic.namingConvention
.. autofunction:: synthetic.synthesizeConstructor
.. autofunction:: synthetic.synthesizeMember
.. autofunction:: synthetic.synthesizeProperty

Indices and tables
******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

