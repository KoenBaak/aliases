import typing as t

if t.TYPE_CHECKING:
    from aliases.space import AliasSpace


class AliasAwareString:
    def __init__(self, data: t.Any, space: "AliasSpace") -> None:
        self.space = space
        self._data = str(data)

    @property
    def representative(self) -> str:
        return self.space.get_representative(self._data)

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return f"<'{self._data}' in {self.space}>"

    def __hash__(self):
        return hash(self.representative)

    def __eq__(self, data):
        return self.representative == self.space.str(data).representative
