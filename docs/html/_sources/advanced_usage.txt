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

.. code-block:: python

    @synthesize_constructor()
    @synthesize_property('value')
    class Double:
        def __init__(self):
            self._value *= 2

    print(Double(10).value)

Displays

.. code-block:: python

    20

The custom constructor can consume extra arguments *(not synthesized members or properties)*.

For more examples, see product's unit tests.

