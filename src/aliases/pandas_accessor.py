import typing as t

import pandas as pd

from aliases.space import AliasSpace, _sentinel


@pd.api.extensions.register_series_accessor("alias")
class SeriesAliasAccessor:
    def __init__(self, pandas_obj: pd.Series) -> None:
        self._obj = pandas_obj

    def preprocess(self, space: AliasSpace) -> pd.Series:
        result = self._obj
        if not space.case_sensitive:
            result = result.str.lower()
        if space.pandas_process_func is not None:
            result = space.pandas_process_func(result)
        return result

    def representative(
        self,
        space: AliasSpace,
        missing: t.Any = _sentinel,
        raise_missing: bool = False,
    ) -> pd.Series:
        result = self.preprocess(space=space).map(space.mapper)
        is_missing = result.isna()
        if is_missing.any() and raise_missing:
            raise KeyError(f"{self._obj[is_missing].values} not found in {space}")
        if missing is not _sentinel:
            return result.fillna(missing)
        result[is_missing] = self._obj[is_missing].values
        return result


@pd.api.extensions.register_dataframe_accessor("alias")
class DataFrameAliasAccessor:
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
                col: self._obj[col].alias.representative(
                    space=space, missing=missing, raise_missing=raise_missing
                )
                for col in columns
            }
        )
