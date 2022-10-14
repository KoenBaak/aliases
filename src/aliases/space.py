import typing as t

_sentinel = object()

if t.TYPE_CHECKING:
    from aliases.string import AliasAwareString
    from aliases.dict import AliasAwareDict

    try:
        import pandas as pd
    except ImportError:
        pass


class AliasSpace:
    def __init__(
        self,
        data: dict[str, list[str]],
        case_sensitive: bool = True,
        process_func: t.Callable[[str], str] | None = None,
        pandas_process_func: t.Callable[["pd.Series"], "pd.Series"] | None = None,
        name: str | None = None,
    ) -> None:
        self._aliases = data
        self._mapper = None
        if pandas_process_func is None and process_func is not None:
            pandas_process_func = lambda s: s.apply(process_func)
        self._process_func = process_func or (lambda x: x)
        self.pandas_process_func = pandas_process_func
        self._case_sensitive = case_sensitive
        self.name = name

    @property
    def case_sensitive(self) -> bool:
        return self._case_sensitive

    @case_sensitive.setter
    def case_sensitive(self, value: bool) -> None:
        self._case_sensitive = value
        self._mapper = self.create_mapper()

    def add_alias(self, alias: str, representative: str) -> None:
        if representative in self._aliases:
            self._aliases[representative].append(alias)
        else:
            self._aliases[representative] = [alias]
            self.mapper[self.preprocess(representative)] = representative
        self.mapper[self.preprocess(alias)] = representative

    def preprocess(self, string: str) -> str:
        result: str = string
        if not self.case_sensitive:
            result = result.lower()
        return self._process_func(result)

    def create_mapper(self) -> dict[str, str]:
        result = {
            self.preprocess(a): rep
            for rep, aliases in self._aliases.items()
            for a in aliases
        }

        # being an alias is reflexive, so we should add a representative as its
        # own alias
        for a in self._aliases:
            result[self.preprocess(a)] = a

        return result

    @property
    def mapper(self) -> dict[str, str]:
        if self._mapper is None:
            self._mapper = self.create_mapper()
        return self._mapper

    def get_representative(
        self, string: str, missing: t.Any = _sentinel, raise_missing: bool = False
    ) -> t.Any:
        result = self.mapper.get(self.preprocess(string), None)
        if result is None:
            if raise_missing:
                raise KeyError(f"{string} not found in {self}")
            if missing is _sentinel:
                return string
            return missing
        return result

    def str(self, data: t.Any) -> "AliasAwareString":
        from aliases.string import AliasAwareString

        return AliasAwareString(data=data, space=self)

    def dict(self, data: dict[str, t.Any] | None = None, **kwargs) -> "AliasAwareDict":
        from aliases.dict import AliasAwareDict

        return AliasAwareDict(space=self, data=data, **kwargs)

    def map(
        self,
        strings: t.Iterable[str],
        missing: t.Any = _sentinel,
        raise_missing: bool = False,
        return_list: bool = False,
    ) -> map | list:
        result = map(
            lambda x: self.get_representative(
                x, missing=missing, raise_missing=raise_missing
            ),
            strings,
        )
        if return_list:
            return list(result)
        return result

    def __contains__(self, item: str) -> bool:
        return self.preprocess(item) in self.mapper

    def __repr__(self) -> str:
        if self.name is None:
            return "AliasSpace"
        return f"AliasSpace {self.name}"
