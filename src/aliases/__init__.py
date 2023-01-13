__version__ = "0.5.6"

from aliases.space import AliasSpace
from aliases.string import AliasAwareString
from aliases.dict import AliasAwareDict

try:
    from aliases.pandas_accessor import AliasAccessor
except ImportError:
    pass

__all__ = [AliasSpace, AliasAwareDict, AliasAwareString]
