.. PySynthetic documentation master file, created by
   sphinx-quickstart on Fri Mar  1 21:46:19 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Be synthetic with PySynthetic
=============================

Example::
        
    class ThisHurtsMyKeyboard:
    
        def __init__(self, a, b, c = None):
            """
        :type a: int
        :type b: str
        :type c: list|None
    """
            self._a = a
            self._b = b
            self._c = c
        
        @property
        def a(self):
            return self._a
    
        @a.setter
        def a(self, value):
            self._a = value
    
    ...

Module documentation
====================

.. automodule:: synthetic
    :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

