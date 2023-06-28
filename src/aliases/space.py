import typing as t

from aliases.processor import StringProcessor

if t.TYPE_CHECKING:
    from aliases.string import AliasAwareString
    from aliases.dict import AliasAwareDict

_sentinel = object()


class AliasSpace:
    """The alias space stores information on existing aliases

    Parameters
    ----------
    data
        A dictionary where the keys are the preferred forms of strings and the
        values are lists of aliases
    processor
        A string processor that can be used to make certain variants of your
        aliases also count as aliases. When a processed string equals the
        processed form of one of the registered aliases, it is also considered
        to be an alias
    name
        Optional name of this alias space
    """
    def __init__(
        self,
        data: dict[str, list[str]],
        processor: StringProcessor | None = None,
        name: str | None = None,
    ) -> None:
        self._aliases = data
        self._mapper = None
        self.processor = processor if processor is not None else StringProcessor()
        self.name = name

    def add_alias(self, alias: str, representative: str) -> None:
        """Add an alias to the space

        Parameters
        ----------
        alias
            Alias to register
        representative
            Preferred form of the string
        """
        if representative in self._aliases:
            self._aliases[representative].append(alias)
        else:
            self._aliases[representative] = [alias]
            self.mapper[self.processor(representative)] = representative
        self.mapper[self.processor(alias)] = representative

    def create_mapper(self) -> dict[str, str]:
        """Creates a dictionary where the processed form of a registered alias maps to its representative
        """
        result = {
            self.processor(a): rep
            for rep, aliases in self._aliases.items()
            for a in aliases
        }

        # being an alias is reflexive, so we should add a representative as its
        # own alias
        for a in self._aliases:
            result[self.processor(a)] = a

        return result

    @property
    def mapper(self) -> dict[str, str]:
        if self._mapper is None:
            self._mapper = self.create_mapper()
        return self._mapper

    def get_representative(
        self, string: str, missing: t.Any = _sentinel, raise_missing: bool = False
    ) -> t.Any:
        """Get the representative of a given string

        Parameters
        ----------
        string
            The raw input string
        missing
            Value to return when the string is not a registered alias. When this
            argument is not given, the raw input string will be returned back.
        raise_missing
            Whether an error must be raised when the input string is not a registered
            alias
        """
        result = self.mapper.get(self.processor(string), None)
        if result is None:
            if raise_missing:
                raise KeyError(f"{string} not found in {self}")
            if missing is _sentinel:
                return string
            return missing
        return result

    def str(self, data: t.Any) -> "AliasAwareString":
        """Create an AliasAwareString

        Parameters
        ----------
        data
            input string
        """
        from aliases.string import AliasAwareString

        return AliasAwareString(data=data, space=self)

    def dict(self, data: dict[str, t.Any] | None = None, **kwargs) -> "AliasAwareDict":
        """Create an AliasAwareDict

        Parameters
        ----------
        data
            input dictionary
        kwargs
            key, value pairs to add to the dictionary
        """
        from aliases.dict import AliasAwareDict

        return AliasAwareDict(space=self, data=data, **kwargs)

    def map(
        self,
        strings: t.Iterable[str],
        missing: t.Any = _sentinel,
        raise_missing: bool = False,
        return_list: bool = False,
    ) -> map | list:
        """Map an iterable of string to their representatives

        Parameters
        ----------
        strings
            Iterable of strings
        missing
            Value to return when the string is not a registered alias. When this
            argument is not given, the raw input string will be returned back.
        raise_missing
            Whether an error must be raised when the input string is not a registered
            alias
        return_list
            Whether to cast the output map to a list object
        """
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
        return self.processor(item) in self.mapper

    def __repr__(self) -> str:
        if self.name is None:
            return "AliasSpace"
        return f"AliasSpace {self.name}"
