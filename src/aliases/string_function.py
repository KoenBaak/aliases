import typing as t
from abc import ABC, abstractmethod
from aliases.third_party_classes import (
    _has_polars,
    _has_pandas,
    plSeries,
    plExpr,
    pdSeries,
)

if t.TYPE_CHECKING:
    try:
        import pandas as pd
    except ImportError:
        pass

    try:
        import polars as pl
    except ImportError:
        pass

StringArg: t.TypeAlias = t.Union[str, "pd.Series", "pl.Series", "pl.Expr"]


class StringFunction(ABC):
    """An Abstract Base Class to represent a function that maps strings to strings
    """
    @abstractmethod
    def handle_builtin_str(self, x: str) -> str:
        """Implementation of the function for Python builtin strings"""
        pass

    @abstractmethod
    def handle_pandas_series(self, s: "pd.Series") -> "pd.Series":
        """Implementation of the function for Pandas Series with string values"""
        pass

    @abstractmethod
    def handle_polars_series(self, s: "pl.Series") -> "pl.Series":
        """Implementation of the function for Polars Series with string values"""
        pass

    @abstractmethod
    def handle_polars_expr(self, e: "pl.Expr") -> "pl.Expr":
        """Implementation of the function for Polars Expr"""
        pass

    def __call__(self, x: StringArg) -> StringArg:
        """Call this StringFunction

        This function will dispatch to one of the implementations depending
        on the type of the input argument

        Parameters
        ----------
        x
            Input String Argument
        """
        if isinstance(x, str):
            return self.handle_builtin_str(x)
        elif _has_pandas and isinstance(x, pdSeries):
            return self.handle_pandas_series(x)
        elif _has_polars and isinstance(x, plSeries):
            return self.handle_polars_series(x)
        elif _has_polars and isinstance(x, plExpr):
            return self.handle_polars_expr(x)
        raise TypeError


class StringIdentity(StringFunction):
    def handle_builtin_str(self, x: str) -> str:
        return x

    def handle_pandas_series(self, s: "pd.Series") -> "pd.Series":
        return s

    def handle_polars_expr(self, e: "pl.Expr") -> "pl.Expr":
        return e

    def handle_polars_series(self, s: "pl.Series") -> "pl.Series":
        return s


class ToLowerCase(StringFunction):
    def handle_builtin_str(self, x: str) -> str:
        return x.lower()

    def handle_pandas_series(self, s: "pd.Series") -> "pd.Series":
        return s.str.lower()

    def handle_polars_expr(self, e: "pl.Expr") -> "pl.Expr":
        return e.str.to_lowercase()

    def handle_polars_series(self, s: "pl.Series") -> "pl.Series":
        return s.str.to_lowercase()


class RightStrip(StringFunction):
    def handle_builtin_str(self, x: str) -> str:
        return x.rstrip()

    def handle_pandas_series(self, s: "pd.Series") -> "pd.Series":
        return s.str.rstrip()

    def handle_polars_expr(self, e: "pl.Expr") -> "pl.Expr":
        return e.str.rstrip()

    def handle_polars_series(self, s: "pl.Series") -> "pl.Series":
        return s.str.rstrip()
