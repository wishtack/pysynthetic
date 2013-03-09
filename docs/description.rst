Be synthetic with PySynthetic
#############################

**PySynthetic** is a set of tools that aims to make writing Python classes shorter and "cleaner".

For instance, one can add properties and accessors *(getters/setters)* to a class with only one line of code *(using respectively* :meth:`synthesize_property <synthetic.synthesize_property>` *and* :meth:`synthesize_member <synthetic.synthesize_member>` *decorators)*, thus making the code more than 5 times shorter *(see* `examples`_ *)*. One can even avoid the laborious task of members initialization by using the :meth:`synthesize_constructor <synthetic.synthesize_constructor>` decorator that takes care of writing the ``__init__`` method.

**PySynthetic** is also useful for applying strict type checking with no pain just by using the decorators' ``contract`` argument *(see* `PyContracts <http://andreacensi.github.com/contracts/>`_ *)*.

Help and ideas are appreciated! Thank you!

.. image:: https://api.flattr.com/button/flattr-badge-large.png
    :target: https://flattr.com/thing/1167227/

.. image:: https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif
    :target: https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=yjaaidi%40gmail%2ecom&lc=US&item_name=yjaaidi&currency_code=EUR&bn=PP%2dDonationsBF%3abtn_donate_SM%2egif%3aNonHosted

