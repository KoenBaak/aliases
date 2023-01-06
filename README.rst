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
with the occurrences of aliases in your data. There are also pandas accessors 
that make it possible to enforce aliases immediately for a whole pandas 
Series or DataFrame.

The ``AliasSpace`` objects keeps track of existing aliases. As input is accepts
a dictionary where a string (the "preferred" form) points to a list of all its
aliases. Using the ``str`` method on the space, we can transform regular strings
into ``AliasAwareString`` objects. 

.. code-block:: python

    >>> s = AliasSpace(
    >>>     {
    >>>         "The Netherlands": ["NL", "Netherlands", "Holland"],
    >>>         "The Hague": ["Den Haag", "'s-Gravenhage"],
    >>>         "Amsterdam": ["Adam"],
    >>>     },
    >>>     case_sensitive=False,
    >>> )
    >>>
    >>> s.str("nl")
    <'nl' in AliasSpace>


The preferred form of an ``AliasAwareString`` is called its *representative*.

.. code-block:: python

    >>> s.str("nl").representative
    'The Netherlands'

``AliasAwareString`` objects with the same representative are considered equal
and have the same hash.

.. code-block:: python

    >>> s.str("holland") == s.str("NL")
    True
    >>>
    >>> data = {s.str("holland"): 12345}
    >>> data[s.str("nl")]
    12345

The example above already shows how alias aware strings can be used to store
data without worrying too much about the different aliases around. However, it
is still annoying to cast to an ``AliasAwareString`` every time manually. To
solve this you can use the ``AliasAwareDict``. This object can be created using
the ``dict`` method on the space.

.. code-block:: python

    >>> data = s.dict(holland=12345)
    >>> data['nl']
    12345

Finally, when you have ``pandas`` installed, the ``aliases`` package will
register accessors for series and dataframes. This allows you to easily enforce
aliases in your pandas DataFrame. The following example was the original
motivation for building this package:

.. code-block:: python

    >>> import pandas as pd
    >>> df = pd.DataFrame(
    >>>     {
    >>>         "Country": ["NL", "Netherlands", "Belgium"],
    >>>         "City": ["Den Haag", "amsterdam", "Brussel"],
    >>>         "SomeData": [10, 11, 12],
    >>>     }
    >>> )
    >>> df
           Country       City  SomeData
    0           NL   Den Haag        10
    1  Netherlands  amsterdam        11
    2      Belgium    Brussel        12
    >>>
    >>> df.Country.aliases.representative(space=s)
    0    The Netherlands
    1    The Netherlands
    2            Belgium
    Name: Country, dtype: object
    >>>
    >>> df.aliases.representative(space=s, missing=pd.NA)
               Country       City  SomeData
    0  The Netherlands  The Hague        10
    1  The Netherlands  Amsterdam        11
    2             <NA>       <NA>        12

Documentation
-------------
Coming soon...
