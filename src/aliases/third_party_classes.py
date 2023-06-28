try:
    import pandas as pd

    _has_pandas = True
    pdSeries = pd.Series
except ImportError:
    _has_pandas = False
    pdSeries = None

try:
    import polars as pl

    _has_polars = True
    plSeries = pl.Series
    plExpr = pl.Expr
except ImportError:
    _has_polars = False
    plSeries = None
    plExpr = None
