Aliases
=======
A very small Python package for keeping track of aliases.

Installation
------------

    $ pip install aliases

Getting Started
---------------
Keeping track of aliases in your data can be annoying. This small packages
provides three small classes than can help you in the bookkeeping associated
with the occurrences of aliases in your data.

The ``AliasSpace`` objects keeps track of existing aliases. As input is accepts
a dictionary where a string (the "preferred" form) points to a list of all its
aliases. Using the ``str`` method on the space, we can transform regular strings
into ``AliasAwareString`` objects. 

.. code-block:: python

    >>> from aliases import AliasSpace
    >>>
    >>> s = AliasSpace(
    >>>     {"The Netherlands": ["NL", "Netherlands", "Holland"]},
    >>>     case_sensitive=False
    >>> )
    >>>
    >>> s.str("nl")
    <'nl' in AliasSpace>


The preferred form of an ``AliasAwareString`` is called its *representative*
(because it represents the equivalance class of the string under the equivalance
relation of being aliases).

.. code-block:: python

    >>> s.str("nl").representative
    'The Netherlands'

``AliasAwareString`` objects with the same representative are considered equal
and have the same hash.

.. code-block:: python

    >>> s.str("holland") == s.str("NL")
    True

    >>> data = {s.str("holland"): 12345}
    >>> data[s.str("nl")]
    12345

The example above already shows how alias aware strings can be used to store
data without worrying to much about the different aliases around. However, it
is still annoying to cast to an ``AliasAwareString`` every time manually. To
solve this you can use the ``AliasAwareDict``. This object can be created using
the ``dict`` method on the space. 

.. code-block:: python

    >>> data = s.dict(holland=12345)
    >>> data['nl']
    12345

Finally, the ``AliasAwareSpace`` object has a ``map`` method which can be used
to find the representatives of a list of strings easily. The following example
was the original motivation for building this package:

.. code-block:: python

    >>> import pandas as pd
    >>> df = pd.DataFrame(
    >>>    {"Country": ["NL", "Netherlands", "Belgium"], "SomeData": [10, 11, 12]}
    >>> )
    >>> df
               Country  SomeData
    0               NL        10
    1      Netherlands        11
    2          Belgium        12
    >>> df.assign(Country=s.map(df.Country, return_list=True))
              Country  SomeData
    0  The Netherlands        10
    1  The Netherlands        11
    2          Belgium        12
    >>> df.assign(Country=s.map(df.Country, return_list=True, missing=pd.NA))
               Country  SomeData
    0  The Netherlands        10
    1  The Netherlands        11
    2             <NA>        12

Documentation
-------------
Coming soon...