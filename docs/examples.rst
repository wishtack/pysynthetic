Examples
********

Synthetic properties
====================

With **PySynthetic**, the following code *(8 lines)*...

.. code-block:: python

    from synthetic import synthesize_constructor, synthesize_property
    
    @synthesize_property('a', contract = int)
    @synthesize_property('b', contract = list)
    @synthesize_property('c', default = "", contract = str, read_only = True)
    @synthesize_constructor()
    class ShortAndClean(object):
        pass

... replaces this *(43 lines)*:

.. code-block:: python

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

.. code-block:: python

    from synthetic import synthesize_constructor, synthesize_member
    
    @synthesize_member('a', contract = int)
    @synthesize_member('b', contract = list)
    @synthesize_member('c', default = "", contract = str, read_only = True)
    @synthesize_constructor()
    class ShortAndClean(object):
        pass

...will replace this *(37 lines)*:

.. code-block:: python

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

