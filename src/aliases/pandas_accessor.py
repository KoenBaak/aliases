import typing as t

import pandas as pd

from aliases.space import AliasSpace, _sentinel


@pd.api.extensions.register_series_accessor("aliases")
class PandasSeriesAliasAccessor:
    def __init__(self, pandas_obj: pd.Series) -> None:
        self._obj = pandas_obj

    def representative(
        self,
        space: AliasSpace,
        missing: t.Any = _sentinel,
        raise_missing: bool = False,
    ) -> pd.Series:
        result = space.processor(self._obj).map(space.mapper)
        is_missing = result.isna()
        if is_missing.any() and raise_missing:
            raise KeyError(f"{self._obj[is_missing].values} not found in {space}")
        if missing is not _sentinel:
            return result.fillna(missing)
        result[is_missing] = self._obj[is_missing].values
        return result


@pd.api.extensions.register_dataframe_accessor("aliases")
class PandasDataFrameAliasAccessor:
    def __init__(self, pandas_obj: pd.DataFrame) -> None:
        self._obj = pandas_obj

    def representative(
        self,
        space: AliasSpace,
        columns: list[str] | None = None,
        missing: t.Any = _sentinel,
        raise_missing: bool = False,
    ) -> pd.DataFrame:
        if columns is None:
            columns = self._obj.columns[
                self._obj.applymap(lambda x: isinstance(x, str)).all(axis=0)
            ].values.tolist()
        return self._obj.assign(
            **{
                col: self._obj[col].aliases.representative(
                    space=space, missing=missing, raise_missing=raise_missing
                )
                for col in columns
            }
        )
