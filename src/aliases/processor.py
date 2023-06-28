import typing as t
from aliases.string_function import (
    StringFunction,
    StringArg,
    StringIdentity,
    ToLowerCase,
    RightStrip,
)


class StringProcessor:
    def __init__(self, f: StringFunction | None = None) -> None:
        self.f = f if f is not None else StringIdentity()

    def __call__(self, x: StringArg) -> StringArg:
        return self.f(x)

    def compose(
        self, other: t.Union[StringFunction, "StringProcessor"]
    ) -> "StringProcessor":
        current = self.f
        f = other if not isinstance(other, StringProcessor) else other.f
        processor = StringProcessor()
        processor.f = lambda x: f(current(x))
        return processor

    def lower(self) -> "StringProcessor":
        return self.compose(ToLowerCase())

    def rstrip(self) -> "StringProcessor":
        return self.compose(RightStrip())
