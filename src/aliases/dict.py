import typing as t
from collections.abc import MutableMapping

if t.TYPE_CHECKING:
    from aliases.space import AliasSpace
    from aliases.string import AliasAwareString

AliasKey: t.TypeAlias = t.Union[str, "AliasAwareString"]


class AliasAwareDict(MutableMapping):
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

    def __getitem__(self, item: AliasKey) -> t.Any:
        return self._data.__getitem__(self.space.str(item))

    def __setitem__(self, key: AliasKey, value: t.Any) -> None:
        return self._data.__setitem__(self.space.str(key), value)

    def __delitem__(self, key: AliasKey) -> None:
        return self._data.__delitem__(self.space.str(key))

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __repr__(self) -> str:
        return f"AliasAwareDict {self.to_dict()}"
