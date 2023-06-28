import typing as t

from aliases.space import AliasSpace, _sentinel
import polars as pl


@pl.api.register_series_namespace("aliases")
class PolarsSeriesAliasAccessor:
    def __init__(self, s: pl.Series) -> None:
        self._s = s

    def representative(
        self,
        space: AliasSpace,
        missing: t.Any = _sentinel,
        raise_missing: bool = False,
    ) -> pl.Series:
        result: pl.Series = space.processor(self._s)
        if raise_missing:
            default = None
        elif missing is _sentinel:
            default = pl.first()
        else:
            default = missing
        result = result.map_dict(remapping=space.mapper, default=default)
        if raise_missing:
            is_missing = result.is_null()
            if is_missing.any():
                raise KeyError(
                    f"{self._s.filter(is_missing).to_list()} not found in {space}"
                )
        return result


@pl.api.register_expr_namespace("aliases")
class PolarsExprAliasAccessor:
    def __init__(self, expr: pl.Expr) -> None:
        self._expr = expr

    def representative(self, space: AliasSpace, missing: t.Any = _sentinel) -> pl.Expr:
        result: pl.Expr = space.processor(self._expr)

        if missing is _sentinel:
            default = pl.first()
        else:
            default = missing
        return result.map_dict(remapping=space.mapper, default=default)


@pl.api.register_dataframe_namespace("aliases")
class PolarsDataFrameAliasAccessor:
    def __init__(self, df: pl.DataFrame) -> None:
        self._df = df

    def representative(
        self,
        space: AliasSpace,
        columns: list[str] | None = None,
        missing: t.Any = _sentinel,
        raise_missing: bool = False,
    ) -> pl.DataFrame:
        cols = columns if columns is not None else pl.Utf8
        missing = missing if not raise_missing else None
        result = self._df.with_columns(
            pl.col(cols).aliases.representative(space=space, missing=missing)
        )

        if raise_missing:
            if result.select(pl.col(cols)).null_count().sum(axis=1) > 0:
                raise KeyError("Some element in the DataFrame could not be found")
        return result


@pl.api.register_lazyframe_namespace("aliases")
class PolarsLazyFrameAliasAccessor:
    def __init__(self, ldf: pl.LazyFrame) -> None:
        self._ldf = ldf

    def representative(
        self,
        space: AliasSpace,
        columns: list[str] | None = None,
        missing: t.Any = _sentinel,
    ) -> pl.LazyFrame:
        cols = columns if columns is not None else pl.Utf8
        return self._ldf.with_columns(
            pl.col(cols).aliases.representative(space=space, missing=missing)
        )
