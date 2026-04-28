from collections.abc import Sequence
from dataclasses import dataclass

from typstpresenter.model.Element import Element
from typstpresenter.model.text.Atom import Atom


@dataclass(frozen=True)
class Text(Element):
    value: Sequence[Atom]

    def __post_init__(self) -> None:
        if isinstance(self.value, str):
            raise TypeError("Use Text(('some content'),) instead of Text('some content').")

    def __str__(self) -> str:
        return "".join(str(v) for v in self.value)
