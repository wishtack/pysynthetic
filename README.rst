Be synthetic with PySynthetic
#############################

**PySynthetic** is a set of tools that aims to make writing Python classes shorter and "cleaner".

For instance, one can add properties and accessors *(getters/setters)* to a class with only one line of code *(using respectively* ``synthesize_property`` *and* ``synthesize_member`` *decorators)*, thus making the code more than 5 times shorter *(see* `examples`_ *)*. One can even avoid the laborious task of members initialization by using the ``synthesize_constructor`` decorator that takes care of writing the ``__init__`` method.

**PySynthetic** is also useful for applying strict type checking with no pain just by using the decorators' ``contract`` argument *(see* `PyContracts <http://andreacensi.github.com/contracts/>`_ *)*.

Help and ideas are appreciated! Thank you!

.. image:: https://api.flattr.com/button/flattr-badge-large.png
    :target: https://flattr.com/thing/1167227/

.. image:: https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif
    :target: https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=yjaaidi%40gmail%2ecom&lc=US&item_name=yjaaidi&currency_code=EUR&bn=PP%2dDonationsBF%3abtn_donate_SM%2egif%3aNonHosted

Resources
*********

* `Documentation <http://pysynthetic.readthedocs.org/>`_
* `Bug Tracker <http://github.com/yjaaidi/pysynthetic/issues>`_
* `Code <http://github.com/yjaaidi/pysynthetic>`_
* `Mailing List <https://groups.google.com/group/pysynthetic>`_ <pysynthetic@googlegroups.com>

Installation
************

.. code-block:: shell

    pip install pysynthetic

Or simply from the tarball or source code if you are not using *pip*.

.. code-block:: shell

    python setup.py install

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

But, if you are more into accessors than properties, you can use ``synthesize_member`` decorator instead.

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

