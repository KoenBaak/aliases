__version__ = "0.6.2"

from aliases.space import AliasSpace
from aliases.string import AliasAwareString
from aliases.dict import AliasAwareDict
from aliases.processor import StringProcessor

try:
    from aliases.pandas_accessor import (
        PandasSeriesAliasAccessor,
        PandasDataFrameAliasAccessor,
    )
except ImportError:
    pass

try:
    from aliases.polars_accessor import (
        PolarsSeriesAliasAccessor,
        PolarsExprAliasAccessor,
        PolarsDataFrameAliasAccessor,
        PolarsLazyFrameAliasAccessor,
    )
except ImportError:
    pass

__all__ = [AliasSpace, AliasAwareDict, AliasAwareString, StringProcessor]
