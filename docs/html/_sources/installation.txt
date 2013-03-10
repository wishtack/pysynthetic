Installation
************

As there is a temporary issue with the **PySynthetic** => **PyContracts** => **PyParsing** dependency chain (**PyParsing** >= 2.0.0 is not compatible with Python 2), **PySynthetic** must be installed this way.

.. code-block:: shell

    pip install 'pyparsing<2.0.0' pysynthetic

Or simply from the tarball or source code if you are not using *pip*.

.. code-block:: shell

    python setup.py install

