Getting Started
===============

Keeping track of aliases in your data can be annoying. This small packages
provides some utilities to help you in the bookkeeping associated
with the occurrences of aliases in your data. There are accessors for both pandas
and polars that make it possible to enforce aliases on Series and DataFrames.

The AliasSpace
--------------
An :class:`~aliases.space.AliasSpace` can be made to store information on existing
aliases in your data. As input a dictionary should be given where the keys are
the preferred form (the *representative*) and the values are lists of all its aliases.

.. code-block:: python

    s = AliasSpace(
        {
            "The Netherlands": ["NL", "Netherlands", "Holland"],
            "The Hague": ["Den Haag", "'s-Gravenhage"],
            "Amsterdam": ["Adam"],
        },
    )

Any string can now be cast to an :class:`~aliases.string.AliasAwareString`, which
has an `representative` property

.. code-block:: python

    >>> x = s.str("NL")
    >>> x.representative
    "The Netherlands"

String Processors
-----------------

Note that in the example above we have

.. code-block:: python

    >>> x = s.str("nl")
    >>> x.representative
    "nl"

This is because the string "NL" is registered as an alias of "The Netherlands"
but "nl" is not. Often times, you want certain variants of your aliases to also
count as aliases. To enable this, you can pass a :class:`~aliases.processor.StringProcessor`
to your space. When a processor is set, any string will count as an alias when
its processed form is equal to the processed form of one of the registered aliases.

For example

.. code-block:: python

    s = AliasSpace(
        {
            "The Netherlands": ["NL", "Netherlands", "Holland"],
            "The Hague": ["Den Haag", "'s-Gravenhage"],
            "Amsterdam": ["Adam"],
        },
        processor=StringProcessor().lower()
    )
    x = s.str("nl")

.. code-block:: python

    >>> x.representative
    "The Netherlands"

Aliases in Data
---------------

This package is mainly there to solve the issue of aliases occurring in datasets.
Therefore, there are accessors for the popular pandas and polars data libraries.

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