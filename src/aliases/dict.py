import typing as t

if t.TYPE_CHECKING:
    from aliases.space import AliasSpace
    from aliases.string import AliasAwareString


class AliasAwareDict:
    def __init__(
        self, space: "AliasSpace", data: dict[str, t.Any] | None = None, **kwargs
    ) -> None:
        self.space = space
        data = data or {}
        data.update(**kwargs)
        self._data: dict["AliasAwareString", t.Any] = {
            self.space.str(key): value for key, value in data.items()
        }

    def to_dict(self) -> dict[str, t.Any]:
        return {k.representative: v for k, v in self._data.items()}

    def __getitem__(self, item: t.Union[str, "AliasAwareString"]) -> t.Any:
        return self._data.__getitem__(self.space.str(item))

    def __setitem__(self, key: t.Union[str, "AliasAwareString"], value: t.Any) -> None:
        return self._data.__setitem__(self.space.str(key), value)

    def __repr__(self) -> str:
        return f"AliasAwareDict {self.to_dict()}"
